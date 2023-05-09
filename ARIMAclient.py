import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from pmdarima.arima import auto_arima

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

# Préparation des données pour la prédiction ARIMA
df_pred = df_client[['date', 'valeur']]
df_pred.set_index('date', inplace=True)

# Détermination des paramètres ARIMA optimaux avec la méthode auto_arima
model = auto_arima(df_pred, seasonal=True, m=12, suppress_warnings=True)
order = model.order
sorder = model.seasonal_order

# Prédiction de la consommation future pour les 5 prochaines années
forecast = model.predict(n_periods=5*12)
forecast_index = pd.date_range(start=df_pred.index[-1], periods=5*12, freq='MS')
forecast = pd.DataFrame(forecast, index=forecast_index, columns=['valeur'])

# Concaténation des données observées et prédites
df_plot = pd.concat([df_pred, forecast], axis=0)

# Affichage du graphique dans Streamlit
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(df_plot.index, df_plot['valeur'], label='Observations')
ax.plot(forecast.index, forecast['valeur'], label='Prédictions')
ax.legend()
ax.set_title(f"Prédiction de la consommation future pour le client {client_id}")
ax.set_xlabel("Date")
ax.set_ylabel("Ventes")
st.pyplot(fig)

# Affichage des prévisions sous format tableau
st.write(f"Prévisions de consommation pour le client {client_id} :")
st.write(forecast)