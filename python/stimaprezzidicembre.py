import os
from dotenv import load_dotenv
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import numpy as np

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Crea l'engine di SQLAlchemy
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Importa la tabella prezzo_turisti_mensili
df = pd.read_sql_table("prezzo_turisti_mensili", con=engine)

# Visualizza le prime righe per capire come sono strutturati i dati
print(df.head())

# Mappa i nomi dei mesi in numeri
month_map = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

# Aggiungi una colonna 'mese_num' che converte il mese da stringa a numero
df['mese_num'] = df['mese'].map(month_map)

# Caricare il DataFrame (assumiamo che sia già disponibile come df)
df_filtered = df[(df['mese'].isin(['November', 'December'])) & (df['anno'] < 2024)]

# Variabili indipendenti (X) e dipendenti (y)
X = df_filtered[['anno', 'turisti_mensili']]
y = df_filtered['prezzo_mensile']

# Trasformazione polinomiale (proviamo con grado 2)
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)

# Creazione e addestramento del modello
model = LinearRegression()
model.fit(X_poly, y)

# Creiamo il dato per Dicembre 2024
X_pred = np.array([[2024, 148015]])  # Anno 2024 e turisti_mensili previsti
X_pred_poly = poly.transform(X_pred)

# Previsione
previsione_dicembre_2024 = model.predict(X_pred_poly)[0]

# Calcoliamo MSE e R² per valutare il modello
y_pred_train = model.predict(X_poly)
mse = mean_squared_error(y, y_pred_train)
r2 = model.score(X_poly, y)

print(f"Stima del prezzo per Dicembre 2024: {previsione_dicembre_2024:.2f}")
print(f"R² Score: {r2:.4f}")


# Converti il valore previsto in un tipo float nativo di Python
previsione_dicembre_2024 = int(previsione_dicembre_2024)

# Crea la query SQL con segnaposti
query = text("""
    UPDATE prezzo_turisti_mensili
    SET prezzo_mensile = :prezzo_mensile
    WHERE anno = :anno AND mese = :mese
""")

# Parametri da passare come dizionario
params = {
    'prezzo_mensile': previsione_dicembre_2024,
    'anno': 2024,
    'mese': 'December'
}

# Esegui la query con gestione degli errori
# Esegui la query con gestione degli errori

with engine.begin() as connection:  # Usa engine.begin() per gestire automaticamente la transazione
    connection.execute(query, params)
    print("Dati aggiornati con successo per Dicembre 2024")


