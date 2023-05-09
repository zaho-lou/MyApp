import streamlit as st
import sqlite3
import hashlib
import secrets


# Fonctions pour la base de données
# Chargement du fichier CSS



def create_usertable():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, salt TEXT)')
    conn.commit()
    conn.close()


def add_userdata(username, password, salt):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users(username, password, salt) VALUES (?,?,?)', (username, password, salt))
    conn.commit()
    conn.close()


def get_userdata(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    data = c.fetchone()
    conn.close()
    return data


# Fonction de hachage de mot de passe

def hash_password(password, salt):
    hash_object = hashlib.sha256(salt.encode() + password.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


# Fonction de création de sel

def create_salt():
    return secrets.token_hex(16)


def login():


    st.title("Page de connexion")
    st.markdown("""
           <style>
               @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
               %s
           </style>
           """ % open("style.css").read(), unsafe_allow_html=True)
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        result = c.fetchone()
        conn.close()

        if result:
            user_id, username, hashed_password, salt = result
            if hashed_password == hash_password(password, salt):
                # Si l'utilisateur est connecté avec succès, initialiser l'attribut 'logged_in'
                st.session_state.logged_in = True
                st.success("Connecté avec succès")
                return True

        st.error("Nom d'utilisateur ou mot de passe incorrect")
    return False

# Fonction pour la page d'inscription

def signup():
    st.title("Page d'inscription")
    st.markdown("""
               <style>
                   @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
                   %s
               </style>
               """ % open("style.css").read(), unsafe_allow_html=True)
    # Création de la table utilisateurs
    create_usertable()

    # Création du formulaire d'inscription
    new_username = st.text_input("Nom d'utilisateur", key='new_username')
    new_password = st.text_input("Mot de passe", type='password', key='new_password')

    if st.button("S'inscrire"):
        salt = create_salt()
        hashed_password = hash_password(new_password, salt)
        add_userdata(new_username, hashed_password, salt)
        st.success("Compte créé avec succès")
        st.info("Veuillez vous connecter pour accéder à l'application")

        # Une fois le compte créé,

def main():





    # Vérification de l'authentification de l'utilisateur
    if 'user' not in st.session_state:
        st.session_state['user'] = False

    # Affichage de la page de connexion si l'utilisateur n'est pas connecté
    if not st.session_state['user']:
        if login():
            st.session_state['user'] = True
        else:
            signup()


if __name__ == "__main__":
    main()