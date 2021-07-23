from sqlalchemy import create_engine
import osmnx as ox
from config import db_connection_string


def collect_streets(lat_max, lat_min, lon_max, lon_min, new_columns, db_connection_string):
    g = ox.graph_from_bbox(lat_max, lat_min, lon_max, lon_min, network_type="all")
    nodes, edges = ox.graph_to_gdfs(g)
    edges = edges.reset_index()
    edges["id"] = edges["u"].astype(str) + "_" + edges['v'].astype(str) + "_" + edges["key"].astype(str)
    for new_col in new_columns:
        edges[new_col] = ""
    engine = create_engine(db_connection_string)
    edges.to_postgis("amsterdam_street_network", engine)


if __name__ == '__main__':
    # Amsterdaam bounding box
    lat_max, lat_min, lon_max, lon_min = 52.2787621079951990, 52.4305254996995984,\
                                         4.7398439999999997, 5.0685830000000003
    # new_columns = ["total_resources", "culture_resources", "sports_resources",
    #               "food_resources", "college_university_resources", "nightlife_resources",
    #                "outdoorsrecreation_resources" ]
    # collect_streets(lat_max, lat_min, lon_max, lon_min, new_columns, db_connection_string)