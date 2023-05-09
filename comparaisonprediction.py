import sqlite3
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
# Connexion à la base de données
def main ():
 conn = sqlite3.connect('ma_base1.db')
 c = conn.cursor()

# Création d'un DataFrame vide pour stocker les données du tableau
 table_data = {
    'Méthode': ['SARIMA'],
    'Client ID': [],
    'Mois actuel': [],
    'Mois prédit': [],
    'Consommation Mois actuel': [],
    'Consommation Mois prédit': [],
    'Ecart-type': [],
    'Taux d\'évolution': []
 }
# Création d'un DataFrame vide pour stocker les données du tableau final
 df_table = pd.DataFrame(columns=table_data.keys())

# Chargement des données dans un dataframe Pandas
 df = pd.read_sql_query("SELECT *, strftime('%Y-%m', date) as mois1 FROM client", conn, parse_dates=['date'])
# Chargement des données de la table de prédiction dans un dataframe Pandas
 prediction = pd.read_sql_query("SELECT *, strftime('%Y-%m', date) as mois2 FROM prediction", conn, parse_dates=['date'])

# Sélection des clients
 selected_clients = []
 if 'reference' in df.columns:
     selected_clients = st.sidebar.multiselect("Sélectionnez un ou plusieurs clients :", df['reference'].unique(),
                                     key=("client_select_" + str(
                                         selected_clients)) if selected_clients else "client_select_default")

 # Sélection des mois à comparer
 selected_month1 = []
 selected_month2 = []
 if 'mois1' in df.columns:
     selected_month1 = st.sidebar.multiselect("Sélectionnez le mois 1 à comparer :", df['mois1'].unique(),
                                             key="months_select_1")
 if 'mois2' in prediction.columns:
     selected_month2 = st.sidebar.multiselect("Sélectionnez le mois 2 à comparer :", prediction['mois2'].unique(),
                                             key="months_select_2")

# Vérifier si deux mois ont été sélectionnés
 if len(selected_month1) != 1 or len(selected_month2) != 1:
    st.warning("Sélectionnez exactement deux mois ou arrêtez la comparaison.")
 else:
    # Boucle pour tous les clients sélectionnés
     for client_id in selected_clients:
         month_1 = selected_month1[0]
         month_2 = selected_month2[0]

        # Récupération des données du client pour les deux mois sélectionnés
         data_month_1 = df[(df['reference'] == client_id) & (df['mois1'] == month_1)]
         data_month_2 = prediction[(prediction['reference'] == client_id) & (prediction['mois2'] == month_2)]

        # Calcul de l'écart-type et du taux d'évolution
         if not data_month_1.empty and not data_month_2.empty:
             conso_month_1 = data_month_1['valeur'].values[0]
             conso_month_2 = data_month_2['prediction'].values[0]
             ecart_type = abs(conso_month_2 - conso_month_1) / conso_month_1 * 100
             taux_evolution = (conso_month_2 - conso_month_1) / conso_month_1 * 100
         else:
             ecart_type = 0
             taux_evolution = 0

         new_row = {
             'Reference': client_id,
             'Mois actuel': month_1,
             'Mois prédit': month_2,
             'Consommation Mois actuel': conso_month_1,
             'Consommation Mois prédit': conso_month_2,
             'Ecart-type': ecart_type,
             'Taux d\'évolution': f"{taux_evolution * 1:.2f} %"
         }

         df_table = pd.concat([df_table, pd.DataFrame(data=new_row, index=[0])], ignore_index=True)

     import plotly.graph_objs as go

    # Filtrer les données pour les clients sélectionnés
     filtered_data = df_table[df_table['Reference'].isin(selected_clients)]
     st.write(filtered_data)

    # Créer un objet Figure de Plotly
     fig = go.Figure()

    # Ajouter une barre pour chaque client
     fig.add_trace(go.Bar(x=filtered_data['Reference'], y=filtered_data['Ecart-type'],
                         marker_color=filtered_data['Ecart-type'],  # Ajouter la couleur
                         text=filtered_data['Ecart-type'],  # Ajouter les valeurs sur chaque barre
                         textposition='auto'  # Positionner les valeurs automatiquement
                         ))

    # Mettre à jour la mise en page du graphe
     fig.update_layout(title='Comparaison des écarts-types pour les clients sélectionnés',
                       xaxis_title='Reference',
                       yaxis_title='Ecart-type')

    # Afficher le graphe
     st.plotly_chart(fig)
if __name__ == "__main__":
     main()