import streamlit as st
from authen import login, signup
import dashb
import authen
import visualisationTab
import visualisationgraphtab
import geoloc
import sarimaclientcsv
import compconso
import comparaisonprediction
from PIL import Image
import  arimaclientdb



logo = Image.open('sonalgaz.jpg')
logo = logo.convert('RGB')  # convert to RGB mode



def main():

    st.set_page_config(
        page_title='Sonalgaz',
        page_icon=logo,
        layout='wide')

    st.markdown('''
      <style>
        /* Style du corps de la page */
        
        body {
               background-color: #FFDAB9;
               font-family: Arial, sans-serif;
               font-size: 16px;
               margin: 0;
               padding: 0;
        }

        /* Style du titre */
        h1 {
            font-size: 36px;
            font-weight: bold;
            color: #333333;
            text-align: center;
            margin-top: 50px;
            margin-bottom: 50px;
        }

        /* Style des boutons */
        button {
            background-color: #87cefa;
            color: #ffffff;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            display: block;
            margin: 0 auto;

         }


        button:hover {
            background-color: #0056b3;
        }

        /* Style du menu latéral */
        .sidebar .sidebar-content {
            background-color: #f0f0f0;
            padding: 20px;
            margin-top: 50px;
        }

        .sidebar .sidebar-content .sidebar-section {
            margin-top: 20px;
            margin-bottom: 20px;
        }

        .sidebar .sidebar-content .sidebar-section h2 {
            font-size: 20px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 10px;
        }

        .sidebar .sidebar-content .sidebar-section ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }

        .sidebar .sidebar-content .sidebar-section ul li a {
            color: #333333;
            text-decoration: none;
            font-size: 16px;
            padding: 10px 20px;
            display: block;
            transition: background-color 0.3s ease;
        }

        .sidebar .sidebar-content .sidebar-section ul li a:hover {
            background-color: #e6e6e6;
        }
        </style>
    ''', unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        menu_items = ['Dashboard', 'Authentification', 'Visualisation', 'Map', 'Prediction', 'Comparaison',
                      'Déconnexion']
        st.sidebar.title('Menu')
        choice = st.sidebar.selectbox('Sélectionner une page', menu_items)

        if choice == 'Dashboard':
            dashb.main()
        elif choice == 'Authentification':
            if __name__ == '__main__':
                authen.main()
        elif choice == 'Visualisation':
            sub_menu_items = ['Tableau', 'Graphique']
            sub_choice = st.sidebar.selectbox('Sélectionner un type', sub_menu_items)
            if sub_choice == 'Tableau':
                visualisationTab.main()
            elif sub_choice == 'Graphique':

                visualisationgraphtab.main()
        elif choice =='Map':
            geoloc.main()


        elif choice == 'Comparaison':
            sub_menu_items = ['consommation', 'consommationprediction']
            sub_choice = st.sidebar.selectbox('Select a type', sub_menu_items)
            if sub_choice == 'consommation':

                compconso.main()
            elif sub_choice == 'consommationprediction':

                comparaisonprediction.main()
        elif choice == 'Prediction':
            sub_menu_items = ['SARIMA', 'ARIMA']
            sub_choice = st.sidebar.selectbox('Select a type', sub_menu_items)
            if sub_choice == 'SARIMA':
                sarimaclientcsv.main()
            elif sub_choice == 'ARIMA':
                arimaclientdb.main()
        elif choice == 'Déconnexion':
            st.session_state.logged_in = False

    else:
        menu_items = {'Login': login, 'Signup': signup}
        st.sidebar.title('Menu')
        choice = st.sidebar.radio('', list(menu_items.keys()))
        if menu_items[choice]():
            # Si la fonction de connexion renvoie True, cela signifie que l'utilisateur est connecté avec succès
            st.session_state.logged_in = True


if __name__ == "__main__":
    main()
