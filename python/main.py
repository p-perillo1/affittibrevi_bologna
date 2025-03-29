import extract  # Importa i dataframe da extract.py
import transform  # Importa i dataframe da transform.py
import load  # Importa i dati da load.py

print("Avvio del processo ETL...")

# Esegui la trasformazione dei dati
df_tourism_cleaned = transform.df_tourism_cleaned  # Usa il DataFrame già trasformato da transform.py
df_listings_cleaned = transform.df_listings_cleaned  # Usa il DataFrame già trasformato da transform.py
df_reviews_cleaned = transform.df_reviews_cleaned  # Usa il DataFrame già trasformato da transform.py

# Carica i dati nel database
load.load_to_db(df_tourism_cleaned, "tourism")
load.load_to_db(df_listings_cleaned, "listings")
load.load_to_db(df_reviews_cleaned, "reviews")

print("ETL completato")

