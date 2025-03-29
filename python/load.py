import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Carica le credianziali del mio databse supabase
load_dotenv()

"""Carica un dataframe in una tabella PostgreSQL usando SQLAlchemy"""
def load_to_db(df, table_name):
    
    engine = create_engine(
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    
    df.to_sql(table_name, engine, if_exists='append', index=False)
    
    print(f"Dati caricati con successo nella tabella {table_name}")
