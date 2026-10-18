import streamlit as st

from supabase import create_client

def connexion_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

if "supabase_client" not in st.session_state:
    st.session_state["supabase_client"] = connexion_supabase()

supabase = st.session_state["supabase_client"]
  
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

st.subheader("Mon compte élève")
if st.session_state.pop("vider_champs_connexion", False):
   st.session_state["email_connexion"] = ""
   st.session_state["mdp_connexion"] = ""
with st.expander("Créer mon compte"):
    with st.form("formulaire_inscription"):
        email = st.text_input("Adresse e-mail")
        pseudo = st.text_input("Pseudonyme (facultatif)")
        mot_de_passe = st.text_input(
            "Mot de passe",
            type="password"
        )
        confirmer_mdp = st.text_input(
            "Confirmer le mot de passe",
            type="password"
        )
        inscrire = st.form_submit_button("Créer mon compte")

    if inscrire:
        if not email.strip() or not mot_de_passe:
            st.warning("Renseigne ton e-mail et ton mot de passe.")
        elif mot_de_passe != confirmer_mdp:
            st.error("Les mots de passe sont différents.")
        elif len(mot_de_passe) < 8:
            st.warning("Utilise au moins 8 caractères.")
        else:
            try:
                client_inscription = create_client(
                    st.secrets["SUPABASE_URL"],
                    st.secrets["SUPABASE_KEY"]
                )
                client_inscription.auth.sign_up({
                    "email": email.strip(),
                    "password": mot_de_passe,
                    "options": {
                        "data": {
                            "pseudo": pseudo.strip()
                        }
                    }
                })
                st.success(
                    "Inscription demandée. Consulte ton e-mail "
                    "pour confirmer ton compte."
                )
            except Exception:
                st.error(
                    "Inscription impossible. Vérifie les informations "
                    "ou réessaie plus tard."
                )

with st.expander("Se connecter"):
    with st.form("formulaire_connexion"):
        email_connexion = st.text_input(
            "Ton adresse e-mail",
            key="email_connexion"
        )

        mdp_connexion = st.text_input(
            "Ton mot de passe",
            type="password",
            key="mdp_connexion"
       )
        connexion = st.form_submit_button("Se connecter")

    if connexion:
        try:
            client_connexion = supabase
            resultat = client_connexion.auth.sign_in_with_password({
                "email": email_connexion.strip(),
                "password": mdp_connexion
            })

            if resultat.user and resultat.session:
                st.session_state["eleve_id"] = resultat.user.id
                st.session_state["session_eleve"] = resultat.session
                st.success("Connexion réussie !")
            else:
                st.error("Connexion impossible.")
        except Exception:
            st.error("E-mail ou mot de passe incorrect.")

if st.session_state.get("eleve_id"):
    st.write("Tu es connecté à ton compte élève.")

    if st.button("Se déconnecter"):        
        supabase.auth.sign_out()
        st.session_state.pop("supabase_client", None)
        st.session_state.pop("eleve_id", None)
        st.session_state.pop("session_eleve", None)
        st.session_state.pop("exercices_actuels", None)
        st.session_state.pop("code_actuel", None)
        st.session_state["vider_champs_connexion"] = True
        st.rerun()

chapitres = {
    "1. Opérations": [
        "Addition, soustraction et multiplication de nombres décimaux",
        "Division euclidienne, multiples et diviseurs",
        "Division par un nombre décimal",
        "Priorités opératoires",
        "Distributivité simple"
    ],
    "2. Nombres relatifs": [
        "Les nombres relatifs",
        "Repérage sur une droite graduée",
        "Repérage dans un repère orthogonal du plan",
        "Comparaison de nombres relatifs"
    ],
    "3. Addition, soustraction de nombres relatifs": [
        "Simplification d'écriture",
        "Addition de nombres relatifs",
        "Soustraction de deux nombres relatifs",
        "Enchaînement d'additions et de soustractions"
    ],
    "4. Nombres rationnels": [
        "Comparaison de fractions",
        "Comparaison de proportions",
        "Addition et soustraction de fractions",
        "Résolution de problèmes avec des fractions"
    ],
    "5. Puissances": [
        "Carré et cube d'un nombre",
        "Carrés des entiers de 0 à 12",
        "Enchaînement de calculs avec des puissances simples",
        "Valeur d'une expression contenant une puissance"
    ],
    "6. Calcul littéral": [
        "Produire des expressions littérales",
        "Calcul de la valeur d'une expression littérale",
        "Reconnaître une somme, un produit",
        "Utilisation de la distributivité simple",
        "Test d'une égalité",
        "Résolution d'une équation du 1er degré"
    ],
    "7. Représentation de l'espace": [
        "Perspective cavalière et patrons",
        "Unités de volume et de capacité",
        "Volumes du pavé droit et du prisme droit",
        "Aire du disque",
        "Volume du cylindre de révolution"
    ],
    "8. Transformations, angles": [
        "Demi-tour ou symétrie centrale",
        "Propriétés conservées",
        "Centre de symétrie, axe de symétrie",
        "Symétrie centrale et figures usuelles",
        "Nouveau vocabulaire des angles",
        "Angles alternes-internes et angles correspondants"
    ],
    "9. Triangles": [
        "Somme des angles d'un triangle",
        "Construction de triangles",
        "Médiatrices d'un triangle (rappels)",
        "Médiatrices d'un triangle rectangle",
        "Aire d'un triangle et hauteurs",
        "Médianes d'un triangle"
    ],
    "10. Parallélogrammes": [
        "Connaître le parallélogramme",
        "Reconnaître un parallélogramme",
        "Rectangles",
        "Losanges",
        "Carrés",
        "Aire du parallélogramme",
        "Unités de longueur et d'aire"
    ],
    "11. Statistiques": [
        "Effectif, fréquence",
        "Moyenne d'une série de données",
        "Représentations graphiques"
    ],
    "12. Probabilités": [
        "Expérience aléatoire et événement",
        "Attribuer une probabilité à une issue",
        "Déterminer la probabilité d'un événement"
    ],
    "13. Proportionnalité": [
        "Pourcentages",
        "Proportions",
        "Situations relevant ou non de la proportionnalité",
        "Linéarité et retour à l'unité",
        "Coefficient de proportionnalité",
        "Caractérisation graphique d'une situation de proportionnalité",
        "Produire une formule"
    ],
    "14. Fonctions": [
        "Expression d'une grandeur en fonction d'une autre",
        "Interprétation d'un tableau de valeurs ou d'un graphique",
        "Passage d'une formule à un tableau",
        "Produire une formule"
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

def recuperer_exercices_eleve(eleve_id):
    if not eleve_id:
        return []

    resultat = (
        supabase_privee.table("series_exercices")
        .select("id, code_reprise, exercices, reponses, progression")
        .eq("eleve_id", eleve_id)
        .order("created_at", desc=True)
        .execute()
    )

    return resultat.data or []

if st.session_state.get("eleve_id"):
    st.subheader("Mes exercices sauvegardés")

    if st.button("Retrouver mes séries"):
        try:
            series = recuperer_exercices_eleve(
                st.session_state["eleve_id"]
            )

            if not series:
                st.info("Aucune série enregistrée pour ce compte.")
            else:
                st.success(f"{len(series)} série(s) retrouvée(s).")

                for serie in series:
                    with st.expander(
                        f"Série n° {serie['id']}"
                    ):
                        
                       if st.button(
                         "Reprendre cette série",
                         key=f"reprendre_serie_{serie['id']}"
                      ):
                         st.session_state.exercices_actuels = serie["exercices"]
                         st.session_state.code_actuel = serie["code_reprise"]

                         reponses = serie.get("reponses") or {}

                         for numero, exercice in enumerate(
                             serie["exercices"], start=1
                         ):
                             cle = f"reponse_{numero}"
                             valeur = reponses.get(str(numero))

                             if valeur is not None:
                                st.session_state[cle] = valeur
                             elif cle in st.session_state:
                                 del st.session_state[cle]

                         st.success("Série chargée !")

                for numero, exercice in enumerate(
                            serie["exercices"], start=1
                        ):
                            st.write(
                                f"**Exercice {numero} :** "
                                f"{exercice['enonce']}"
                            )

                            reponse = (
                                serie.get("reponses") or {}
                            ).get(str(numero))

                            if reponse is not None:
                                st.write(
                                    f"Ta réponse enregistrée : {reponse}"
                                )

        except Exception:
            st.error("Impossible de récupérer tes exercices.")

def generer_code_reprise():
    caracteres = string.ascii_uppercase + string.digits
    return "".join(
        secrets.choice(caracteres) for _ in range(16)
    )
    
def sauvegarder_serie(exercices):
    code = generer_code_reprise()
    try:
        supabase_privee.table("series_exercices").insert({
            "eleve_id": st.session_state.get("eleve_id"),
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
                st.session_state.exercices_actuels = serie["exercices"]
                st.session_state.code_actuel = code_saisi.strip()

                reponses = serie.get("reponses") or {}

                for numero, exercice in enumerate(
                     serie["exercices"], start=1
                    ):
                     cle = f"reponse_{numero}"
                     valeur = reponses.get(str(numero))

                     if valeur is not None:
                        st.session_state[cle] = valeur
                     elif cle in st.session_state:
                          del st.session_state[cle]

                st.success("Série retrouvée !")

            else:
                st.warning("Aucune série trouvée avec ce code.")
        except Exception:
            st.error("Impossible de récupérer la série.")

def sauvegarder_reponse(code, numero, reponse):
    serie = recuperer_serie(code)

    if not serie:
        return False

    reponses = serie.get("reponses") or {}
    reponses[str(numero)] = reponse

    supabase_privee.table("series_exercices").update({
        "reponses": reponses
    }).eq("code_reprise", code).execute()

    return True

def enregistrer_reponse_auto(numero):
    code = st.session_state.get("code_actuel")
    reponse = st.session_state.get(f"reponse_{numero}")

    if code and reponse is not None:
        try:
            sauvegarder_reponse(code, numero, reponse)
        except Exception:
            st.session_state["erreur_sauvegarde"] = True

import random

def generer_exercice(chapitre, partie, difficulte, type_exercice):
    import random

    a = random.randint(2, 5 + difficulte * 5)
    b = random.randint(2, 5 + difficulte * 5)

    if chapitre == "1. Opérations":
        if partie == "Addition, soustraction et multiplication de nombres décimaux":
            x = round(a + random.randint(1, 9) / 10, 1)
            y = round(b + random.randint(1, 9) / 10, 1)
            operation = random.choice(["+", "-", "×"])

            if operation == "+":
                resultat = x + y
            elif operation == "-":
                resultat = x - y
            else:
                resultat = x * y

            enonce = f"Calcule : {x} {operation} {y}"
            correction = f"{x} {operation} {y} = {round(resultat, 2)}"

        elif partie == "Division euclidienne, multiples et diviseurs":
            diviseur = random.randint(2, 9)
            quotient = random.randint(2, 5 + difficulte * 5)
            reste = random.randint(0, diviseur - 1)
            dividende = diviseur * quotient + reste

            enonce = f"Effectue la division euclidienne de {dividende} par {diviseur}."
            correction = (
                f"{dividende} = {diviseur} × {quotient} + {reste}"
            )

        elif partie == "Division par un nombre décimal":
            diviseur = random.randint(2, 9) / 10
            quotient = random.randint(2, 5 + difficulte * 5)
            dividende = round(diviseur * quotient, 2)

            enonce = f"Calcule : {dividende} ÷ {diviseur}"
            correction = f"{dividende} ÷ {diviseur} = {quotient}"

        elif partie == "Priorités opératoires":
            enonce = f"Calcule : {a} + {b} × 3"
            reponse_attendue = a + b * 3
            correction = (
                f"On effectue d'abord la multiplication : "
                f"{b} × 3 = {b * 3}. "
                f"Puis {a} + {b * 3} = {a + b * 3}."
            )

        else:
            enonce = f"Développe : {a} × (x + {b})"
            correction = (
                f"{a} × (x + {b}) = {a}x + {a * b}"
            )

    else:
        enonce = f"Calcule la valeur de {a} × x + {b} pour x = 3."
        correction = f"{a} × 3 + {b} = {3 * a + b}"

    return {
    "enonce": enonce,
    "correction": correction,
    "reponse_attendue": reponse_attendue if chapitre == "1. Opérations" and partie == "Priorités opératoires" else None
}
    
if "exercices_actuels" not in st.session_state:
    st.session_state.exercices_actuels = []
if st.button("Générer mes exercices"):
    exercices = [
        generer_exercice(chapitre, partie, difficulte, type_exercice)
        for _ in range(nombre)
    ]
    st.session_state.exercices_actuels = exercices

    try:
        code = sauvegarder_serie(exercices)
        st.session_state.code_actuel = code
        st.success("Exercices générés et sauvegardés !")
        st.write("Ton code de reprise :")
        st.code(code)
    except Exception:
        st.error("Sauvegarde impossible.")

if st.session_state.exercices_actuels:
    for numero, exercice in enumerate(st.session_state.exercices_actuels, start=1):
        st.subheader(f"Exercice {numero}")
        st.write(exercice["enonce"])

        if exercice.get("reponse_attendue") is not None:
            reponse_eleve = st.number_input(
                "Ta réponse :",
                 value=None,
                 step=1,
                 key=f"reponse_{numero}",
                 on_change=enregistrer_reponse_auto,
                 args=(numero,)
            )

            if st.button("Vérifier ma réponse", key=f"verifier_{numero}"):
                if reponse_eleve is not None:
                    try:
                        sauvegarder_reponse(
                            st.session_state.code_actuel,
                            numero,
                            reponse_eleve
                        )
                        st.info("Réponse enregistrée.")
                    except Exception:
                        st.error("Impossible d'enregistrer la réponse.")

                if reponse_eleve is None:
                    st.warning("Saisis d'abord ta réponse.")
                elif reponse_eleve == exercice["reponse_attendue"]:
                    st.success("Bonne réponse !")
                else:
                    st.error("Réponse incorrecte. Essaie encore.")

        with st.expander("Voir la correction"):
            st.write(exercice["correction"])



