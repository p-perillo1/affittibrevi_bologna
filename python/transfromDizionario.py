import pandas as pd
import matplotlib.pyplot as plt
from extract import df_tourism, df_listings, df_reviews
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import numpy as np

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
    return df.rename(columns=str.lower).drop_duplicates().dropna(how="all", axis=1)

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

# 4. Regressione Polinomiale 
def apply_regression(df):
    if all(col in df.columns for col in ["anno", "mese", "numero"]):
        df['mese_num'] = df['mese'].map({
            'Gennaio': 1, 'Febbraio': 2, 'Marzo': 3, 'Aprile': 4, 'Maggio': 5, 'Giugno': 6,
            'Luglio': 7, 'Agosto': 8, 'Settembre': 9, 'Ottobre': 10, 'Novembre': 11, 'Dicembre': 12
        })

        df_filtered = df[df['anno'] >= 2023]
        X, y = df_filtered[['anno', 'mese_num']], df_filtered['numero']

        model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
        model.fit(X, y)

        r2 = model.score(X, y)
        print(f"R^2 (accuratezza del modello): {r2:.4f}")

        X_pred = pd.DataFrame([[2024, 12]], columns=['anno', 'mese_num'])
        y_pred = model.predict(X_pred)
        print(f"Numero stimato di turisti per dicembre 2024: {y_pred[0]:.2f}")

        # Aggiunta della previsione al dataset
        df = pd.concat([df, pd.DataFrame([{
            'anno': 2024, 'mese': 'Dicembre', 'mese_num': 12, 'numero': int(y_pred[0])
        }])])

        df = df.sort_values(by=['anno', 'mese_num'], ascending=[True, False])
        print(df.tail(12))

        plot_tourists_per_year(df, "Previsione Totale Turisti per Anno")
        
    return df  # Restituisce il DataFrame aggiornato

# Applica la regressione e aggiorna il dataframe

dfs["Tourism"] = apply_regression(dfs["Tourism"])

# Esporta i DataFrame trasformati
df_tourism_cleaned = dfs["Tourism"]
df_listings_cleaned = dfs["Listings"]
df_reviews_cleaned = dfs["Reviews"]
