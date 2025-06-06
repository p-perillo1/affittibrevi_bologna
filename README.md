# Descrizione del progetto

Questo progetto si propone di analizzare il mercato degli affitti brevi a Bologna, utilizzando i dataset forniti da Airbnb e dal Comune di Bologna. L'obiettivo principale è osservare l'andamento dei prezzi e del numero di turisti nel corso degli anni.    
Sono stati utilizzati dati storici sui prezzi degli affitti brevi e sul numero di turisti per identificare le tendenze, le fluttuazioni e le eventuali correlazioni. Inoltre, sono state sviluppate tecniche di regressione per stimare i prezzi futuri, in particolare per il 2025, usando i dati del 2024 per testare i modelli. Il progetto include la creazione di una dashboard interattiva in Power BI che visualizza l'andamento dei prezzi e dei turisti nel tempo.

![Screenshot 2025-05-22 135549](https://github.com/user-attachments/assets/c91753dd-12a4-4ac8-b68d-628e9d1338e6)

## Funzionalità della dashboard in Power BI

La dashboard fornisce le seguenti visualizzazioni:

- **Prezzi per anno**: analisi dei prezzi totali degli affitti brevi per ogni anno
- **Turisti per anno**: numero totale di turisti che hanno visitato Bologna ogni anno
- **Prezzi e turisti per anno**: relazione tra i prezzi degli affitti brevi e il numero di turisti per anno
- **Turisti per mese e anno**: numero di turisti mese per mese per ogni anno
- **Prezzi per mese e anno**: andamento dei prezzi mese per mese per ogni anno
- **Prezzi medi per quartiere e conteggio annunci**: visualizzazione dei prezzi medi degli affitti brevi nei diversi quartieri di Bologna e conteggio degli annunci
- **Mappa con le distribuzioni degli alloggi**: visualizzazione di una mappa interattiva con la distrubuzione degli alloggi con colori differenti per ogni quartiere
- **Variazione percentuale dei prezzi e dei turisti rispetto all'anno precedente**: analisi della variazione percentuale dei prezzi e dei turisti rispetto all'anno precedente

## Flusso di lavoro

Il flusso di lavoro del progetto segue il metodo **PACE (Plan, Analyze, Construct, Execute)**, studiato durante la specializzazione *Google Advanced Data Analytics*, con il supporto di un flusso ETL per l'estrazione, trasformazione e caricamento dei dati nel database. Il flusso completo è strutturato come segue:

### Pianificazione (Plan)
Durante la fase di pianificazione, sono stati definiti gli obiettivi principali del progetto: visualizzare l'andamento dei prezzi e dei turisti nel tempo e prevedere i prezzi del 2025. È stato stabilito l'ambito del progetto, inclusa la scelta dei dataset.

### Analisi (Analyze)
In questa fase sono stati estratti e analizzati i dati per identificare eventuali problematiche nei dataset.  
Durante l'analisi esplorativa dei dati (EDA), è stato notato che i dati sui turisti erano già aggregati mensilmente, ma il dataset non includeva i dati di dicembre 2024. Questo ha portato alla necessità di implementare una regressione polinomiale per stimare i turisti mancanti di dicembre 2024.

Gli screenshot seguenti mostrano i risultati dell'analisi descrittiva (describe() e info()) sui dati, e le visualizzazioni che hanno evidenziato la mancanza dei dati di dicembre 2024:

Esempio di analisi descrittiva sul dataframe `Reviews`:  
![Screenshot 2025-04-04 075414](https://github.com/user-attachments/assets/6f2d6761-3573-4410-9138-7352cf0b82a4)

Visualizzazione durante l' analasi esplorativa:  
![Screenshot 2025-04-04 105906](https://github.com/user-attachments/assets/a2c4bc59-be6e-4c83-82a9-142c8a3067c3)

Sono stati stampati i dati dei turisti per il 2024:

![Screenshot 2025-04-04 191508](https://github.com/user-attachments/assets/c654630a-b17f-4b8a-8d4a-f2a62cc6fe01)

Dall'output si evince che il valore di dicembre 2024 non è presente:  
![Screenshot 2025-04-04 082721](https://github.com/user-attachments/assets/6e9129ba-c41d-49a6-9d57-e511ac85b496)

### Costruzione (Construct)
In questa fase sono stati sviluppati i seguenti passaggi chiave:

#### ETL (Extract, Transform, Load)

- **Extract**: I dati sono stati estratti dai file CSV (Airbnb e turisti) e caricati in un ambiente di sviluppo.

![Screenshot 2025-04-04 095229](https://github.com/user-attachments/assets/390ef775-f726-4494-9379-e5223a105d4a)

- **Transform**: I dati sono stati puliti e trasformati rimuovendo i duplicati, eliminando i campi interamente vuoti e uniformando i nomi delle colonne, rinominandoli in minuscolo e rimuovendo eventuali spazi bianchi.  
La colonna `date` del dataframe `Reviews` è stata convertita da tipo object a tipo datetime per facilitare l'analisi nei processi successivi.

![Screenshot 2025-04-05 200526](https://github.com/user-attachments/assets/36634db3-9be4-47b0-ad0d-11e463f7910d)

Durante l'analisi preliminare dei dati trasformati, è stata riscontrata l'assenza dei dati relativi ai turisti di dicembre 2024. Per colmare questa mancanza, nella fase di trasformazione è stata implementata una regressione polinomiale per stimare i valori mancanti. Il modello è stato prima testato utilizzando i dati di novembre 2024 per verificarne l'accuratezza prima di applicarlo alla previsione di dicembre 2024.

**Regressioni polinomiali per i turisti di dicembre 2024**:   

![Screenshot 2025-04-04 105631](https://github.com/user-attachments/assets/867bce7e-a939-4280-94af-6f4b659adcb4)  
![Screenshot 2025-04-04 105648](https://github.com/user-attachments/assets/3aa3f8e3-1200-434b-a078-c3d5c087c0ae)

![Screenshot 2025-04-04 084230](https://github.com/user-attachments/assets/c034e4bd-e59d-4a0a-ae04-f21a5e95cda4)  
![Screenshot 2025-04-04 084412](https://github.com/user-attachments/assets/6aa24562-2747-465e-b61d-e7e081057692)

Visualizzazione dopo l' aggiunta del valore stimato:  
![Screenshot 2025-04-04 110000](https://github.com/user-attachments/assets/ab4ebdfd-8113-4489-bb01-c63e0f70aedd)

- **Load**: I dati trasformati sono stati caricati in un database PostgreSQL utilizzando Supabase.

![Screenshot 2025-04-04 084849](https://github.com/user-attachments/assets/a42d5a08-5b5e-489a-926d-8e7ce207423a)

#### Aggiunta variante ETL con OOP
Oltre alla pipeline ETL implementata con script separati(extract.py, transform.py, load.py, main.py) è stata sviluppata anche una variante orientata agli oggetti(OOP).
Questa versione utilizza classi per gestire le fasi di estrazione, trasformazione e caricamento dei dati, offrendo una struttura più modulare ed estendibile.

#### Calcolo dei prezzi e turisti annuali e mensili in SQL
Sono state create due tabelle aggregate in SQL per analizzare i prezzi e i flussi turistici su base mensile e annuale.  
Poiché nei dati originali erano presenti solo il prezzo per notte, il numero di recensioni e il numero minimo di notti per ciascun alloggio, sono stati calcolati i prezzi annuali e mensili con le seguenti formule:

**Prezzo annuale**: Moltiplicando il prezzo per notte di ciascun alloggio per il numero di recensioni e il numero minimo di notti.  
**Prezzo mensile**: Calcolato come il prezzo annuale diviso per 12.

Questi calcoli sono stati effettuati direttamente nel database PostgreSQL utilizzando query SQL per aggregare i dati per anno e mese. Le tabelle risultanti sono state poi utilizzate per l'analisi successiva.   
**È importante notare che, trattandosi di stime, questi prezzi rappresentano una proiezione basata sui dati disponibili e non devono essere considerati come valori assoluti, ma come un'indicazione dei trend del mercato.**

Tabella prezzi e turisti mensili:  
```SQL
CREATE TABLE prezzo_turisti_mensili AS
WITH num_reviews AS (
    SELECT 
        listing_id, 
        EXTRACT(YEAR FROM date) AS anno,  
        EXTRACT(MONTH FROM date) AS mese,  
        COUNT(listing_id) AS num_reviews_in_month
    FROM reviews
    GROUP BY listing_id, anno, mese
)
SELECT 
    nr.anno, 
    nr.mese,  
    SUM(l.price * l.minimum_nights * nr.num_reviews_in_month) AS prezzo_mensile,  -- Moltiplica il prezzo per il minimo di notti e il numero di recensioni
    t.numero AS turisti_mensili
FROM listings l
JOIN num_reviews nr ON l.id = nr.listing_id  -- Associa listings con il numero di recensioni
JOIN tourism t ON nr.anno = t.anno AND nr.mese = t.mese_num  -- Associa il risultato del primo join a tourism
GROUP BY nr.anno, nr.mese, t.numero
ORDER BY nr.anno, nr.mese;
```

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
Dal risultato della query si nota che i dati di dicembre 2024 sono aggiornati al 19-12-2024:  
![Screenshot 2025-04-03 232641](https://github.com/user-attachments/assets/aba029c1-7aa2-48e0-a71c-52d1e9263caa)

#### Regressioni polinomiali per i prezzi di dicembre 2024
Nella tabella aggregata mensilmente in SQL è stata notata una carenza di dati sui prezzi di dicembre 2024. È stata quindi implementata una regressione polinomiale per stimare i prezzi di dicembre 2024, testando il modello sui dati di novembre 2024. Successivamente il database è stato aggiornato con i nuovi dati.

![Screenshot 2025-04-04 090013](https://github.com/user-attachments/assets/4a510452-0837-4edf-88ba-31e8783cf5ed)

![Screenshot 2025-04-16 223959](https://github.com/user-attachments/assets/3c26bd9c-85a1-4fc7-b36b-d6a41e85aafd)

Tabella prezzi e turisti annuali:  

```SQL
CREATE TABLE prezzo_turisti_annuali AS
SELECT 
    anno, 
    SUM(turisti_mensili) AS turisti_annuali,
    SUM(prezzo_mensile) AS prezzi_annuali
FROM prezzo_turisti_mensili    
GROUP BY anno
ORDER BY anno;
```
![Screenshot 2025-04-16 224441](https://github.com/user-attachments/assets/91d3ff3e-6654-47c6-bb93-4d36185e47e6)

#### Regressione lineare previsione 2025
È stata implementata una regressione lineare con regolarizzazione Ridge per calcolare il totale dei prezzi del 2025 utilizzando i dati del 2024 per valutare il modello.

![Screenshot 2025-04-16 224812](https://github.com/user-attachments/assets/ea6e09db-025e-49d0-8191-5391f36f5e0d)

Per trattare la variabile `mese` si è utilizzata una tecnica di codifica ciclica. I mesi dell'anno sono stati trasformati in due nuove colonne: seno e coseno.  
Questo approccio consente al modello di catturare la periodicità del calendario, evitando che mesi consecutivi ma numericamente distanti, come dicembre(12) e gennaio(1), vengano interpretati come lontani nel tempo.

Per addestrare il modello sono stati utlizzati i dati del 2022 e 2023, in questo modo si è cercato di catturare una dinamica più stabile e coerente con la realtà post-pandemica. Gli anni precedenti (2019–2021) sono stati esclusi per via della forte variabilità dovuta alla pandemia.

Analizzando i dati è emerso che la crescita tra il 2023 e il 2024 è stata inferiore rispetto agli anni precedenti. Questo ha introdotto una fluttuazione temporanea nei trend che avrebbe potuto distorcere le previsioni del modello.  
L'inclusione del 2024 nel set di addestramento avrebbe spinto il modello ad adattarsi a questa anomalia di crescita ridotta, compromettendo la capacità predittiva per i periodi successivi.   
Per questo motivo il 2024 è stato escluso dal training ed è stato utilizzato solo come dato di test, in modo da valutare il modello su dati reali ma non influenzarne l’addestramento.  

#### Testing con Prophet
È stato anche testato un modello con Prophet per la previsione dei prezzi del 2025, come ulteriore metodo di verifica. 

![Screenshot 2025-04-04 090308](https://github.com/user-attachments/assets/85400afd-3171-4cf4-8def-d133781cc913)

Il test condotto con Prophet ha evidenziato una sottostima delle previsioni per il 2024. Questo comportamento è probabilmente attribuibile alla scarsità di dati disponibili per l’addestramento, che ha limitato la capacità del modello di cogliere appieno le dinamiche di lungo periodo.

Al contrario, la regressione lineare con regolarizzazione Ridge, pur non essendo progettata per la modellazione di serie temporali, ha prodotto previsioni più coerenti con il trend osservato. Nonostante i limiti del modello e la quantità ridotta di dati utilizzata per l'addestramento, la regressione lineare ha saputo cogliere in maniera più efficace la tendenza di crescita rispetto a Prophet.

### Esecuzione (Execute)
Una volta completata la fase di costruzione, sono stati eseguiti i seguenti passaggi:

- **Caricamento dei dati in Power BI**: I dati finali sono stati importati da PostgreSQL in Power BI.
- **Creazione della dashboard in Power BI**: È stata creata una dashboard interattiva che visualizza i prezzi, i turisti e le loro relazioni nel tempo.

![Screenshot 2025-05-22 135549](https://github.com/user-attachments/assets/aad376a8-3368-4bf4-9825-a7bd0c02e455)  
![Screenshot 2025-05-22 135604](https://github.com/user-attachments/assets/128b3078-f46e-41d6-8f75-c2e9066e9f5c)  
![Screenshot 2025-05-22 140242](https://github.com/user-attachments/assets/f11698bd-8770-479b-a323-109149211cd8)  
![Screenshot 2025-05-22 140850](https://github.com/user-attachments/assets/39327cf3-8e82-41f7-8b88-f0d4f742abfd)

## Insight

La dashboard mostra l’andamento annuale e mensile dei prezzi degli affitti brevi a Bologna, in relazione al numero di turisti. I dati evidenziano un forte calo nel 2020 a causa della pandemia da COVID-19, seguito da una ripresa costante a partire dal 2021.  
Nel 2023 si è registrato un marcato incremento del flusso turistico e dei prezzi, con valori che hanno superato sensibilmente quelli del periodo pre-pandemia. Nel 2024 la crescita è proseguita, seppur con un ritmo più moderato, a conferma di una tendenza positiva e consolidata nel settore turistico.  
Dal punto di vista stagionale si osservano picchi nei prezzi degli affitti brevi nei mesi di maggio, giugno, luglio, settembre e ottobre, corrispondenti ai periodi di maggiore afflusso turistico. I quartieri centrali (come Santo Stefano, Porto-Saragozza) presentano prezzi medi più elevati e un maggior numero di alloggi disponibili.  
Per i proprietari che affittano su Airbnb, l’analisi suggerisce di adeguare le tariffe con un incremento annuale del 5-8%, soprattutto nei mesi ad alta domanda.

## Tecnologie utilizzate

- **Python**: Per l'estrazione, la trasformazione e il caricamento dei dati (ETL) e per l'implementazione dei modelli di machine learning.
- **NumPy**: Per operazioni numeriche e manipolazione di array.
- **Pandas**: Per la gestione dei dati.
- **Matplotlib**: Per la visualizzazione grafica dei dati durante l'analisi esplorativa.
- **scikit-learn**: Per l'implementazione delle regressioni.
- **Prophet**: Per la previsione dei prezzi.
- **SQL**: Per creare e gestire il database PostgreSQL.
- **Power BI**: Per la visualizzazione dei dati e la creazione della dashboard interattiva.
- **Supabase**: Per l'hosting e la gestione del database PostgreSQL.
- **ODBC**: Per la connessione tra PostgreSQL e Power BI.

## Conclusioni
Il progetto fornisce un'analisi degli affitti brevi a Bologna, con una particolare attenzione all'andamento dei prezzi e al numero di turisti.       
La dashboard interattiva in Power BI consente di esplorare le tendenze nel tempo e la relazione tra i due fattori, evidenziando la correlazione tra l'aumento dei turisti e l'incremento dei prezzi.     
Le regressioni hanno permesso di stimare il totale dei prezzi e il numero dei turisti per il mese di dicembre 2024 e di fare previsioni per il 2025.  
L'incremento costante del numero di turisti ha contribuito all'espansione del mercato degli affitti brevi e all'aumento dei prezzi, sottolineando che l'affitto breve è ormai parte integrante dell'ecosistema turistico cittadino.    
 **È importante sottolineare che le stime sui turisti e sui prezzi di dicembre 2024, così come le previsioni per il 2025, sono indicative e basate sui dati storici disponibili, con l'obiettivo di esplorare le possibili tendenze.  
Questo progetto è stato realizzato a scopo didattico e di analisi.**

## Link dataset  
[Dataset Turisti](https://inumeridibolognametropolitana.it/dati-statistici/turisti-nel-comune-e-nella-citta-metropolitana-di-bologna-serie-storica): Fornisce dati storici sul numero di turisti a Bologna e nell’area metropolitana.  
[Dataset Airbnb](https://insideairbnb.com/get-the-data/): Contiene dati sugli affitti brevi nella città di Bologna, estratti dalla piattaforma Inside Airbnb. Include informazioni su prezzi, disponibilità e recensioni.

## Struttura del progetto

La struttura del progetto `affittibrevi_bologna` è la seguente:
```
affittibrevi_bologna/
├── python/
│   ├── extract.py                                      # Estrazione dei dati dai file CSV
│   ├── transform.py                                    # Trasformazione dei dati per il modello
│   ├── load.py                                         # Caricamento dei dati nel database PostgreSQL
│   ├── main.py                                         # Script principale che esegue l'intero processo ETL
│   ├── etl_oop.py                                      # Pipeline ETL orientata agli oggetti(OOP)
│   ├── regressione_turisti_novembre_2024.py            # Modello di regressione per turisti a novembre 2024
│   ├── regressione_turisti_dicembre_2024.py            # Modello di regressione per turisti a dicembre 2024
│   ├── regressione_prezzi_novembre_2024.py             # Modello di regressione per prezzi a novembre 2024
│   ├── regressione_prezzi_dicembre_2024.py             # Modello di regressione per prezzi a dicembre 2024
│   ├── regressione_ridge_test_2024_previsione_2025.py  # Modello di regressione Ridge per previsione 2025
│   ├── prophet.py                                      # Modello Prophet per previsioni di serie temporali
│   └── env.py                                          # File per configurare le variabili d'ambiente
├── README.md                                           # Questo file
├── requirements.txt                                    # File delle dipendenze del progetto
├── sql/                                                # Cartella per script SQL                
│   └── querySQL.sql                                    # Script SQL per eseguire query analitiche sui dati
```
