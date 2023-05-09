import pandas as pd
import streamlit as st
import pmdarima as pm
from sklearn.metrics import mean_absolute_error
import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('ma_base1.db')
c = conn.cursor()

# Création d'un DataFrame vide pour stocker les données du tableau
table_data = {
    'Nom': [],
    'Client ID': [],
    'Mois 1': [],
    'Mois 2': [],
    'Prédiction Mois 2': [],
    'Ecart-type': []
}


def get_customer_data(client_id, month):
    query = f"SELECT date, valeur FROM ma_table WHERE client_id='{client_id}' AND strftime('%Y-%m', date)='{month}'"
    c.execute(query)
    data = c.fetchall()
    return data

df_table = pd.DataFrame(data=table_data)

# Chargement des données dans un dataframe Pandas
df = pd.read_sql_query("SELECT *, strftime('%Y-%m', date) as mois FROM ma_table", conn, parse_dates=['date'])

# Sélection des clients
selected_clients = []
if 'client_id' in df.columns:
    selected_clients = st.sidebar.multiselect("Sélectionnez un ou plusieurs clients :", df['client_id'].unique(),
                                              key=("client_select_" + str(
                                                  selected_clients)) if selected_clients else "client_select_default")

# Sélection des mois à comparer
selected_months = []
if 'mois' in df.columns:
    selected_months = st.sidebar.multiselect("Sélectionnez deux mois à comparer :", df['mois'].unique(),
                                             key="months_select_" + "_".join(selected_months))

# Vérifier si deux mois ont été sélectionnés
if len(selected_months) != 2:
    st.warning("Sélectionnez exactement deux mois ou arrêtez la comparaison.")
else:
    # Boucle pour tous les clients sélectionnés
    for client_id in selected_clients:
        # Boucle pour toutes les paires de mois sélectionnées
        for i in range(len(selected_months) - 1):
            month_1 = selected_months[i]
            month_2 = selected_months[i + 1]

            # Récupération des données du client pour les deux mois sélectionnés
            data_month_1 = get_customer_data(client_id, month_1)
            data_month_2 = get_customer_data(client_id, month_2)

            # Création d'un DataFrame pour stocker les données de prédiction
            prediction_data = {
                'Date': [],
                'Prediction': []
            }
            df_prediction = pd.DataFrame(data=prediction_data)

            # Prédiction de la consommation pour le mois 2 à partir des données du mois 1
            model = pm.auto_arima([data[1] for data in data_month_1], seasonal=True, m=12)
            prediction = model.predict(n_periods=len(data_month_2))

            # Ajout des données de prédiction au DataFrame
            for j in range(len(prediction)):
                prediction_data = {
                    'Date': data_month_2[j][0],
                    'Prediction': prediction[j]
                }
                df_prediction = pd.concat([df_prediction, pd.DataFrame(data=prediction_data, index=[0])],
                                          ignore_index=True)

            # Calcul de la consommation réelle pour le mois 2
            consommation_month_2 = sum([data[1] for data in data_month_2])

            # Calcul de la consommation prédite pour le mois 2
            consommation_month_2_pred = sum(df_prediction['Prediction'])

            # Calcul de l'écart-type des consommations des deux mois
            ecart_type = consommation_month_2_pred - consommation_month_2

            # Calcul du taux d'évolution des prédictions et des données réelles
            if consommation_month_2 != 0:
                evolution_rate = ecart_type / consommation_month_2
            else:
                evolution_rate = float('nan')  # ou toute autre valeur qui convient à votre cas d'utilisation

            new_row = {
                'Client ID': client_id,
                'Mois 1': month_1,
                'Mois 2': month_2,
                'Consommation Mois 2': consommation_month_2,
                'Consommation Prédite Mois 2': consommation_month_2_pred,
                'Ecart-type': ecart_type,
                'Taux d\'évolution': evolution_rate
            }

            df_table = pd.concat([df_table, pd.DataFrame(data=new_row, index=[0])], ignore_index=True)

# Affichage du tableau modifié
st_table = st.experimental_data_editor(df_table, num_rows="dynamic")
st.write(st_table)

import plotly.graph_objs as go

# Filtrer les données pour les clients sélectionnés
filtered_data_pred = df_table[(df_table['Client ID'].isin(selected_clients)) & (df_table['Ecart-type'] != 0)]
filtered_data_real = df_table[(df_table['Client ID'].isin(selected_clients)) & (df_table['Ecart-type'] == 0)]

# Créer un objet Figure de Plotly
fig = go.Figure()

# Ajouter une barre pour chaque client pour les prévisions et les données réelles
for client in selected_clients:
    # Ajouter les données prédites
    data_pred = filtered_data_pred[filtered_data_pred['Client ID'] == client]
    fig.add_trace(go.Bar(name=f"Prédiction {client}", x=data_pred['Mois 2'], y=data_pred['Consommation Prédite Mois 2'],
                         error_y=dict(type='data', array=data_pred['Ecart-type'], visible=True)))

    # Ajouter les données réelles
    data_real = filtered_data_real[filtered_data_real['Client ID'] == client]
    fig.add_trace(go.Bar(name=f"Données réelles {client}", x=data_real['Mois 2'], y=data_real['Consommation Mois 2']))

# Ajouter les titres d'axes et le titre du graphique
fig.update_layout(title='Prévisions de consommation', xaxis_title='Mois', yaxis_title='Consommation (kWh)')

# Afficher le graphique
st.plotly_chart(fig)
