import pandas as pd
import matplotlib.pyplot as plt
from extract import df_tourism, df_listings, df_reviews
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import numpy as np

# 1. EDA - Esplorazione dati
for name, df in [("Tourism", df_tourism), ("Listings", df_listings), ("Reviews", df_reviews)]:
    print(f"{name} - Esempio:\n{df.head()}\nInformazioni:\n{df.info()}\nStatistiche:\n{df.describe()}\n")

# 2. Pulizia Dati
def clean_data(df):
    return df.rename(columns=str.lower).drop_duplicates().dropna(how="all", axis=1)

df_tourism_cleaned = clean_data(df_tourism)
df_listings_cleaned = clean_data(df_listings)
df_reviews_cleaned = clean_data(df_reviews)


# 3. Visualizzazioni
def plot_avg_price(df):
    df.groupby('neighbourhood')['price'].mean().sort_values().plot(kind='barh', figsize=(8, 5), color='orange', edgecolor='black')
    plt.title("Prezzi Medi per Quartiere")
    plt.xlabel("Prezzo (€)")
    plt.ylabel("Quartiere")
    plt.grid(True)
    plt.show()


def plot_tourists_per_year(df):
    df.groupby('anno')['numero'].sum().plot(kind='bar', figsize=(8, 5), color='green', edgecolor='black')
    plt.title("Totale Turisti per Anno")
    plt.xlabel("Anno")
    plt.ylabel("Numero di Turisti")
    plt.grid(True)
    plt.show()

plot_avg_price(df_listings)
plot_tourists_per_year(df_tourism_cleaned)

# 4. Regressione Polinomiale
df_tourism_cleaned['mese_num'] = df_tourism_cleaned['mese'].map({
    'Gennaio': 1, 'Febbraio': 2, 'Marzo': 3, 'Aprile': 4, 'Maggio': 5, 'Giugno': 6,
    'Luglio': 7, 'Agosto': 8, 'Settembre': 9, 'Ottobre': 10, 'Novembre': 11, 'Dicembre': 12
})

# Filtra i dati per ottobre, novembre e dicembre dal 2019 a novembre 2024
df_filtered = df_tourism_cleaned[(df_tourism_cleaned['anno'] >= 2023)]

# Definisci variabili indipendenti (X) e dipendente (y)
X = df_filtered[['anno', 'mese_num']]
y = df_filtered['numero']

# Crea e allena il modello
model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
model.fit(X, y)

# Calcola R^2
r2 = model.score(X, y)
print(f"R^2 (accuratezza del modello): {r2:.4f}")

# Previsione per dicembre 2024
X_pred = pd.DataFrame([[2024, 12]], columns=['anno', 'mese_num'])
y_pred = model.predict(X_pred)
print(f"Numero stimato di turisti per dicembre 2024: {y_pred[0]:.2f}")

# 5. Aggiungi la previsione di dicembre 2024 al DataFrame
stima_dicembre_2024_df = pd.DataFrame([{
    'anno': 2024,
    'mese': 'Dicembre',
    'mese_num': 12,
    'numero': int(y_pred[0])
}])

df_tourism_cleaned = pd.concat([df_tourism_cleaned, stima_dicembre_2024_df])

# Ordinare per anno in ordine crescente e mese_num in ordine decrescente
df_tourism_cleaned = df_tourism_cleaned.sort_values(by=['anno', 'mese_num'], ascending=[True, False])

# Visualizzare gli ultimi 12 mesi
print(df_tourism_cleaned.tail(12))

# Visualizzare il grafico dei turisti per anno, includendo la previsione di dicembre 2024
plot_tourists_per_year(df_tourism_cleaned)
