import geopandas as gpd
from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKTElement


db_connection_string = 'postgresql://postgres:postgres@localhost/age_segregation'
engine = create_engine(db_connection_string)
# read file
gdf = gpd.read_file("/data/age_accessibility_data/data/WijkBuurtkaart_2021_v0/SHP/CBS_buurten2021.shp")
#gdf_ams = gdf.loc[gdf["GM_NAAM"]=='Amsterdam']
#gdf_rot = gdf.loc[gdf["GM_NAAM"]=='Rotterdam']
#gdf_utr = gdf.loc[gdf["GM_NAAM"]=='Utrecht']
#gdf_hag = gdf.loc[gdf["GM_NAAM"]=="'s-Gravenhage"]
gdf_ein = gdf.loc[gdf["GM_NAAM"]=='Eindhoven']

# store the results to a postgres db
gdf_ein.to_postgis("pop_2020_100_buurt_ein", con=engine, schema='eindhoven')
