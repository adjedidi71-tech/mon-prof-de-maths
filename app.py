
import streamlit as st

st.set_page_config(
    page_title="Mon Prof de Maths",
    page_icon="📐"
)

st.title("Mon Prof de Maths")
st.write("Prépare tes exercices de mathématiques !")

chapitres = {
    "Expressions littérales": [
        "Écrire une expression",
        "Calculer une expression",
        "Réduire une expression",
        "Distributivité",
        "Tester une égalité"
    ],
    "Fractions": [
        "Comparer des fractions",
        "Additionner et soustraire"
    ],
    "Nombres relatifs": [
        "Comparer les nombres",
        "Additionner et soustraire"
    ]
}

chapitre = st.selectbox(
    "Chapitre",
    list(chapitres.keys())
)

partie = st.selectbox(
    "Sous-chapitre",
    chapitres[chapitre]
)

col1, col2 = st.columns(2)

with col1:
    type_exercice = st.selectbox(
        "Type d'exercice",
        [
            "Mes automatismes",
            "Je m'entraîne",
            "Je résous des problèmes"
        ]
    )

with col2:
    difficulte = st.selectbox(
        "Difficulté",
        [1, 2, 3, 4, 5],
        index=2
    )

nombre = st.selectbox(
    "Nombre d'exercices",
    [1, 2, 3, 4, 5],
    index=2
)

if st.button("Générer mes exercices"):
    st.success("Configuration enregistrée !")
    st.write("Chapitre :", chapitre)
    st.write("Sous-chapitre :", partie)
    st.write("Type :", type_exercice)
    st.write("Difficulté :", difficulte, "/5")
    st.write("Nombre d'exercices :", nombre)
    st.info("La génération IA sera ajoutée ensuite.")

