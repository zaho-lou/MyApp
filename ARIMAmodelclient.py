import streamlit as st
import pandas as pd
import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('ma_base1.db')
cur = conn.cursor()

# Chargement des données
df = pd.read_sql_query("SELECT * FROM ma_table", conn, parse_dates=['date'])

# Sélection de l'ID client
clients = df['client_id'].unique()
client_id = st.selectbox('Sélectionnez un client :', clients)

# Filtrage des données pour le client sélectionné
df_client = df[df['client_id'] == client_id]

# Calcul du taux d'évolution mensuel des consommations
df_client['taux_evol'] = df_client['valeur'].pct_change() * 100

# Affichage du taux d'évolution sous forme de tableau
st.write(f"Taux d'évolution mensuel des consommations pour le client {client_id} :")
st.write(df_client[['date', 'valeur', 'taux_evol']])
