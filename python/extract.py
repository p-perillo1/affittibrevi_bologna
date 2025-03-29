import pandas as pd  # Libreria per lavorare con i DataFrame
import os  # Libreria per interagire con il sistema operativo
from dotenv import load_dotenv  # Permette di caricare le variabili dal file .env

# Carica le variabili d'ambiente dal file .env
load_dotenv()


# Legge i file CSV usando i percorsi definiti nel .env
df_tourism = pd.read_csv(os.getenv("csv_tourism"),sep= ";")
df_listings = pd.read_csv(os.getenv("csv_listings"))
df_reviews = pd.read_csv(os.getenv("csv_reviews"))

# Stampa le prime righe per verificare il caricamento corretto
print("Dati Turismo:", df_tourism.head(), sep="\n")
print("Dati Listings:", df_listings.head(), sep="\n")
print("Dati Reviews:", df_reviews.head(), sep="\n")



