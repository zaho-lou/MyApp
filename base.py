import streamlit as st
import sqlite3
from datetime import datetime
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd



# Chargement des données des clients
def parser(x):
    return datetime.strptime(x,'%m%Y')

data = pd.read_csv('ts_bruttt22.csv', sep=";",index_col=1,parse_dates=[1],  date_parser=parser, encoding='ISO-8859-1')
data['valeur'] = data.valeur.fillna(0)

client = pd.read_csv('clients2.csv', sep=";", parse_dates=['date'],date_parser=parser, encoding='ISO-8859-1')

consommation = pd.read_csv('consommation.csv', sep=";", parse_dates=['date'],date_parser=parser, encoding='ISO-8859-1')

prediction = pd.read_csv('predictions.csv', sep=";", parse_dates=['date'],date_parser=parser, encoding='ISO-8859-1')

pred = pd.read_csv('pred.csv', sep=";", parse_dates=['date'],date_parser=parser, encoding='ISO-8859-1')


# Créer une connexion à la base de données
conn = sqlite3.connect('ma_base1.db')

# Ajouter les tables du DataFrame à la base de données
data.to_sql('ma_table', conn, if_exists='replace', index=True)
client.to_sql('client', conn, if_exists='replace', index=False)
consommation.to_sql('consommation', conn, if_exists='replace', index=False)
prediction.to_sql('prediction', conn, if_exists='replace', index=False)
pred.to_sql('pred', conn, if_exists='replace', index=False)

# Fermer la connexion à la base de données
conn.close()

# Ouvrir une nouvelle connexion à la base de données
conn = sqlite3.connect('ma_base1.db')

# Récupérer les données de la base de données dans un DataFrame Pandas
data = pd.read_sql('SELECT * FROM ma_table', conn)
client = pd.read_sql('SELECT * FROM client', conn)
consommation = pd.read_sql('SELECT * FROM consommation', conn)
prediction = pd.read_sql('SELECT * FROM prediction', conn)
pred = pd.read_sql('SELECT * FROM pred', conn)

# Fermer la connexion à la base de données
conn.close()

# Afficher les données dans Streamlit
st.write('Table "ma_table" :', data)
st.write('Table "clients" :', client)
st.write('Table "consommations" :', consommation)
st.write('Table "predictions" :', prediction)
st.write('Table "prevision" :', pred)