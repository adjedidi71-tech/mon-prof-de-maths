import streamlit as st

from supabase import create_client

@st.cache_resource
def connexion_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

supabase = connexion_supabase()
  
@st.cache_resource
def connexion_supabase_privee():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_SECRET_KEY"]
    )

supabase_privee = connexion_supabase_privee()

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

import secrets
import string

def generer_code_reprise():
    caracteres = string.ascii_uppercase + string.digits
    return "".join(
        secrets.choice(caracteres) for _ in range(16)
    )
    
def sauvegarder_serie(exercices):
    code = generer_code_reprise()
    try:
        supabase_privee.table("series_exercices").insert({
            "code_reprise": code,
            "exercices": exercices,
            "reponses": {},
            "progression": 0
        }).execute()
        return code
    except Exception as e:
        raise RuntimeError(
            f"Erreur Supabase : {type(e).__name__}"
        ) from None

if st.button("Tester la sauvegarde Supabase"):
    exercices_test = [
        {
            "enonce": "Calculer 3 × 4",
            "correction": "12"
        }
    ]

    try:
        code = sauvegarder_serie(exercices_test)
        st.success("Sauvegarde réussie !")
        st.code(code)
    except Exception as e:
        st.error("La sauvegarde a échoué.")
        st.write("Type d'erreur :", type(e).__name__)

def recuperer_serie(code):
    resultat = (
        supabase_privee.table("series_exercices")
        .select("code_reprise, exercices, reponses, progression")
        .eq("code_reprise", code.strip().upper())
        .limit(1)
        .execute()
    )
    if resultat.data:
        return resultat.data[0]
    return None


st.subheader("Reprendre mes exercices")

code_saisi = st.text_input(
    "Saisis ton code de reprise"
)

if st.button("Retrouver mes exercices"):
    if not code_saisi.strip():
        st.warning("Saisis d'abord ton code.")
    else:
        try:
            serie = recuperer_serie(code_saisi)
            if serie:
                st.success("Série retrouvée !")
                st.json(serie["exercices"])
            else:
                st.warning("Aucune série trouvée avec ce code.")
        except Exception:
            st.error("Impossible de récupérer la série.")

if st.button("Générer mes exercices"):
    st.success("Configuration enregistrée !")
    st.write("Chapitre :", chapitre)
    st.write("Sous-chapitre :", partie)
    st.write("Type :", type_exercice)
    st.write("Difficulté :", difficulte, "/5")
    st.write("Nombre d'exercices :", nombre)
    st.info("La génération IA sera ajoutée ensuite.")

