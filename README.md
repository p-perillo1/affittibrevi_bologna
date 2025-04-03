Descrizione del Progetto

Questo progetto si propone di analizzare il mercato degli affitti brevi a Bologna, utilizzando i dataset forniti da Airbnb e dal Comune di Bologna. L'obiettivo principale è analizzare l'andamento dei prezzi e del numero di turisti nel corso degli anni.

Sono stati utilizzati dati storici sui prezzi degli affitti brevi e sul numero di turisti per identificare le tendenze, le fluttuazioni e le eventuali correlazioni. Inoltre, sono state sviluppate tecniche di regressione per stimare i prezzi futuri, in particolare per il 2025, usando i dati del 2024 per testare i modelli.

Il progetto include la creazione di una dashboard interattiva in Power BI che visualizza l'andamento dei prezzi e dei turisti nel tempo.



Insight

La dashboard mostra l'andamento annuale e mensile dei prezzi degli affitti brevi a Bologna e il numero di turisti. Gli insight ottenuti dalle analisi mostrano una crescita continua dei prezzi in coincidenza con l'aumento dei turisti.

Picco dei prezzi: Maggio, luglio e ottobre.

Quartieri centrali: Prezzi medi più alti.

Quartieri periferici: Prezzi più bassi, ma con una crescita più rapida.


Funzionalità della Dashboard in Power BI

Prezzi per anno: Analisi dei prezzi totali degli affitti brevi per ogni anno.

Turisti per anno: Numero totale di turisti che hanno visitato Bologna ogni anno.

Prezzi e turisti per anno: Relazione tra i prezzi degli affitti brevi e il numero di turisti per anno.

Prezzi mese per mese per anno: Andamento dei prezzi mese per mese per ogni anno.

Prezzi medi per quartiere: Visualizzazione dei prezzi medi degli affitti brevi nei diversi quartieri di Bologna.

Variazione percentuale dei prezzi rispetto all'anno precedente: Analisi della variazione percentuale dei prezzi rispetto all'anno precedente.







---

Flusso di Lavoro

Il flusso di lavoro del progetto segue il framework PACE (Plan, Analyze, Construct, Execute), con un flusso ETL per l'estrazione, trasformazione e caricamento dei dati nel database.

1. Pianificazione (Plan)

Definizione degli obiettivi principali: visualizzare l'andamento dei prezzi e dei turisti nel tempo e prevedere i prezzi del 2025.

Scelta dei dataset.


2. Analisi (Analyze)

Analisi esplorativa dei dati (EDA).

Correzione delle problematiche nei dataset, come la mancanza dei dati di dicembre 2024.


3. Costruzione (Construct)

ETL (Extract, Transform, Load)

Extract: I dati sono stati estratti dai file CSV (Airbnb e turisti).

Transform: Pulizia e trasformazione dei dati, inclusa una regressione polinomiale per stimare i turisti mancanti di dicembre 2024.

Load: Caricamento dei dati trasformati in un database PostgreSQL utilizzando Supabase.

SQL: Creazione di tabelle aggregate per visualizzare il numero di turisti e il totale dei prezzi per anno e mese.


Calcolo dei Prezzi Annuali e Mensili

Poiché nei dati originali erano presenti solo il prezzo per notte, il numero di recensioni e il numero minimo di notti per ciascun alloggio, sono stati calcolati i prezzi annuali e mensili con le seguenti formule:

Prezzo annuale: prezzo per notte × numero di recensioni × numero minimo di notti

Prezzo mensile: prezzo annuale ÷ 12


Questi calcoli sono stati effettuati direttamente nel database PostgreSQL utilizzando query SQL.

Regressione Polinomiale e Lineare

Regressione polinomiale: Stima dei prezzi di dicembre 2024.

Regressione lineare: Previsione dei prezzi per il 2025.

Testing con Prophet: Verifica delle previsioni con il modello Prophet.


4. Esecuzione (Execute)

Caricamento dei dati in Power BI.

Creazione della dashboard interattiva.



---

Tecnologie Utilizzate

Python: Per la pulizia, trasformazione e analisi dei dati.

Pandas: Per la gestione dei dati.

scikit-learn: Per le regressioni.

Prophet: Per la previsione dei prezzi.

SQL: Per creare e gestire il database PostgreSQL.

Power BI: Per la visualizzazione dei dati.


Conclusioni

Il progetto fornisce un'analisi dettagliata degli affitti brevi a Bologna, con una particolare attenzione all'andamento dei prezzi e al numero di turisti.

Le regressioni hanno permesso di stimare il totale dei prezzi e il numero dei turisti per dicembre 2024 e prevedere i prezzi del 2025.

La dashboard interattiva in Power BI consente di esplorare le tendenze nel tempo e la relazione tra i prezzi e il numero di turisti.

Le stime sono indicative e basate sui dati storici disponibili.


⚠️ Questo progetto è stato realizzato a scopo didattico e di analisi.

