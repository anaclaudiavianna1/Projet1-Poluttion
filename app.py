import streamlit as st

st.set_page_config(page_title="Projet Streamlit - Qualité de l'Air", layout="wide")

# ----- Header en HTML -----
st.markdown("""
    <div style='text-align:center'>
        <h1>Projet Streamlit - Qualité de l'Air</h1>
        <h3>Analyse des données de pollution atmosphérique</h3>
    </div>
""", unsafe_allow_html=True)

st.caption("Utilisez le menu de pages (à gauche) pour accéder à l'Exploration et aux Corrélations.")

# --------Textbox--------
nom = st.text_input("Entrer votre nom :")
if nom:
    st.write(f"Merci {nom}")

# ------- ComboBox------
options = ['Afficher la description du projet',
           'Voir les objectifs',
           'Afficher les directives principales']
choix = st.selectbox('Veuillez choisir une option :', options)

if choix == 'Afficher la description du projet':
    st.info("Le projet consiste à créer une application Streamlit interactive pour analyser la qualité de l’air au Canada.")
elif choix == 'Voir les objectifs':
    st.success("Objectifs : Explorer les données, étudier les corrélations, et présenter des visualisations interactives.")
elif choix == 'Afficher les directives principales':
    st.warning("Directives : Nettoyage des données, analyse descriptive et étude de corrélation entre les variables.")


# -----RadioButton----
choix2 = st.radio('Choississez votre ville :', ['Montréal', 'Longueiul', 'Laval', 'Quebec City'])
st.write(f'Votre ville est : {choix2}')

# -------Checkbox ----
activer_filtre = st.checkbox(f"Filtrer l’analyse par la ville sélectionnée ({choix2})")
if activer_filtre:
    st.session_state["ville_filtre_active"] = True
    st.session_state["ville_selectionnee"] = choix2
    st.success(f"Filtre activé : {choix2}. Les pages *Exploration* et *Corrélations* peuvent utiliser ce filtre.")
else:
    st.session_state["ville_filtre_active"] = False
    st.session_state["ville_selectionnee"] = None


# ------Slider-------
age = st.slider("Votre âge :", 0, 100, 20)
st.write(f'Votre âge est : {age}')

text = st.text_area("Votre commentaire svp : ")
if text:
    st.write(f'Commentaire : {text}')

# -----Button----

st.button('Ok')
