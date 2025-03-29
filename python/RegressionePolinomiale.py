import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import os
from dotenv import load_dotenv

# Caricare le variabili d'ambiente
# Qui carichiamo le variabili d'ambiente, che potrebbero contenere percorsi o altre informazioni sensibili.
load_dotenv()

# Percorso del file CSV
# Otteniamo il percorso del file CSV dalle variabili d'ambiente.
# Assicurati che nella tua variabile d'ambiente "csv_prezzo_turisti_annuali" ci sia il percorso corretto.
env_path = os.getenv("csv_prezzo_turisti_annuali")


# Caricare i dati
# Usa pandas per leggere il file CSV. Sostituisci "env_path" con il percorso corretto se non usi le variabili d'ambiente.
df = pd.read_csv(env_path)

# Assumiamo che le colonne si chiamino 'anno' e 'prezzi_annuali'.
# Se i nomi delle colonne nel tuo CSV sono diversi, aggiorna qui le variabili 'X' e 'y'.
X = df[['anno']].values  # 'anno' è la feature indipendente (i dati da cui il modello impara).
y = df['prezzi_annuali'].values  # 'prezzi_annuali' è la variabile dipendente (quello che vogliamo prevedere).

# Regressione polinomiale di secondo grado
degree = 2  # Definiamo il grado del polinomio. Puoi cambiarlo se vuoi usare un polinomio di grado diverso.
model_poly = make_pipeline(PolynomialFeatures(degree), LinearRegression())  # Creiamo una pipeline che applica il polinomio e la regressione lineare.
model_poly.fit(X, y)  # Alleniamo il modello sui dati.

# Fare previsioni per i prossimi 5 anni
# Questo calcola la previsione per i prossimi 5 anni partendo dall'anno più recente nei dati.
future_years = np.array([[year] for year in range(df['anno'].max() + 1, df['anno'].max() + 6)])
future_prices_poly = model_poly.predict(future_years)

# Valutazione del modello polinomiale
# Calcoliamo il punteggio R², che ci dice quanto bene il modello si adatta ai dati.
r2_poly = r2_score(y, model_poly.predict(X))
print(f"R² Score (Polinomiale): {r2_poly:.4f}")  # Mostriamo il punteggio R².

# Calcolare l'incremento previsto tra l'ultimo anno e il primo anno futuro
# L'incremento previsto è la differenza tra il prezzo previsto per il prossimo anno e l'ultimo prezzo conosciuto.
incremento_previsione_poly = future_prices_poly[0] - y[-1]
print(f"L'incremento previsto nei prossimi 5 anni rispetto all'ultimo anno è: {incremento_previsione_poly:.2f}")

# Visualizzazione dei risultati
plt.figure(figsize=(10,6))  # Creiamo una figura per il grafico.

# Dati reali
plt.scatter(X, y, color='blue', label='Dati reali')  # Visualizza i dati reali come punti blu.

# Regressione polinomiale
plt.plot(X, model_poly.predict(X), color='orange', label='Regressione polinomiale')  # Visualizza la linea di regressione polinomiale.

# Previsioni future
plt.plot(future_years, future_prices_poly, color='purple', linestyle='dashed', label='Previsione Polinomiale')  # Visualizza la previsione per i prossimi 5 anni con una linea tratteggiata.

# Annotazione per l'incremento
# Aggiungiamo un'annotazione che mostra l'incremento previsto nei prossimi 5 anni.
plt.annotate(f"Incremento: {incremento_previsione_poly:.2f}", 
             xy=(future_years[0], future_prices_poly[0]), 
             xytext=(future_years[0] + 1, future_prices_poly[0] - 1000),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.xlabel("Anno")  # Etichetta dell'asse x
plt.ylabel("Prezzi annuali")  # Etichetta dell'asse y
plt.legend()  # Mostra la legenda
plt.title("Regressione Polinomiale con Previsioni")  # Titolo del grafico
plt.show()  # Mostra il grafico.

# Visualizzazione dei residui
# I residui sono la differenza tra i valori reali e quelli previsti dal modello.
# Mostriamo un grafico dei residui per verificare se il modello è stato adattato correttamente.
residuals_poly = y - model_poly.predict(X)
plt.figure(figsize=(10,6))
plt.scatter(X, residuals_poly)
plt.title("Residui della Regressione Polinomiale")  # Titolo del grafico dei residui
plt.xlabel("Anno")  # Etichetta dell'asse x
plt.ylabel("Residuo")  # Etichetta dell'asse y
plt.show()  # Mostra il grafico dei residui.

