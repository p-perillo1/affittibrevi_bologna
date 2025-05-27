import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sqlalchemy import create_engine
from regressione_turisti_dicembre_2024 import apply_regression

class Extractor:
    def __init__(self):
        load_dotenv()
        self.df_tourism = None
        self.df_listings = None
        self.df_reviews = None

    def extract(self):
        """Estrae i dati dai file CSV con gestione errori"""
        try:
            self.df_tourism = pd.read_csv(os.getenv("csv_tourism"), sep=";")
            self.df_listings = pd.read_csv(os.getenv("csv_listings"))
            self.df_reviews = pd.read_csv(os.getenv("csv_reviews"))
            print("Estrazione completata.")
        except FileNotFoundError as e:
            print(f"File non trovato: {e}")
            raise
        except Exception as e:
            print(f"Errore durante l'estrazione: {e}")
            raise


class Transformer:
    def __init__(self):
        self.df_tourism = None
        self.df_listings = None
        self.df_reviews = None

    def eda(self, df_tourism, df_listings, df_reviews):
        """Analisi esplorativa"""
        try:
            print("\n=== EDA - Tourism ===")
            print(df_tourism.head(), df_tourism.info(), df_tourism.describe())
            print("\n=== EDA - Listings ===")
            print(df_listings.head(), df_listings.info(), df_listings.describe())
            print("\n=== EDA - Reviews ===")
            print(df_reviews.head(), df_reviews.info(), df_reviews.describe())
        except Exception as e:
            print(f"Errore durante l'EDA: {e}")

    def clean_data(self, df):
        """Pulizia dei dati"""
        try:
            df = df.rename(columns=lambda x: x.strip().lower())
            df = df.drop_duplicates()
            df = df.dropna(how="all", axis=1)
            return df
        except Exception as e:
            print(f"Errore nella pulizia dei dati: {e}")
            raise

    def plot_avg_price(self, df, title="Prezzi Medi per Quartiere"):
        """Visualizza i prezzi medi per quartiere."""
        try:
            if "neighbourhood" in df.columns and "price" in df.columns:
                df.groupby('neighbourhood')['price'].mean().sort_values().plot(
                    kind='barh', figsize=(8, 5), color='orange', edgecolor='black')
                plt.title(title)
                plt.xlabel("Prezzo (€)")
                plt.ylabel("Quartiere")
                plt.grid(True)
                plt.tight_layout()
                plt.show()
        except Exception as e:
            print(f"Errore durante la visualizzazione prezzi: {e}")

    def plot_tourists_per_year(self, df, title="Totale Turisti per Anno"):
        """Visualizza il numero di turisti per anno"""
        try:
            if "anno" in df.columns and "numero" in df.columns:
                df.groupby('anno')['numero'].sum().plot(
                    kind='bar', figsize=(8, 5), color='green', edgecolor='black')
                plt.title(title)
                plt.xlabel("Anno")
                plt.ylabel("Numero di Turisti")
                plt.grid(True)
                plt.tight_layout()
                plt.show()
            else:
                print("Colonne 'anno' o 'numero' non trovate")
        except Exception as e:
            print(f"Errore durante la visualizzazione turisti: {e}")

    def visualizations(self, df_tourism, df_listings):
        """Chiama le funzioni di visualizzazione"""
        self.plot_avg_price(df_listings)
        self.plot_tourists_per_year(df_tourism)

    def transform(self, df_tourism, df_listings, df_reviews):
        """Applica pulizia e visualizzazioni"""
        try:
            self.eda(df_tourism, df_listings, df_reviews)

            self.df_tourism = self.clean_data(df_tourism)
            self.df_listings = self.clean_data(df_listings)
            self.df_reviews = self.clean_data(df_reviews)

            self.visualizations(self.df_tourism, self.df_listings)
            print("Trasformazione completata")
            return self.df_tourism, self.df_listings, self.df_reviews
        except Exception as e:
            print(f"Errore nella fase di trasformazione: {e}")
            raise


class Loader:
    def __init__(self):
        try:
            load_dotenv()
            self.engine = create_engine(
                f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
                f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
            )
        except Exception as e:
            print(f"Errore nella connessione al database: {e}")
            raise

    def load_to_db(self, df, table_name):
        """Carica DataFrame nel database"""
        try:
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
            print(f"Dati caricati nella tabella '{table_name}'.")
        except Exception as e:
            print(f"Errore durante il caricamento in '{table_name}': {e}")
            raise


class ETLProcess:
    def __init__(self):
        self.extractor = Extractor()
        self.transformer = Transformer()
        self.loader = Loader()

    def run(self):
        """Esegue l'intero processo ETL"""
        print("Avvio del processo ETL...")

        try:
            self.extractor.extract()

            df_tourism, df_listings, df_reviews = self.transformer.transform(
                self.extractor.df_tourism, self.extractor.df_listings, self.extractor.df_reviews)

            print("Applicazione regressione...")
            df_tourism = apply_regression(df_tourism)

            print("Regressione applicata con successo")

            # Caricamento su DB (decommenta se necessario)
            self.loader.load_to_db(df_tourism, "tourism")
            self.loader.load_to_db(df_listings, "listings")
            self.loader.load_to_db(df_reviews, "reviews")

            print("ETL completato con successo")

        except Exception as e:
            print(f"ETL terminato con un errore: {e}")


if __name__ == "__main__":
    etl = ETLProcess()
    etl.run()
