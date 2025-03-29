import pandas as pd
import matplotlib.pyplot as plt
from extract import df_tourism, df_listings, df_reviews


# 1. EDA - Esplorazione dati
for name, df in [("Tourism", df_tourism), ("Listings", df_listings), ("Reviews", df_reviews)]:
    print(f"{name} - Esempio:\n{df.head()}\nInformazioni:\n{df.info()}\nStatistiche:\n{df.describe()}\n")

# 3. Pulizia Dati
def clean_data(df):
    return df.rename(columns=str.lower).drop_duplicates().dropna(how="all", axis=1)

df_tourism_cleaned = clean_data(df_tourism)
df_listings_cleaned = clean_data(df_listings)
df_reviews_cleaned = clean_data(df_reviews)

# 4. Visualizzazioni
def plot_avg_price(df):
    df.groupby('neighbourhood')['price'].mean().sort_values().plot(kind='barh', figsize=(8, 5), color='orange', edgecolor='black')
    plt.title("Prezzi Medi per Quartiere")
    plt.xlabel("Prezzo (€)")
    plt.ylabel("Quartiere")
    plt.grid(True)
    plt.show()

print(df_reviews_cleaned.dtypes)
df_reviews_cleaned['date'] = pd.to_datetime(df_reviews_cleaned['date'])
def plot_reviews_per_year(df):
    # Raggruppa per anno direttamente con la colonna 'date' usando .dt.year
    df.groupby(df['date'].dt.year).size().plot(kind='bar', figsize=(8, 5), color='red', edgecolor='black')
    plt.title("Numero di Recensioni per Anno")
    plt.xlabel("Anno")
    plt.ylabel("Numero di Recensioni")
    plt.grid(True)
    plt.show()

def plot_tourists_per_year(df):
    df.groupby('anno')['numero'].sum().plot(kind='bar', figsize=(8, 5), color='green', edgecolor='black')
    plt.title("Totale Turisti per Anno")
    plt.xlabel("Anno")
    plt.ylabel("Numero di Turisti")
    plt.grid(True)
    plt.show()

plot_avg_price(df_listings_cleaned)
plot_reviews_per_year(df_reviews_cleaned)
plot_tourists_per_year(df_tourism_cleaned)



from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
import numpy as np


# Converti il mese in numerico
df_tourism_cleaned['mese_num'] = df_tourism_cleaned['mese'].map({
    'Gennaio': 1, 'Febbraio': 2, 'Marzo': 3, 'Aprile': 4, 'Maggio': 5, 'Giugno': 6,
    'Luglio': 7, 'Agosto': 8, 'Settembre': 9, 'Ottobre': 10, 'Novembre': 11, 'Dicembre': 12
})

# Filtra solo ottobre, novembre e dicembre dal 2019 a novembre 2024, escludendo dicembre 2024
df_filtered = df_tourism_cleaned[
    (df_tourism_cleaned['anno'] >= 2022) & 
    (df_tourism_cleaned['mese'].isin(['Ottobre', 'Novembre', 'Dicembre']))]

# Definisci variabili indipendenti (X) e dipendente (y)
X = df_filtered[['anno', 'mese_num']]
y = df_filtered['numero']

# Crea un modello di regressione polinomiale di grado 3
model = make_pipeline(PolynomialFeatures(degree=3), LinearRegression())
model.fit(X, y)

# Calcola R^2
r2 = model.score(X, y)
print(f"R^2 (accuratezza del modello): {r2:.4f}")

# Previsione per dicembre 2024
X_pred = np.array([[2024, 12]])
y_pred = model.predict(X_pred)
print(f"Numero stimato di turisti per dicembre 2024: {y_pred[0]:.2f}")

# Grafico della regressione
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X['anno'], X['mese_num'], y, color='blue', label='Dati reali')

# Creazione della griglia per la superficie del modello
anno_range = np.linspace(X['anno'].min(), X['anno'].max(), 30)
mese_range = np.linspace(X['mese_num'].min(), X['mese_num'].max(), 3)
anno_grid, mese_grid = np.meshgrid(anno_range, mese_range)
X_grid = np.column_stack([anno_grid.ravel(), mese_grid.ravel()])
y_grid_pred = model.predict(X_grid).reshape(anno_grid.shape)

# Plotta la superficie della regressione
ax.plot_surface(anno_grid, mese_grid, y_grid_pred, color='red', alpha=0.5)
ax.set_xlabel('Anno')
ax.set_ylabel('Mese')
ax.set_zlabel('Numero di turisti')
ax.set_title('Regressione Polinomiale su Anno e Mese')
plt.legend()
plt.show()




# 6. Creare un DataFrame per la stima di Dicembre 2024
stima_dicembre_2024_df = pd.DataFrame([{
    'anno': 2024,
    'mese': 'Dicembre',
    'mese_num': 12,
    'numero': int(y_pred[0])  # Estrai il primo valore di y_pred e poi convertilo in int
}])

# Concatenare la stima di dicembre 2024 al DataFrame
df_tourism_cleaned = pd.concat([df_tourism_cleaned, stima_dicembre_2024_df])

# Ordinare per anno e mese in ordine cronologico
# Definiamo l'ordine dei mesi in italiano
ordine_mesi = ['Dicembre', 'Novembre', 'Ottobre', 'Settembre', 
               'Agosto', 'Luglio', 'Giugno', 'Maggio', 'Aprile', 
               'Marzo', 'Febbraio', 'Gennaio']
df_tourism_cleaned['mese'] = pd.Categorical(df_tourism_cleaned['mese'], categories=ordine_mesi, ordered=True)
df_tourism_cleaned = df_tourism_cleaned.sort_values(by=['anno', 'mese'])
df_tourism_cleaned.reset_index(drop=True, inplace=True)

# Visualizzare gli ultimi 12 mesi
print(df_tourism_cleaned.tail(12))

# Visualizzare il grafico dei turisti per anno, includendo la previsione di dicembre 2024
plot_tourists_per_year(df_tourism_cleaned)
