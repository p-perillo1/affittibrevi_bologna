-- Query per la creazione della tabella con i prezzi ed i turisti mensili 
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


-- Query per la creazione della tabella con i prezzi ed i turisti annuali
CREATE TABLE prezzo_turisti_annuali AS
SELECT 
    anno, 
    SUM(turisti_mensili) AS turisti_annuali,
    SUM(prezzo_mensile) AS prezzi_annuali
FROM prezzo_turisti_mensili    
GROUP BY anno
ORDER BY anno;


-- Query per il conteggio del numero di recensioni e la data dell' ultima recensione disponibile per l'anno 2024
SELECT 
    EXTRACT(YEAR FROM "date") AS anno,
    EXTRACT(MONTH FROM "date") AS mese,
    COUNT(*) AS numero_recensioni,
    MAX("date") AS ultima_recensione
FROM reviews  
WHERE EXTRACT(YEAR FROM "date") = 2024  -- Filtro per l'anno 2024
GROUP BY anno, mese
ORDER BY anno, mese;

