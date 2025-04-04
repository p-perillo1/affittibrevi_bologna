# Descrizione del Progetto

Questo progetto si propone di analizzare il mercato degli affitti brevi a Bologna, utilizzando i dataset forniti da Airbnb e dal Comune di Bologna. L'obiettivo principale è analizzare l'andamento dei prezzi e del numero di turisti nel corso degli anni.  
Sono stati utilizzati dati storici sui prezzi degli affitti brevi e sul numero di turisti per identificare le tendenze, le fluttuazioni e le eventuali correlazioni. Inoltre, sono state sviluppate tecniche di regressione per stimare i prezzi futuri, in particolare per il 2025, usando i dati del 2024 per testare i modelli. Il progetto include la creazione di una dashboard interattiva in Power BI che visualizza l'andamento dei prezzi e dei turisti nel tempo.

![Screenshot 2025-04-04 095002](https://github.com/user-attachments/assets/21db0537-5148-4d80-841b-120a9116a67b)

## Funzionalità della Dashboard in Power BI

La dashboard fornisce le seguenti visualizzazioni:

- **Prezzi per anno**: Analisi dei prezzi totali degli affitti brevi per ogni anno.
- **Turisti per anno**: Numero totale di turisti che hanno visitato Bologna ogni anno.
- **Prezzi e turisti per anno**: Relazione tra i prezzi degli affitti brevi e il numero di turisti per anno.
- **Prezzi per mese e anno**: Andamento dei prezzi mese per mese per ogni anno.
- **Prezzi medi per quartiere e conteggio host**: Visualizzazione dei prezzi medi degli affitti brevi nei diversi quartieri di Bologna e il conteggio degli host
- **Mappa con le distrubizioni degli alloggi**: Visualizzazione di una mappa interattiva con la distrubuzione degli alloggi con colori differenti per ogni quartiere.
- **Variazione percentuale dei prezzi rispetto all'anno precedente**: Analisi della variazione percentuale dei prezzi rispetto all'anno precedente.

## Flusso di Lavoro

Il flusso di lavoro del progetto segue il framework PACE (Plan, Analyze, Construct, Execute), studiato durante la specializzazione *Google Advanced Data Analytics*, con il supporto di un flusso ETL per l'estrazione, trasformazione e caricamento dei dati nel database. Il flusso completo è strutturato come segue:

### Pianificazione (Plan)
Durante la fase di pianificazione, sono stati definiti gli obiettivi principali del progetto: visualizzare l'andamento dei prezzi e dei turisti nel tempo e prevedere i prezzi del 2025. È stato stabilito l'ambito del progetto, inclusa la scelta dei dataset.

### Analisi (Analyze)
In questa fase sono stati analizzati i dati per identificare eventuali problematiche nei dataset:
- Durante l'analisi esplorativa dei dati (EDA), è stato notato che i dati sui turisti erano già aggregati mensilmente, ma il dataset non includeva i dati di dicembre 2024. Questo ha portato alla necessità di implementare una regressione polinomiale per stimare i turisti mancanti di dicembre 2024.

![Screenshot 2025-04-04 075414](https://github.com/user-attachments/assets/6f2d6761-3573-4410-9138-7352cf0b82a4)

### Costruzione (Construct)
In questa fase sono stati sviluppati i seguenti passaggi chiave:

#### ETL (Extract, Transform, Load)

- **Extract**: I dati sono stati estratti dai file CSV (Airbnb e turisti) e caricati in un ambiente di sviluppo.

![Screenshot 2025-04-04 095229](https://github.com/user-attachments/assets/390ef775-f726-4494-9379-e5223a105d4a)

- **Transform**: I dati sono stati puliti e trasformati rimuovendo i duplicati, le colonne interamente vuote, rinominando in minuscolo e rimuovendo evenutali spazi bianchi da tutte le intestazioni delle colonne.
I dati transfromati sono stati visualizzati per una prima analisi che ha evidenziato la mancanza dei dati dei turisti di dicembre 2024. Successivamente sono stati eseguiti calcoli per stimare i turisti di dicembre 2024 tramite regressione polinomiale utilizzando i dati di novembre 2024 per testare il modello.

![Screenshot 2025-04-04 080149](https://github.com/user-attachments/assets/ef7eecc1-d49f-4706-b4fa-273fef6a839c)

![Screenshot 2025-04-04 082721](https://github.com/user-attachments/assets/6e9129ba-c41d-49a6-9d57-e511ac85b496)

![Screenshot 2025-04-04 084230](https://github.com/user-attachments/assets/c034e4bd-e59d-4a0a-ae04-f21a5e95cda4)
![Screenshot 2025-04-04 084412](https://github.com/user-attachments/assets/6aa24562-2747-465e-b61d-e7e081057692)

- **Load**: I dati trasformati sono stati caricati in un database PostgreSQL utilizzando Supabase.

![Screenshot 2025-04-04 084849](https://github.com/user-attachments/assets/a42d5a08-5b5e-489a-926d-8e7ce207423a)
  
- **SQL**: Creazione di due tabelle aggregate in SQL per visualizzare il numero dei turisti e il totale dei prezzi per anno e mese.

#### Calcolo dei Prezzi Annuali e Mensili
Poiché nei dati originali erano presenti solo il prezzo per notte, il numero di recensioni e il numero minimo di notti per ciascun alloggio, sono stati calcolati i prezzi annuali e mensili con le seguenti formule:
- **Prezzo annuale**: Moltiplicando il prezzo per notte di ciascun alloggio per il numero di recensioni e il numero minimo di notti.
- **Prezzo mensile**: Calcolato come il prezzo annuale diviso per 12.

Questi calcoli sono stati effettuati direttamente nel database PostgreSQL utilizzando query SQL per aggregare i dati per anno e mese. Le tabelle risultanti sono state poi utilizzate per l'analisi successiva. È importante notare che, trattandosi di stime, questi prezzi rappresentano una proiezione basata sui dati disponibili e non devono essere considerati come valori assoluti, ma come un'indicazione dei trend del mercato.

![Screenshot 2025-04-03 233043](https://github.com/user-attachments/assets/caa5e7a3-c8cf-4575-90ef-89741d0cd554)

```SQL
SELECT 
    EXTRACT(YEAR FROM "date") AS anno,
    EXTRACT(MONTH FROM "date") AS mese,
    COUNT(*) AS numero_recensioni,
    MAX("date") AS ultima_recensione
FROM reviews  
WHERE EXTRACT(YEAR FROM "date") = 2024  -- Filtro per l'anno 2024
GROUP BY anno, mese
ORDER BY anno, mese;
```
Dal risultato della query si nota che i dati di dicembre 2024 sono aggiornati al 19-12-2024.
![Screenshot 2025-04-03 232641](https://github.com/user-attachments/assets/aba029c1-7aa2-48e0-a71c-52d1e9263caa)

#### Regressione polinomiale
Nella tabella aggregata mensilmente in SQL è stata notata una carenza di dati sui prezzi di dicembre 2024. È stata quindi implementata una regressione polinomiale per stimare i prezzi di dicembre 2024 e aggiornato il database con i nuovi dati.

![Screenshot 2025-04-04 090013](https://github.com/user-attachments/assets/4a510452-0837-4edf-88ba-31e8783cf5ed)

![Screenshot 2025-04-04 090126](https://github.com/user-attachments/assets/a2a86caa-96d5-460d-981a-1eeb64379f30)

Creazione tabella con i prezzi annuali
```
CREATE TABLE prezzo_turisti_annuali AS
SELECT 
    anno, 
    SUM(turisti_mensili) AS turisti_annuali,
    SUM(prezzo_mensile) AS prezzi_annuali
FROM prezzo_turisti_mensili    
GROUP BY anno
ORDER BY anno;
```
![Screenshot 2025-04-04 102404](https://github.com/user-attachments/assets/2a2162f8-7d5f-4070-8452-158e3d176830)

#### Regressione Lineare previsione 2025
È stata implementata una regressione lineare con regularizzazione Ridge per calcolare il totale dei prezzi del 2025 utilizzando i dati del 2024 per valutare il modello.

![Screenshot 2025-04-04 102209](https://github.com/user-attachments/assets/5130f88b-8ca2-4227-8e95-04cf170795e9)

#### Testing con Prophet
È stato anche testato un modello con Prophet per la previsione dei prezzi del 2025, come ulteriore metodo di verifica.

![Screenshot 2025-04-04 090308](https://github.com/user-attachments/assets/85400afd-3171-4cf4-8def-d133781cc913)

Il test con Prophet ha evidenziato come quest'ultimo tenda a sovrastimare le previsioni del 2025, questo risultato è probabilmente dovuto ai pochi dati con cui il modello è stato allenato. 
Le previsioni della regressione Lineare con regularizzazione Ridge nonostante i limiti del modello per la previsione su serie temporali tendono ad essere più veritiere.

### Esecuzione (Execute)
Una volta completata la fase di costruzione, sono stati eseguiti i seguenti passaggi:

- **Caricamento dei dati in Power BI**: I dati finali sono stati importati da PostgreSQL in Power BI.
- **Creazione della dashboard in Power BI**: È stata creata una dashboard interattiva che visualizza i prezzi, i turisti e le loro relazioni nel tempo.

![Screenshot 2025-04-04 003614](https://github.com/user-attachments/assets/c05e8c21-442e-4284-9dad-da242eab7832)

![Screenshot 2025-04-04 004852](https://github.com/user-attachments/assets/025b455c-b69a-487f-84f7-342f3cf76bd8)

![Screenshot 2025-04-04 004824](https://github.com/user-attachments/assets/a24f6e7a-88c6-4ac6-941f-37cde607ab51)

## Insight

La dashboard mostra l'andamento annuale e mensile dei prezzi degli affitti brevi a Bologna e il numero di turisti. Gli insight ottenuti dalle analisi mostrano una forte descrescita nel 2020 dovuta al COVID, dal 2021 si nota una crescita continua dei prezzi in coincidenza con l'aumento dei turisti. È stato osservato un picco nei prezzi degli affitti brevi durante i mesi di maggio, luglio e ottobre. I quartieri centrali tendono ad avere prezzi medi più alti ed un maggior numero di alloggi, nonostante ciò la differenza tra i prezzi medi dei vari quartieri tende ad essere bassa.

## Tecnologie Utilizzate

- **Python**: Per la pulizia, trasformazione e analisi dei dati.
- **Pandas**: Per la gestione dei dati.
- **scikit-learn**: Per l'implementazione delle regressioni.
- **Prophet**: Per la previsione dei prezzi.
- **SQL**: Per creare e gestire il database PostgreSQL.
- **Power BI**: Per la visualizzazione dei dati e la creazione della dashboard interattiva.

## Conclusioni
Il progetto fornisce un'analisi dettagliata degli affitti brevi a Bologna, con una particolare attenzione all'andamento dei prezzi e al numero di turisti. La dashboard interattiva in Power BI consente di esplorare le tendenze nel tempo e la relazione tra i due fattori. Le regressioni hanno permesso di stimare il totale dei prezzi e il numero dei turisti per il mese di dicembre 2024 e di fare previsioni per il 2025. È importante notare che le stime sui turisti e sui prezzi di dicembre 2024, così come le previsioni per il 2025, sono indicative e basate sui dati storici disponibili, con l'obiettivo di esplorare le possibili tendenze. Questo progetto è stato realizzato a scopo didattico e di analisi.
