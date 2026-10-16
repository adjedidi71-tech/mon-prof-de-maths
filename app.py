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
                for numero, exercice in enumerate(serie["exercices"], 1):
                    st.subheader(f"Exercice {numero}")
                    st.write(exercice["enonce"])

                    with st.expander("Voir la correction"):
                        st.write(exercice["correction"])

            else:
                st.warning("Aucune série trouvée avec ce code.")
        except Exception:
            st.error("Impossible de récupérer la série.")

import random

def generer_exercice(chapitre, partie, difficulte, type_exercice):
    maximum = 5 * difficulte + 5
    a = random.randint(2, maximum)
    b = random.randint(2, maximum)

    if chapitre == "Fractions":
        enonce = f"Calcule et simplifie : {a}/{b} + {a}/{b}"
        correction = f"{a}/{b} + {a}/{b} = {2*a}/{b}. Simplifie si possible."

    elif chapitre == "Nombres relatifs":
        enonce = f"Calcule : (-{a}) + {b}"
        correction = f"(-{a}) + {b} = {b-a}"

    else:
        enonce = f"Calcule la valeur de {a} × x + {b} pour x = 3."
        correction = f"{a} × 3 + {b} = {3*a+b}"

    return {"enonce": enonce, "correction": correction}


if st.button("Générer mes exercices"):
    exercices = [
        generer_exercice(chapitre, partie, difficulte, type_exercice)
        for _ in range(nombre)
    ]

    try:
        code = sauvegarder_serie(exercices)
        st.success("Exercices générés et sauvegardés !")
        st.write("Ton code de reprise :")
        st.code(code)
    except Exception:
        st.error("Sauvegarde impossible.")

    for numero, exercice in enumerate(exercices, start=1):
        st.subheader(f"Exercice {numero}")
        st.write(exercice["enonce"])

        with st.expander("Voir la correction"):
            st.write(exercice["correction"])

