import os
from dotenv import load_dotenv
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
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


df_filtered = df[(df['anno'] >= 2019) & ~((df['anno'] == 2024) & (df['mese'] == 12))]

X, y = df_filtered[['anno', 'mese', 'turisti_mensili']], df_filtered['prezzo_mensile']

# Scaling Min-Max (0-1)
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()

# Suddivisione in Training (80%) e Test (20%)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# Creazione e addestramento del modello
model = make_pipeline(PolynomialFeatures(degree=2, include_bias=False), LinearRegression())
model.fit(X_train, y_train)

# Creiamo il dato per Dicembre 2024
X_pred = scaler_X.transform([[2024, 12, 136794]])
y_pred_scaled = model.predict(X_pred)
y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))[0, 0]

# Previsione
previsione_dicembre_2024 = float(y_pred)  # Converti in float nativo di Python

# Calcoliamo MSE e R² per valutare il modello
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)
mse_train = mean_squared_error(y_train, y_pred_train)
mse_test = mean_squared_error(y_test, y_pred_test)
r2_train = model.score(X_train, y_train)
r2_test = model.score(X_test, y_test)

# Descalare le previsioni
y_pred_train_descaled = scaler_y.inverse_transform(y_pred_train.reshape(-1, 1)).flatten()
y_pred_test_descaled = scaler_y.inverse_transform(y_pred_test.reshape(-1, 1)).flatten()

# Calcolare MSE sui dati originali (descalati)
mse_train_descaled = mean_squared_error(scaler_y.inverse_transform(y_train.reshape(-1, 1)).flatten(), y_pred_train_descaled)
mse_test_descaled = mean_squared_error(scaler_y.inverse_transform(y_test.reshape(-1, 1)).flatten(), y_pred_test_descaled)

# Calcolare RMSE sui dati originali
rmse_train_descaled = np.sqrt(mse_train_descaled)
rmse_test_descaled = np.sqrt(mse_test_descaled)

# Risultati
print(f"Stima del prezzo per Dicembre 2024: {previsione_dicembre_2024:.2f}")
print(f"R² Score (Training): {r2_train:.4f}")
print(f"R² Score (Test): {r2_test:.4f}")
print(f"MSE (Training): {mse_train:.4f}")
print(f"MSE (Test): {mse_test:.4f}")
print(f"RMSE (Training, descalato): {rmse_train_descaled:.4f}")
print(f"RMSE (Test, descalato): {rmse_test_descaled:.4f}")





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
    'mese': 12
}

# Esegui la query con gestione degli errori
# Esegui la query con gestione degli errori

with engine.begin() as connection:  # Usa engine.begin() per gestire automaticamente la transazione
    connection.execute(query, params)
    print("Dati aggiornati con successo per Dicembre 2024")





