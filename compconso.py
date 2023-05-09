import sqlite3
import pandas as pd
import streamlit as st
import plotly.graph_objs as go


def main():
    # Connexion à la base de données
    conn = sqlite3.connect('ma_base1.db')
    c = conn.cursor()

    # Création d'un DataFrame vide pour stocker les données du tableau
    table_data = {
        'Nom': [],
        'Référence': [],
        'Mois 1': [],
        'Mois 2': [],
        'Consommation Mois 1': [],
        'Consommation Mois 2': [],
        'Ecart-type': [],
        'Taux d\'évolution': []
    }

    def get_customer_data(reference, month):
        query = f"SELECT date, valeur FROM client WHERE reference='{reference}' AND strftime('%Y-%m', date)='{month}'"
        c.execute(query)
        data = c.fetchall()
        return data

    df_table = pd.DataFrame(data=table_data)

    # Chargement des données dans un dataframe Pandas
    df = pd.read_sql_query("SELECT *, strftime('%Y-%m', date) as mois FROM client", conn, parse_dates=['date'])

    # Sélection des clients
    selected_clients = []

    selected_clients = st.sidebar.multiselect("Sélectionnez un ou plusieurs clients :", df['reference'].unique(),
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
        for reference in selected_clients:
            # Boucle pour toutes les paires de mois sélectionnées
            for i in range(len(selected_months) - 1):
                month_1 = selected_months[i]
                month_2 = selected_months[i + 1]

                # Récupération des données du client pour les deux mois sélectionnés
                data_month_1 = get_customer_data(reference, month_1)
                data_month_2 = get_customer_data(reference, month_2)

                # Calcul de la consommation pour chaque mois
                if data_month_1:
                    consommation_month_1 = sum([data[1] for data in data_month_1])
                else:
                    consommation_month_1 = 0

                consommation_month_2 = sum([data[1] for data in data_month_2])

                # Calcul de l'écart-type des consommations des deux mois

                ecart_type = consommation_month_2 - consommation_month_1 if consommation_month_1 is not None else None

                # Calcul du taux d'évolution des consommations des deux mois
                if consommation_month_1 != 0:
                    evolution_rate = round((ecart_type / consommation_month_1) * 100, 2)
                else:
                    evolution_rate = float('nan')  # ou toute autre valeur qui convient à votre cas d'utilisation

                new_row = {
                    'Référence': reference,
                    'Mois 1': month_1,
                    'Mois 2': month_2,
                     'Consommation Mois 1': consommation_month_1,
                     'Consommation Mois 2': consommation_month_2,
                     'Ecart-type': ecart_type,
                     'Taux d\'évolution': f"{evolution_rate*1:.2f} %"
                }

                df_table = pd.concat([df_table, pd.DataFrame(data=new_row, index=[0])], ignore_index=True)

    # Affichage du tableau modifié

    st_table = st.experimental_data_editor(df_table, num_rows="dynamic")



# Filtrer les données pour les clients sélectionnés
    filtered_data = df_table[df_table['Référence'].isin(selected_clients)]

# Créer un objet Figure de Plotly
    fig = go.Figure()

# Ajouter une barre pour chaque client
    fig.add_trace(go.Bar(x=filtered_data['Référence'], y=filtered_data['Ecart-type'],
                     marker_color=filtered_data['Ecart-type'],  # Ajouter la couleur
                     text=filtered_data['Ecart-type'],  # Ajouter les valeurs sur chaque barre
                     textposition='auto'  # Positionner les valeurs automatiquement
                       ))

# Mettre à jour la mise en page du graphe
    fig.update_layout(title='Comparaison des écarts-types pour les clients sélectionnés',
                  xaxis_title='Référence',
                  yaxis_title='Ecart-type')

# Afficher le graphe
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
