import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

server = 'hotels-database.database.windows.net,1433'
database = 'hotels-data'
username = 'shashank@hotels-database'
password = 'Snowy@123'
driver = 'ODBC Driver 17 for SQL Server'

params = urllib.parse.quote_plus(
    f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
)
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
