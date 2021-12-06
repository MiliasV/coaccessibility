from geoalchemy2 import Geometry, WKTElement
import geopandas as gpd
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import *
import pandas as pd
import psycopg2
import psycopg2.extras
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import *
from sqlalchemy.orm import Session

def get_col_from_db(c, cols, table):
    c.execute("SELECT " + cols + " from {table}" .format(table=table))
    return c.fetchall()

def get_col_from_db_first_rows(c, cols, table, count, order):
    c.execute("SELECT " + cols + " from {table} order by c28992r100 {order} limit {count}" .format(table=table, order=order, count=count))
    return c.fetchall()

def get_count_from_db(c, table):
    c.execute("select count(*) from {table}".format(table=table))
    return c.fetchall()


def create_neighbors_table(engine, table_name, metadata, schema):
    # if table does not exist
    # if not engine.dialect.has_table(engine, table_name, schema=schema):
        Table(table_name, metadata,
            Column("c28992r100", String, primary_key=True, nullable=False),
            Column("children", Numeric),
            Column("adults", Numeric),
            Column("elderly", Numeric),
            Column("children_perc", Numeric),
            Column("adults_perc", Numeric),
            Column("elderly_perc", Numeric),
            Column("total_pop", Numeric),schema=schema)
        metadata.create_all()


def setup_db(table_name, db_connection, schema):
    Base = automap_base()
    # Connect to the database
    db = create_engine(db_connection)
    # create object to manage table definitions
    metadata = MetaData(db)
    # create table if it doesn't exist - also define the table.
    create_neighbors_table(db, table_name, metadata,schema)
    # reflect the tables
    Base.prepare(db, schema=schema,reflect=True)
    myTable = getattr(Base.classes, table_name)
    # create a Session
    session = Session(db)
    return session, myTable


if __name__ == '__main__':
    for env in ['15']:
        for city_name in ['amsterdam']:
            print(city_name)
            print(env + '\n\n')
            conn = psycopg2.connect(dbname='age_segregation', host='localhost', user='postgres',password='postgres' )
            c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            db_connection_string = 'postgresql://postgres:postgres@localhost/age_segregation'
            engine = create_engine(db_connection_string)
            
            mapping_table = city_name + ".mapping_pop_with_neighbors_" + env + "_" + city_name[0:3]
            pop_table = city_name + "." + city_name[0:3] + "_pop_2020_100"
            to_store_table = 'pop_poi_based_neighbors_' + env + "_" + city_name[0:3]
            
            session, myTable = setup_db(to_store_table, db_connection_string, city_name)
            
            count = get_count_from_db(c, mapping_table)[0]['count']
            # break it in two if table is too big
            print("before reading map table")
            count_order = [(int(count/2),'asc'), (count - int(count/2),'desc')]
            for part in count_order:
                pop_squares = get_col_from_db_first_rows(c, 'c28992r100, neighbor_list', mapping_table, part[0], part[1])
                print("after reading map table")
                query = 'select c28992r100, pop."INW_014" as children,(pop."INW_1524" + pop."INW_2544" + pop."INW_4564") as adults, ' + \
                    '(pop."INW_65PL") as elderly,(pop."INW_014" + pop."INW_1524" + pop."INW_2544"+ pop."INW_4564"+ pop."INW_65PL")  as total_pop '+ \
                    'from {pop_table} as pop'.format(pop_table=pop_table)
                df_pop = pd.read_sql_query(query,con=engine)
            
                for pop in pop_squares:
                    data = {}
                    if pop["neighbor_list"]:
                        neigh_list = list(set(pop["neighbor_list"].split(",")))
                    else:
                        neigh_list=[]
                    df_res = df_pop[df_pop['c28992r100'].isin(neigh_list)].sum()
                    data["c28992r100"] = pop['c28992r100']
                    data["children"] = int(df_res.children)
                    data["adults"] = int(df_res.adults)
                    data["elderly"] = int(df_res.elderly)
                    data["total_pop"] = int(df_res.total_pop)
                    if  int(df_res.total_pop)!=0:
                        data["children_perc"] = int(df_res.children)/int(df_res.total_pop)
                        data["adults_perc"] = int(df_res.adults)/int(df_res.total_pop)
                        data["elderly_perc"] = int(df_res.elderly)/int(df_res.total_pop)
                    else:
                        data["children_perc"]=0
                        data["adults_perc"] = 0
                        data["elderly_perc"] = 0
                    session.add(myTable(**data))
                    session.commit()
