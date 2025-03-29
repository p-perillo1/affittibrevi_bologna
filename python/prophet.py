import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import os
from dotenv import load_dotenv

# Caricamento dati
load_dotenv()
df = pd.read_csv(os.getenv("csv_prezzo_turisti_mensili"))
df['data'] = pd.to_datetime(df['anno'].astype(str) + '-' + df['mese'].astype(str).str.zfill(2) + '-01')
df = df[(df['anno'] >= 2022) & (df['anno'] <= 2023)]

# Preparazione dei dati per Prophet
df_prophet = df[['data', 'prezzo_mensile']].rename(columns={'data': 'ds', 'prezzo_mensile': 'y'})

# Crea e addestra il modello Prophet
prophet_model = Prophet(yearly_seasonality=True)  # Forza la stagionalità annuale
prophet_model.fit(df_prophet)

# Creazione del dataframe per le previsioni (24 mesi futuri)
future_prophet = prophet_model.make_future_dataframe(periods=24, freq='M')

# Previsione dei dati futuri
forecast_prophet = prophet_model.predict(future_prophet)

# Visualizzazione dei dati reali e delle previsioni
plt.figure(figsize=(12, 6))
plt.plot(df_prophet['ds'], df_prophet['y'], label='Dati reali', color='blue')
plt.plot(forecast_prophet['ds'], forecast_prophet['yhat'], label='Previsioni Prophet', color='green', linestyle='--')
plt.fill_between(forecast_prophet['ds'], forecast_prophet['yhat_lower'], forecast_prophet['yhat_upper'], 
                 color='green', alpha=0.3, label='Intervallo di confidenza')
plt.title("Confronto dati reali e previsioni (Prophet)")
plt.xlabel("Data")
plt.ylabel("Prezzo mensile")
plt.legend()
plt.grid(True)
plt.show()

# Calcolo dei prezzi annuali previsti
total_2024_prophet = forecast_prophet[forecast_prophet['ds'].dt.year == 2024]['yhat'].sum()
total_2025_prophet = forecast_prophet[forecast_prophet['ds'].dt.year == 2025]['yhat'].sum()

print(f"Prezzo annuale previsto 2024 (Prophet): €{total_2024_prophet:,.0f}")
print(f"Prezzo annuale previsto 2025 (Prophet): €{total_2025_prophet:,.0f}")
