import pandas as pd
import matplotlib.pyplot as plt
from extract import df_tourism, df_listings, df_reviews
from regressione_turisti_dicembre import apply_regression  # Importiamo la funzione dal file separato

# Dizionario per gestire i DataFrame
dfs = {
    "Tourism": df_tourism,
    "Listings": df_listings,
    "Reviews": df_reviews
}

# 1. Esplorazione dati
def explore_data(dfs):
    for name, df in dfs.items():
        print(f"\n=== {name} ===")
        print(df.head(), df.info(), df.describe())

explore_data(dfs)

# 2. Pulizia dati
def clean_data(df):
    df.columns = df.columns.str.strip()  # Rimuovi spazi bianchi dalle intestazioni
    df = df.rename(columns=str.lower)  # Converti le intestazioni in minuscolo
    df = df.drop_duplicates()  # Applica drop_duplicates
    df = df.dropna(how="all", axis=1)  # Applica dropna
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Converti la colonna date in datetime
    return df


# Pulisce i DataFrame nel dizionario
dfs = {name: clean_data(df) for name, df in dfs.items()}

# 3. Funzioni per visualizzazioni
def plot_avg_price(df, title="Prezzi Medi per Quartiere"):
    if "neighbourhood" in df.columns and "price" in df.columns:
        df.groupby('neighbourhood')['price'].mean().sort_values().plot(kind='barh', figsize=(8, 5), color='orange', edgecolor='black')
        plt.title(title)
        plt.xlabel("Prezzo (€)")
        plt.ylabel("Quartiere")
        plt.grid(True)
        plt.show()

def plot_tourists_per_year(df, title="Totale Turisti per Anno"):
    if "anno" in df.columns and "numero" in df.columns:
        df.groupby('anno')['numero'].sum().plot(kind='bar', figsize=(8, 5), color='green', edgecolor='black')
        plt.title(title)
        plt.xlabel("Anno")
        plt.ylabel("Numero di Turisti")
        plt.grid(True)
        plt.show()

# Applica le funzioni di visualizzazione in base ai dati disponibili
for name, df in dfs.items():
    if name == "Listings":
        plot_avg_price(df)
    elif name == "Tourism":
        plot_tourists_per_year(df)

# 4. Applicazione della regressione polinomiale
dfs["Tourism"] = apply_regression(dfs["Tourism"])

# Esporta i DataFrame trasformati
df_tourism_cleaned = dfs["Tourism"]
df_listings_cleaned = dfs["Listings"]
df_reviews_cleaned = dfs["Reviews"]

