from sqlalchemy.ext.automap import automap_base
from geoalchemy2 import Geometry
from sqlalchemy import *
from sqlalchemy.orm import Session
import psycopg2
import psycopg2.extras
from config import params, db_connection_string
import time


def create_poi_ages_table(engine, table_name, metadata):
    # if table does not exist
    if not engine.dialect.has_table(engine, table_name):
        Table(table_name, metadata,
              Column("fsq_id", String, primary_key=True, nullable=False),
              Column("INW_014", Numeric),
              Column("INW_1524", Numeric),
              Column("INW_2544", Numeric),
              Column("INW_4564", Numeric),
              Column("INW_65PL", Numeric))
        metadata.create_all()


def create_place_isochrones_table(engine, table_name, metadata, place_id):
    # if table does not exist
    if not engine.dialect.has_table(engine, table_name):
        Table(table_name, metadata,
            Column("id", String, primary_key=True, nullable=False),
            Column("c28992r100", String),
            Column(place_id, String))
        metadata.create_all()


def setup_db(pois_table_name, db_connection, table_type):
    Base = automap_base()
    # Connect to the database
    db = create_engine(db_connection)
    # create object to manage table definitions
    metadata = MetaData(db)
    # create table if it doesn't exist - also define the table.
    if table_type == "fsq_age":
        create_poi_ages_table(db, pois_table_name, metadata)
    else:
        create_place_isochrones_table(db, pois_table_name, metadata, table_type)
    # reflect the tables
    Base.prepare(db, reflect=True)
    Table = getattr(Base.classes, pois_table_name)
    # create a Session
    session = Session(db)
    return session, Table

def insert_poi_polygon_to_db(conn, c, data , table, id_col):
    sql = "INSERT INTO " + table + " (id, " + id_col + ", c28992r100 ) VALUES (%s, %s, %s)"
    c.execute(sql, (data["id"], data[id_col], data["c28992r100"]))
    conn.commit()


def get_col_from_db(c, cols, table, id_col, max_added_id):
    c.execute("SELECT " + cols + " from {table}  where {id_col}>'{max_added_id}' order by {id_col}"
              .format(table=table, id_col=id_col, max_added_id=max_added_id))
    return c.fetchall()


def get_place_that_interesect_with_polygon(c, table_poi, table_pop,  poly_col, poly_id_col, poly_id):
    c.execute('SELECT {poly_id_col}, id FROM {table_poi} place '
              ' INNER JOIN {table_pop} pop '
              ' ON ST_Intersects(place.geom, ST_Transform(ST_GEOMFROMTEXT(pop.{poly_col}, 28992),4326)) '
              " where pop.{poly_id_col}='{poly_id}'".format(table_poi=table_poi, table_pop=table_pop,
                                                          poly_col = poly_col, poly_id_col = poly_id_col,
                                                          poly_id = poly_id))
    return c.fetchall()


def get_ages_count_per_poi(c, table_poi, table_pop, fsq_id):
    c.execute('SELECT  sum(pop."INW_014") as INW_014,  sum(pop."INW_1524") as INW_1524,  '
              'sum(pop."INW_2544") as INW_2544,  '
              'sum(pop."INW_4564") as INW_4564,  sum(pop."INW_65PL") as INW_65PL FROM {table_poi} fsq '
              ' INNER JOIN {table_pop} pop '
              ' ON ST_Intersects(fsq.geom, ST_Transform(ST_GEOMFROMTEXT(pop."iso_15_1524_80.4", 28992),4326)) '
              " where fsq.id='{fsq_id}'".format(table_poi=table_poi, table_pop=table_pop, fsq_id=fsq_id))
    return c.fetchall()[0]


def insert_data(session, Table, data):
    try:
        session.add(
            Table(**data))
        session.commit()
        print("~~  INSERTED!")
    except Exception as err:
        session.rollback()
        print("# NOT INSERTED: ", err)


if __name__ == '__main__':
    conn = psycopg2.connect(**params)
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # id column name of population data
    pop_id_col = 'c28992r100'
    pop_table = 'pop_ams_with_iso'
    isochrone_cols = '"iso_15_014_75","iso_15_2544_80_4","iso_15_65PL_72_6"'

    place_table = 'fsq_ams_whole_40_msc_typel1'
    # place_table = 'park_ams_all'
    id_col = 'fsq_id'
    # place_table = 'squares_ams_all'

    # create table if it doesn't exist
    to_store_table ='fsq_ams_iso_mapping'
    session, Table = setup_db(to_store_table, db_connection_string, id_col)

    # get all pois or isochrones
    # max_added_id =  'E1213N4861'
    max_added_id = ''

    pop_isochrones = get_col_from_db(c, pop_id_col + ',' + isochrone_cols, pop_table, pop_id_col, max_added_id)
    # calculate intersections -> places - isochrones
    for pop_square in pop_isochrones:
        data = {}
        start_time = time.time()
        print("Calculating --> " + pop_square[pop_id_col])
        results = get_place_that_interesect_with_polygon(c, place_table, pop_table, "iso_15_014_75", pop_id_col, pop_square[pop_id_col])
        # print("Time to get query results --- %s seconds ---" % (time.time() - start_time))
        count = 0
        if not results:
            data["c28992r100"] = pop_square[pop_id_col]
            data[id_col] = "None"
            data["id"] = pop_square[pop_id_col]
            session.add(Table(**data))

        for res in results:
            # print(res)
            # start_time = time.time()
            data["c28992r100"] = res["c28992r100"]
            data[id_col] = res["id"]
            data["id"] = data["c28992r100"] + "_" + str(data[id_col])
            # insert_poi_polygon_to_db(conn, c, data, to_store_table, id_col)
            session.add(Table(**data))
            # print("Time to get add one record  --- %s seconds ---" % (time.time() - start_time))

        # print("Time to get add to session --- %s seconds ---" % (time.time() - start_time))
        # start_time = time.time()
        count += 1
        session.commit()
        print("~~  INSERTED - " + str(count))
        print("Time needed  --- %s seconds ---" % (time.time() - start_time))







