import sqlite3
import streamlit as st
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import folium

from streamlit_folium import folium_static


def main():
    conn = sqlite3.connect('ma_base1.db')
    c = conn.cursor()

    # Fonction pour récupérer les informations de géolocalisation et de nom du client
    def get_client_by_id(client_id):
        c.execute("SELECT latitude, longitude, nom FROM client WHERE client_id=?", (client_id,))
        result = c.fetchone()
        return result

    def get_client_by_ref(reference):
        c.execute("SELECT latitude, longitude, nom FROM client WHERE reference=?", (reference,))
        result = c.fetchone()
        return result

    # Récupération de toutes les références de clients
    c.execute("SELECT DISTINCT reference FROM client")
    references = [r[0] for r in c.fetchall()]

    # Récupération de tous les IDs de clients
    c.execute("SELECT DISTINCT client_id FROM client")
    client_ids = [r[0] for r in c.fetchall()]

    # Création de la carte centrée sur Béjaia
    carte = folium.Map(location=[36.7602, 5.0554], zoom_start=10)

    # Affichage de la carte dans le navigateur
    carte.save('bejaia.html')

    # Récupération du choix de l'utilisateur : recherche par ID ou par référence
    choix_recherche = st.sidebar.selectbox("Rechercher un client par :", ("ID", "Référence"))

    if choix_recherche == "ID":
        # Récupération de l'ID du client saisi par l'utilisateur
        client_id = st.sidebar.selectbox('Sélectionnez un ID de client :', client_ids)
        if client_id:
            # Afficher la géolocalisation et le nom du client sur la carte
            client_info = get_client_by_id(client_id)
            if client_info:
                # Création d'un marqueur pour le client
                marker = folium.Marker(location=client_info[:2], tooltip="Client",
                                       popup=folium.Popup(
                                           f"Nom du client : {client_info[2]}<br>ID du client : {client_id}"))
                marker.add_to(carte)
            else:
                st.warning("Le client n'a pas de géolocalisation enregistrée dans la base de données.")
    else:
        # Récupération de la référence du client saisi par l'utilisateur
        reference = st.sidebar.selectbox('Sélectionnez une référence de client :', references)
        if reference:
            # Afficher la géolocalisation et le nom du client sur la carte
            client_info = get_client_by_ref(reference)
            if client_info:
                # Création d'un marqueur pour le client
                marker = folium.Marker(location=client_info[:2], tooltip="Client",
                                       popup=folium.Popup(
                                           f"Nom du client : {client_info[2]}<br>Référence du client : {reference}"))
                marker.add_to(carte)
            else:
                st.warning("Le client n'a pas de géolocalisation enregistrée dans la base de données.")

    #

    # Affichage de la carte
    folium_static(carte)

    # Fermeture de la connexion à la base de données
    c.close()
    conn.close()


if __name__ == "__main__":
    main()
