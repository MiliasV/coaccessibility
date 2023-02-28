import pyproj
import swifter
import networkx as nx
import osmnx as ox
from geoalchemy2 import Geometry, WKTElement
import geopandas as gpd
from sqlalchemy import create_engine
from shapely.ops import transform
import sys
import numpy as np
sys.path.append('../')
from config import db_connection_string
from descartes import PolygonPatch
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import Point, LineString, Polygon
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
    cities = ["rotterdam"]
    # speed in meters per minute
    walking_speed = {'avg_speed': 75.6}
    # 5, 10, 15
    trip_times =[15, 10, 15]
    for city in cities:
        print(city)
        if city=='hague':
            # download the street network
            G_wgs84 = ox.graph_from_place(city + ",netherlands",retain_all=True, buffer_dist=1000, network_type='walk')
        else:
            G_wgs84 = ox.graph_from_place(city,retain_all=True, buffer_dist=1000, network_type='walk')
        #remove isolated nodes
        G_wgs84.remove_nodes_from(list(nx.isolates(G_wgs84)))
        # netherlands projection
        G = ox.project_graph(G_wgs84, to_crs='epsg:28992')

        # tranform from utm to wgs84
        wgs84 = pyproj.CRS('EPSG:4326')
        utm = pyproj.CRS('EPSG:28992')
        project = pyproj.Transformer.from_crs(utm, wgs84, always_xy=True).transform
        # add an edge attribute for time in minutes required to traverse each edge
        for age in walking_speed:
            for u, v, k, data in G.edges(data=True, keys=True):
                data['time'] = data['length'] / walking_speed[age]
        
        
        sql = "Select * from " + city + "." + city[0:3] + "_pop_2020_100"

        for trip_time in trip_times:
            print(trip_time)
            # population data
            gdf_pop_all = gpd.GeoDataFrame.from_postgis(sql, engine, geom_col='geometry')
            #gdf_pop_all = gdf_pop_all.head(10)
            gdf_list = np.array_split(gdf_pop_all,4)
            count=0
            for gdf_pop in gdf_list:
                count+=1
                print("Iteration: ", count)
                if count ==1 or count==3 or count==4:
                    continue
                # create centroids and project them to wgs84
                gdf_pop = gdf_pop.drop(gdf_pop[gdf_pop.geometry.geom_type=='MultiPolygon'].index)
                gdf_pop["centroid_wgs84"] = gdf_pop.apply(lambda row: transform(project, row["geometry"].centroid), axis=1)
                start_time = time.time()
                for age in walking_speed:
                    walking_speed_col_name = str(walking_speed[age]).replace(".","_")
                    print("Done calculating speeds. Generating Polygons....")
                    for index, row in gdf_pop.iterrows():
                        gdf_pop.loc[index,"iso_" + str(trip_time) +"_" + age + "_" + walking_speed_col_name] =  make_iso_polys(G, G_wgs84, gdf_pop.loc[index,'centroid_wgs84'], [trip_time], edge_buff=25, node_buff=0, infill=True)
                        # gdf_pop["iso_" + str(trip_time) +"_" + age + "_" + walking_speed_col_name] = gdf_pop.apply(lambda row: make_iso_polys(G, G_wgs84, row.centroid_wgs84, [trip_time], edge_buff=25, node_buff=0, infill=True), axis=1)
                print("DONE )--> iso_" + str(trip_time) +"_" + age + "_" + str(walking_speed[age]))
                gdf_pop.to_postgis("iso_population_2020_100_" + str(trip_time) + "_" + city[0:3] , con=engine, if_exists='append', chunksize=50, schema=city)
                print("Time needed --- %s seconds ---\n\n" % (time.time() - start_time))