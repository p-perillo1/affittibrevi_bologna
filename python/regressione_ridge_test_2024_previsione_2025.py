import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
import os
from dotenv import load_dotenv

# Caricamento dati
load_dotenv()
df = pd.read_csv(os.getenv("csv_prezzo_turisti_mensili"))
df['data'] = pd.to_datetime(df['anno'].astype(str) + '-' + df['mese'].astype(str).str.zfill(2) + '-01')
df = df[(df['anno'] >= 2022) & (df['anno'] <= 2023)]

# Feature engineering
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

df['mese_sin'] = np.sin(2 * np.pi * df['mese'] / 12)  # Codifica ciclica
df['mese_cos'] = np.cos(2 * np.pi * df['mese'] / 12)

# Preparazione dati
X = df[['anno', 'mese_sin', 'mese_cos']].values
y = df['prezzo_mensile'].values.reshape(-1, 1)

# Scaling corretto
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y).flatten()

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# Modello con Ridge Regression
model = Ridge(alpha=0.8)
model.fit(X_train, y_train)

# Valutazione
y_pred_scaled = model.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()

rmse = np.sqrt(mean_squared_error(y_test, y_pred_scaled))  # RMSE sui dati scalati
rmse_original = np.sqrt(mean_squared_error(scaler_y.inverse_transform(y_test.reshape(-1, 1)), 
                                           scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))))

print("\n" + "="*50)
print(f"R²: {r2_score(y_test, y_pred_scaled):.2f}")
print(f"MSE: {mean_squared_error(y_test, y_pred_scaled):.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"RMSE originale (in €): €{int(rmse_original):,.0f}".replace(',', '.'))
print("="*50 + "\n")

# Previsioni 2024-2025
future_months = pd.DataFrame({
    'anno': [2024]*12 + [2025]*12,
    'mese': list(range(1, 13)) * 2
})

# Applica lo stesso feature engineering ai dati futuri
future_months['mese_sin'] = np.sin(2 * np.pi * future_months['mese'] / 12)
future_months['mese_cos'] = np.cos(2 * np.pi * future_months['mese'] / 12)

X_future = future_months[['anno', 'mese_sin', 'mese_cos']].values
X_future_scaled = scaler_X.transform(X_future)
future_prices_scaled = model.predict(X_future_scaled)
future_prices = scaler_y.inverse_transform(future_prices_scaled.reshape(-1, 1)).flatten()

# Calcolo prezzi annuali
total_2024 = sum(future_prices[:12])
total_2025 = sum(future_prices[12:])

# Visualizzazione
plt.figure(figsize=(12, 6))
plt.scatter(df['data'], df['prezzo_mensile'], color='blue', label='Dati reali')
future_dates = pd.date_range(start="2024-01-01", periods=24, freq='ME')
plt.plot(future_dates, future_prices, color='red', linestyle='--', label='Previsioni')
plt.title("Confronto dati reali e previsioni (R² migliorato)")
plt.xlabel("Data")
plt.ylabel("Prezzo mensile")
plt.legend()
plt.grid(True)
plt.show()

print(f"Prezzo annuale previsto 2024: €{(total_2024):,.0f}".replace(',', '.'))
print(f"Prezzo annuale previsto 2025: €{(total_2025):,.0f}".replace(',', '.'))
