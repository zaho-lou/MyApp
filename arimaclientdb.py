import streamlit as st
import pandas as pd
import sqlite3
import calendar
def main():
# Connexion à la base de données SQLite3
 conn = sqlite3.connect('ma_base1.db')

# Lecture des données de consommation de la table 'ma_table'
 df_cons = pd.read_sql_query("SELECT * FROM client", conn, index_col='date', parse_dates=True)

# Lecture des données de prédiction depuis le fichier 'predictions.csv'

 df_pred = pd.read_sql_query("SELECT * FROM pred", conn, index_col='date', parse_dates=True)

# Fermeture de la connexion à la base de données
 conn.close()


# Liste des clients disponibles
 clients_list = df_cons['reference'].unique().tolist()

# Sélection de l'ID du client
 selected_client = st.sidebar.selectbox('Sélectionner une reference:', clients_list)

# Récupération des données de consommation du client sélectionné
 df_cons = df_cons.loc[df_cons['reference'] == selected_client][['valeur']].dropna()

# Récupération des données de prédiction du client sélectionné
 df_pred = df_pred.loc[df_pred['reference'] == selected_client][['prevision']].dropna()

# Configuration de l'affichage de Pandas
 pd.options.display.float_format = '{:,.0f}'.format

# Affichage de la prédiction pour toutes les données
 st.write('Prévision de la consommation future des clients:')
 st.line_chart(pd.concat([df_cons, df_pred], axis=1).rename(columns={'valeur': 'Historique', 'prevision': 'Prévision'}))

# Affichage des données de prédiction dans un tableau
 st.write('Données de prédiction :')
 df_future = df_pred.reset_index().rename(columns={'date': 'Date', 'prevision': 'Prévision'})
 df_future['Date'] = pd.to_datetime(df_future['Date'])
 df_future['Year'] = df_future['Date'].dt.strftime('%Y')
 df_future['Month'] = df_future['Date'].dt.month.apply(lambda x: calendar.month_name[x]).str.capitalize()

# Tri des données par an et mois
 df_future = df_future.sort_values(by=['Year', 'Date'])
 df_future['Month'] = pd.Categorical(df_future['Month'], categories=list(calendar.month_name)[1:], ordered=True)
 df_future = df_future.sort_values(['Year', 'Month'], ascending=[True, True])

 df_pivot = df_future.pivot_table(values='Prévision', index='Year', columns=df_future['Month'])

 st_table = st.experimental_data_editor(df_pivot, height=400, num_rows="dynamic")

# Fusion des données de consommation et de prédiction totales par ann
 df_future['Date'] = pd.to_datetime(df_future['Date'])

 df_total = pd.concat([df_cons, df_pred], axis=1)
 df_total.index = pd.to_datetime(df_total.index)
 df_total['Year'] = df_total.index.to_series().dt.year


 df_total['Month'] = df_total.index.strftime('%m-%B').str.capitalize()


# Tri des données par an et mois
 df_total = df_total.sort_values(by=['Year', 'Month'])
 df_total['Month'] = pd.Categorical(df_total['Month'], categories=list(calendar.month_name)[1:], ordered=True)
 df_total = df_total.sort_values(['Year', 'Month'], ascending=[True, True])

# Pivot table pour obtenir la consommation totale par an
 df_pivot = df_total.pivot_table(values='valeur', index='Year', columns=df_total['Month'])

# Ajout de la colonne de total annuel
 df_pivot['Total'] = df_pivot.sum(axis=1)


# Affichage de la consommation et de la prédiction totales
 st.write('Consommation et prévision totales par année :')
 chart_data = pd.DataFrame({'Consommation': df_total['valeur'], 'Prévision': df_total['prevision']})
 st.bar_chart(chart_data, height=400)
if __name__ == "__main__":
    main()