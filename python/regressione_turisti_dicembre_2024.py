import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt

def apply_regression(df_tourism):
    if all(col in df_tourism.columns for col in ["anno", "mese", "numero"]):
        df_tourism['mese_num'] = df_tourism['mese'].map({
            'Gennaio': 1, 'Febbraio': 2, 'Marzo': 3, 'Aprile': 4, 'Maggio': 5, 'Giugno': 6,
            'Luglio': 7, 'Agosto': 8, 'Settembre': 9, 'Ottobre': 10, 'Novembre': 11, 'Dicembre': 12
        })

        # Escludere dicembre 2024 dai dati di addestramento
        df_filtered = df_tourism[(df_tourism['anno'] >= 2021) & ~((df_tourism['anno'] == 2024) & (df_tourism['mese_num'] == 12))]
        X, y = df_filtered[['anno', 'mese_num']], df_filtered['numero']

        # Scaling Min-Max (0-1)
        scaler_X = MinMaxScaler()
        scaler_y = MinMaxScaler()
        X_scaled = scaler_X.fit_transform(X)
        y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()

        # Suddivisione in Training (70%) e Test (30%)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.3, random_state=42)

        # Modello di regressione polinomiale
        model = make_pipeline(PolynomialFeatures(degree=2, include_bias=False), LinearRegression())
        model.fit(X_train, y_train)

        # Valutazione del modello
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        mse_train = mean_squared_error(y_train, y_train_pred)
        mse_test = mean_squared_error(y_test, y_test_pred)
        rmse_train = sqrt(mse_train)  # RMSE su dati normalizzati
        rmse_test = sqrt(mse_test)    # RMSE su dati normalizzati
        r2_test = model.score(X_test, y_test)

        # Trasformazione inversa per riportare i valori predetti nella scala originale
        y_train_pred_original = scaler_y.inverse_transform(y_train_pred.reshape(-1, 1)).flatten()
        y_test_pred_original = scaler_y.inverse_transform(y_test_pred.reshape(-1, 1)).flatten()
        y_train_original = scaler_y.inverse_transform(y_train.reshape(-1, 1)).flatten()
        y_test_original = scaler_y.inverse_transform(y_test.reshape(-1, 1)).flatten()

        # Calcolo dell'RMSE nella scala originale
        rmse_train_original = sqrt(mean_squared_error(y_train_original, y_train_pred_original))
        rmse_test_original = sqrt(mean_squared_error(y_test_original, y_test_pred_original))

        print(f"MSE Training Set: {mse_train:.4f}")
        print(f"RMSE Training Set (Normalizzato): {rmse_train:.4f}")
        print(f"RMSE Training Set (Scala Originale): {rmse_train_original:.4f}")  # RMSE nella scala originale
        print(f"MSE Test Set: {mse_test:.4f}")
        print(f"RMSE Test Set (Normalizzato): {rmse_test:.4f}")
        print(f"RMSE Test Set (Scala Originale): {rmse_test_original:.4f}")    # RMSE nella scala originale
        print(f"R^2 Test Set: {r2_test:.4f}")

        # Previsione per dicembre 2024
        X_pred = scaler_X.transform([[2024, 12]])
        y_pred_scaled = model.predict(X_pred)
        y_pred = scaler_y.inverse_transform([[y_pred_scaled[0]]])[0][0]

        valore_reale = df_tourism[(df_tourism['anno'] == 2024) & (df_tourism['mese_num'] == 12)]['numero'].values
        if valore_reale.size > 0:
            print(f"Numero reale di turisti per dicembre 2024: {valore_reale[0]}")
        print(f"Numero stimato di turisti per dicembre 2024: {y_pred:.2f}")

        # Aggiungiunta della previsione al dataframe
        df_tourism = pd.concat([df_tourism, pd.DataFrame([{
            'anno': 2024, 'mese': 'Dicembre', 'mese_num': 12, 'numero': int(y_pred)
        }])])

        # Ordinamento dei dati per anno e mese
        df_tourism = df_tourism.sort_values(by=['anno', 'mese_num'], ascending=[True, False])

        print(df_tourism.tail(12))  # Visualizziamo gli ultimi 12 record
        
        plot_regression_line(X_scaled, y_scaled, model)
        plot_tourists_per_year(df_tourism)
    
    return df_tourism

def plot_regression_line(X, y, model):
    X_range = np.linspace(0, 1, 100).reshape(-1, 1)
    X_mese = np.tile(np.linspace(0, 1, 12), len(X_range)).reshape(-1, 1)
    X_range_final = np.column_stack([np.repeat(X_range, 12), X_mese])
    y_pred_range = model.predict(X_range_final)
    
    plt.figure(figsize=(8, 5))
    plt.scatter(X[:, 0], y, color='blue', label='Dati Originali')
    y_pred_annual = [np.mean(y_pred_range[i*12:(i+1)*12]) for i in range(len(X_range))]
    plt.plot(X_range, y_pred_annual, color='red', label='Curva di Regressione')
    plt.title("Curva di Regressione Polinomiale")
    plt.xlabel("Anno (Normalizzato)")
    plt.ylabel("Numero di Turisti (Normalizzato)")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_tourists_per_year(df):
    df.groupby('anno')['numero'].sum().plot(kind='bar', figsize=(8, 5), color='green', edgecolor='black')
    plt.title("Totale Turisti per Anno")
    plt.xlabel("Anno")
    plt.ylabel("Numero di Turisti")
    plt.grid(True)
    plt.show()



