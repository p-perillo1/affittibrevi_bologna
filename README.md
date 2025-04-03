Descrizione del Progetto

Questo progetto si propone di analizzare il mercato degli affitti brevi a Bologna, utilizzando i dataset forniti da Airbnb e dal Comune di Bologna. L'obiettivo principale è analizzare l'andamento dei prezzi e del numero di turisti nel corso degli anni.  
Sono stati utilizzati dati storici sui prezzi degli affitti brevi e sul numero di turisti per identificare le tendenze, le fluttuazioni e le eventuali correlazioni. Inoltre, sono state sviluppate tecniche di regressione per stimare i prezzi futuri, in particolare per il 2025, usando i dati del 2024 per testare i modelli.
Il progetto include la creazione di una dashboard interattiva in Power BI che visualizza l'andamento dei prezzi e dei turisti nel tempo.

![Screenshot 2025-04-04 003614](https://github.com/user-attachments/assets/5fd06c62-c5bb-4287-8767-cb30b31604ee)


Insight:
La dashboard mostra l'andamento annuale e mensile dei prezzi degli affitti brevi a Bologna e il numero di turisti. Gli insight ottenuti dalle analisi mostrano una crescita continua dei prezzi in coincidenza con l'aumento dei turisti.

È stato osservato un picco nei prezzi degli affitti brevi durante i mesi di maggio, luglio e ottobre.

I quartieri centrali tendono ad avere prezzi medi più alti, mentre i quartieri periferici offrono tariffe più basse, ma con una crescita più rapida nei prezzi.

Funzionalità della Dashboard in Power BI

La dashboard fornisce le seguenti visualizzazioni:
    • Prezzi per anno: Analisi dei prezzi totali degli affitti brevi per ogni anno.
    • Turisti per anno: Numero totale di turisti che hanno visitato Bologna ogni anno.
    • Prezzi e turisti per anno: Relazione tra i prezzi degli affitti brevi e il numero di turisti per anno.
    • Prezzi mese per mese per anno: Andamento dei prezzi mese per mese per ogni anno.
    • Prezzi medi per quartiere: Visualizzazione dei prezzi medi degli affitti brevi nei diversi quartieri di Bologna.
    • Variazione percentuale dei prezzi rispetto all'anno precedente: Analisi della variazione percentuale dei prezzi rispetto all'anno precedente.

![Screenshot 2025-04-04 004852](https://github.com/user-attachments/assets/9d3e478b-55d3-4c17-a4e2-3fb322ab68da)


![Screenshot 2025-04-04 004824](https://github.com/user-attachments/assets/16f545cf-de41-4b45-9556-b03664a0f3c7)


Flusso di Lavoro

Il flusso di lavoro del progetto segue il framework PACE (Plan, Analyze, Construct, Execute), studiato durante la specializzazione Google Advanced Data Analytics”,con il supporto di un flusso ETL per l'estrazione, trasformazione e caricamento dei dati nel database. Il flusso completo è strutturato come segue:

1. Pianificazione (Plan)
Durante la fase di pianificazione, sono stati definiti gli obiettivi principali del progetto: visualizzare l'andamento dei prezzi e dei turisti nel tempo e prevedere i prezzi del 2025. È stato stabilito l'ambito del progetto, inclusa la scelta dei dataset.

2. Analisi (Analyze)
In questa fase sono stati analizzati i dati per identificare eventuali problematiche nei dataset:
    • Durante l'analisi esplorativa dei dati (EDA), è stato notato che i dati sui turisti erano già aggregati mensilmente, ma il dataset non includeva i dati di dicembre 2024. Questo ha portato alla necessità di implementare una regressione polinomiale per stimare i turisti mancanti di dicembre 2024.

3. Costruzione (Construct)
In questa fase sono stati sviluppati i seguenti passaggi chiave:
    • ETL (Extract, Transform, Load):
        ◦ Extract: I dati sono stati estratti dai file CSV (Airbnb e turisti) e caricati in un ambiente di sviluppo.
        ◦ Transform: I dati sono stati puliti e trasformati rimuovendo i duplicati e le colonne interamente vuote. In particolare, sono stati eseguiti calcoli per stimare i prezzi di dicembre 2024 tramite regressione polinomiale utilizzando i dati di novembre 2024 per testare il modello.
        ◦ Load: I dati trasformati sono stati caricati in un database PostgreSQL utilizzando Supabase.
        ◦ SQL: Creazione di due tabelle aggregate in SQL per visualizzare il numero dei turisti e il totale dei prezzi per anno e mese.
    • Calcolo dei Prezzi Annuali e Mensili: Poiché nei dati originali erano presenti solo il prezzo per notte, il numero di recensioni e il numero minimo di notti per ciascun alloggio, sono stati calcolati i prezzi annuali e mensili con le seguenti formule:
    • Prezzo annuale: Moltiplicando il prezzo per notte di ciascun alloggio per il numero di recensioni e il numero minimo di notti.
    • Prezzo mensile: Calcolato come il prezzo annuale diviso per 12.
Questi calcoli sono stati effettuati direttamente nel database PostgreSQL utilizzando query SQL per aggregare i dati per anno e mese. Le tabelle risultanti sono state poi utilizzate per l'analisi successiva. È importante notare che, trattandosi di stime, questi prezzi rappresentano una proiezione basata sui dati disponibili e non devono essere considerati come valori assoluti, ma come un'indicazione dei trend del mercato.
          
    • Regressione polinomiale: Nella tabella aggregata mensilmente in SQL è stata notata una carenza di dati sui prezzi di dicembre 2024. È stata quindi implementata una regressione polinomiale per stimare i prezzi di dicembre 2024 e aggiornato il database con i nuovi dati.
    • Regressione Lineare: È stata implementata una regressione lineare per prevedere il totale dei prezzi del 2025 utilizzando i dati del 2024 per valutare il modello.
    • Testing con Prophet: È stato anche testato un modello con Prophet per la previsione dei prezzi, come ulteriore metodo di verifica.

4. Esecuzione (Execute)
Una volta completata la fase di costruzione, sono stati eseguiti i seguenti passaggi:
    • Caricamento dei dati in Power BI: I dati finali sono stati importati da PostgreSQL in Power BI.
    • Creazione della dashboard in Power BI: È stata creata una dashboard interattiva che visualizza i prezzi, i turisti e le loro relazioni nel tempo.
Tecnologie Utilizzate
    • Python: Per la pulizia, trasformazione e analisi dei dati.
    • Pandas: Per la gestione dei dati.
    • scikit-learn: Per l'implementazione delle regressioni.
    • Prophet: Per la previsione dei prezzi.
    • SQL: Per creare e gestire il database PostgreSQL.
    • Power BI: Per la visualizzazione dei dati e la creazione della dashboard interattiva.

Conclusioni
Il progetto fornisce un'analisi dettagliata degli affitti brevi a Bologna, con una particolare attenzione all'andamento dei prezzi e al numero di turisti. La dashboard interattiva in Power BI consente di esplorare le tendenze nel tempo e la relazione tra i due fattori. Le regressioni hanno permesso di stimare il totale dei prezzi e il numero dei turisti per il mese di dicembre 2024 e di fare previsioni per il 2025. È importante notare che le stime sui turisti e sui prezzi di dicembre 2024, così come le previsioni per il 2025, sono indicative e basate sui dati storici disponibili, con l'obiettivo di esplorare le possibili tendenze. Questo progetto è stato realizzato a scopo didattico e di analisi.
