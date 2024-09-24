import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Charger ou créer un fichier CSV pour stocker les tâches
def charger_donnees():
    try:
        return pd.read_csv('taches.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['Nom', 'Date Limite', 'Priorité'])

# Sauvegarder les données dans le fichier CSV
def sauvegarder_donnees(df):
    df.to_csv('taches.csv', index=False)

# Afficher les tâches du jour
def taches_du_jour(df):
    aujourd_hui = datetime.now().date()
    return df[pd.to_datetime(df['Date Limite']).dt.date == aujourd_hui]

# Fonction principale de l'application
def main():
    st.title("Gestionnaire de Tâches")
    
    # Charger les données
    df = charger_donnees()

    # Formulaire pour ajouter une tâche
    st.sidebar.header("Ajouter une nouvelle tâche")
    nom = st.sidebar.text_input("Nom de la Tâche")
    date_limite = st.sidebar.date_input("Date Limite", min_value=datetime.now().date())
    priorite = st.sidebar.selectbox("Priorité", [1, 2, 3])

    if st.sidebar.button("Ajouter Tâche"):
        nouvelle_tache = {'Nom': nom, 'Date Limite': date_limite.strftime('%Y-%m-%d'), 'Priorité': priorite}
        df = df.append(nouvelle_tache, ignore_index=True)
        sauvegarder_donnees(df)
        st.sidebar.success("Tâche ajoutée avec succès!")

    # Afficher les tâches
    st.header("Toutes les Tâches")
    st.dataframe(df.sort_values(by=['Date Limite', 'Priorité']))

    # Afficher les suggestions pour aujourd'hui
    st.header("Tâches pour Aujourd'hui")
    taches_aujourdhui = taches_du_jour(df)
    if not taches_aujourdhui.empty:
        st.table(taches_aujourdhui.sort_values(by=['Priorité']))
    else:
        st.write("Aucune tâche pour aujourd'hui.")

if __name__ == "__main__":
    main()

