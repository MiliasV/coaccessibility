import pyproj
import swifter
import networkx as nx
import osmnx as ox
from geoalchemy2 import Geometry, WKTElement
import geopandas as gpd
from sqlalchemy import create_engine
from shapely.geometry import Point
from shapely.ops import transform
import sys
sys.path.append('../')
from config import db_connection_string
from sqlalchemy import create_engine
from descartes import PolygonPatch
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
# ox.config(log_console=True, use_cache=True)
import matplotlib.pyplot as plt
from descartes import PolygonPatch
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
# ox.config(log_console=True, use_cache=True)
# ox.__version__
import matplotlib.pyplot as plt
import time


def make_iso_polys(G, G_wgs84, point, trip_times,edge_buff=25, node_buff=50, infill=False):
    source_node = ox.distance.nearest_nodes(G_wgs84, point.x, point.y)
    isochrone_polys = []
    for trip_time in sorted(trip_times, reverse=True):
        subgraph = nx.ego_graph(G, source_node, radius=trip_time, distance='time')
        node_points = [Point((data['x'], data['y'])) for node, data in subgraph.nodes(data=True)]
        nodes_gdf = gpd.GeoDataFrame({'id': subgraph.nodes()}, geometry=node_points)
        nodes_gdf = nodes_gdf.set_index('id')
        edge_lines = []
        for n_fr, n_to in subgraph.edges():
            f = nodes_gdf.loc[n_fr].geometry
            t = nodes_gdf.loc[n_to].geometry
            edge_lookup = G.get_edge_data(n_fr, n_to)[0].get('geometry',  LineString([f,t]))
            edge_lines.append(edge_lookup)

        n = nodes_gdf.buffer(node_buff).geometry
        e = gpd.GeoSeries(edge_lines).buffer(edge_buff).geometry
        all_gs = list(n) + list(e)
        new_iso = gpd.GeoSeries(all_gs).unary_union
        # try to fill in surrounded areas so shapes will appear solid and blocks without white space inside them
        if infill:
            try:
                new_iso = Polygon(new_iso.exterior)
            except:
                return None
    isochrone_polys.append(new_iso)
    return isochrone_polys[0]

def make_iso_polys_for_viz(G, G_wgs84, point, trip_times,edge_buff=25, node_buff=50, infill=False):
    source_node = ox.distance.nearest_nodes(G_wgs84, point.x, point.y)
    isochrone_polys = []
    for trip_time in sorted(trip_times, reverse=True):
        subgraph = nx.ego_graph(G, source_node, radius=trip_time, distance='time')
        node_points = [Point((data['x'], data['y'])) for node, data in subgraph.nodes(data=True)]
        nodes_gdf = gpd.GeoDataFrame({'id': subgraph.nodes()}, geometry=node_points)
        nodes_gdf = nodes_gdf.set_index('id')

        edge_lines = []
        for n_fr, n_to in subgraph.edges():
            f = nodes_gdf.loc[n_fr].geometry
            t = nodes_gdf.loc[n_to].geometry
            edge_lookup = G.get_edge_data(n_fr, n_to)[0].get('geometry',  LineString([f,t]))
            edge_lines.append(edge_lookup)

        n = nodes_gdf.buffer(node_buff).geometry
        e = gpd.GeoSeries(edge_lines).buffer(edge_buff).geometry
        all_gs = list(n) + list(e)
        new_iso = gpd.GeoSeries(all_gs).unary_union
        # try to fill in surrounded areas so shapes will appear solid and blocks without white space inside them
        if infill:
            new_iso = Polygon(new_iso.exterior)
        isochrone_polys.append(new_iso)
    return isochrone_polys

def add_iso_polys_to_viz(G, G_wgs84, point_list, trip_times, ax):
    for x in point_list:
        isochrone_polys = make_iso_polys_for_viz(G, G_wgs84, x, trip_times, edge_buff=25, node_buff=0, infill=True)
        for polygon, fc in zip(isochrone_polys, iso_colors):
            patch = PolygonPatch(polygon, fc=fc, ec='none', alpha=0.6, zorder=-1)
            ax.add_patch(patch)

if __name__ =='__main__':
    # db initialization
    # store to db
    db_connection_string = 'postgresql://postgres:postgres@localhost/age_segregation'
    engine = create_engine(db_connection_string)
    # "eindhoven", hague
    cities = ["eindhoven", "utrecht",  "rotterdam", "amsterdam", "hague"]
    for city in cities:
        print(city)
        # download the street network
        G_wgs84 = ox.graph_from_place(city,retain_all=True, buffer_dist=1000, network_type='walk')
        #remove isolated nodes
        G_wgs84.remove_nodes_from(list(nx.isolates(G_wgs84)))
        # netherlands projection
        G = ox.project_graph(G_wgs84, to_crs='epsg:28992')

        sql = "Select * from " + city + "." + city[0:3] + "_population_2020_100"
        # population data
        gdf_pop = gpd.GeoDataFrame.from_postgis(sql, engine, geom_col='geometry')

        # tranform from utm to wgs84
        wgs84 = pyproj.CRS('EPSG:4326')
        utm = pyproj.CRS('EPSG:28992')
        project = pyproj.Transformer.from_crs(utm, wgs84, always_xy=True).transform

        # create centroids and project them to wgs84
        gdf_pop["centroid_wgs84"] = gdf_pop.apply(lambda row: transform(project, row["geometry"].centroid), axis=1)
        # speed in meters per minute
        walking_speed = {'avg_speed': 75.6}

        start_time = time.time()

        trip_time = 15
        # for trip_time in trip_times:
        # add an edge attribute for time in minutes required to traverse each edge
        for age in walking_speed:
            for u, v, k, data in G.edges(data=True, keys=True):
                data['time'] = data['length'] / walking_speed[age]
            walking_speed_col_name = str(walking_speed[age]).replace(".","_")
            print("Done calculating speeds. Generating Polygons....")
            gdf_pop["iso_" + str(trip_time) +"_" + age + "_" + walking_speed_col_name] = gdf_pop.apply(lambda row: make_iso_polys(G, G_wgs84, row.centroid_wgs84, [trip_time], edge_buff=25, node_buff=0, infill=True), axis=1)
            print("DONE )--> iso_" + str(trip_time) +"_" + age + "_" + str(walking_speed[age]))
            print("Time needed --- %s seconds ---" % (time.time() - start_time))

        gdf_pop.to_postgis("iso_population_iso_2020_100_" + city[0:3] , con=engine, schema=city)
