import streamlit as st
from google import genai
from groq import Groq
from banque_priorites import generer_exercices_priorites
from supabase import create_client
from auth_persistante import (
    enregistrer_session,
    supprimer_session,
    effacer_jeton_navigateur,
    enregistrer_jeton_navigateur,
    lire_jeton_navigateur,
    verifier_session
)

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

if not st.session_state.get("eleve_id"):
    jeton = lire_jeton_navigateur()

    if isinstance(jeton, str) and jeton:
        try:
            eleve_id = verifier_session(supabase_privee, jeton)
        except Exception:
            eleve_id = None

        if eleve_id:
            st.session_state["eleve_id"] = eleve_id
            st.session_state["jeton_persistant"] = jeton
            
if st.session_state.get("eleve_id"):
    jeton = st.session_state.get("jeton_persistant")

    if jeton:
        try:
            eleve_id = verifier_session(supabase_privee, jeton)
        except Exception:
            eleve_id = None
    else:
        eleve_id = None

    if not eleve_id or eleve_id != st.session_state["eleve_id"]:
        st.session_state.pop("eleve_id", None)
        st.session_state.pop("jeton_persistant", None)
        st.session_state.pop("session_eleve", None)
        
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

                jeton_persistant = enregistrer_session(
                    supabase_privee,
                    resultat.user.id
                )

                st.session_state["jeton_persistant"] = jeton_persistant
                enregistrer_jeton_navigateur(jeton_persistant)
                st.success("Connexion réussie !")

            else:
                st.error("Connexion impossible.")
        except Exception:
            st.error("Une erreur est survenue lors de la connexion.")

if st.session_state.get("eleve_id"):
    st.write("Tu es connecté à ton compte élève.")

    if st.button("Se déconnecter"):
        jeton = st.session_state.pop("jeton_persistant", None)
        if jeton:
            try:
                supprimer_session(supabase_privee, jeton)
            except Exception as e:
                st.error(f"Erreur suppression session : {e}")
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
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

if chapitre == "1. Opérations":
    partie = chapitres[chapitre][0]
else:
    partie = st.selectbox(
        "Sous-chapitre",
        chapitres[chapitre]
    )

st.write("**Type d'exercice**")

categories = [
    "Mes automatismes",
    "Je m'entraîne",
    "Je résous des problèmes"
]

type_exercice = st.radio(
    "Choisis une catégorie",
    categories,
    horizontal=True,
    label_visibility="collapsed",
    key="categorie_exercice"
)

couleurs_categories = {
    "Mes automatismes": ("#E8F3FF", "#2478D4"),
    "Je m'entraîne": ("#FFF3D9", "#D99416"),
    "Je résous des problèmes": ("#F0E7FF", "#8956D8")
}

descriptions = {
    "Mes automatismes": "Bases et réflexes — niveaux 1 à 3",
    "Je m'entraîne": "Calculs élaborés — niveaux 4 à 6",
    "Je résous des problèmes": "Raisonnement — niveaux 7 à 9"
}

fond, couleur = couleurs_categories[type_exercice]

st.markdown(
    f"""
    <div style="
        background-color: {fond};
        border: 2px solid {couleur};
        border-radius: 12px;
        padding: 18px;
        margin: 12px 0;
        color: #202B45;
    ">
        <strong>{type_exercice}</strong>
        <p style="margin-bottom:0">
            {descriptions[type_exercice]}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

col2 = st.container()
with col2:
    difficulte = st.radio(
        "Difficulté",
        [1, 2, 3],
        index=1,
        horizontal=True,
        format_func=lambda x: {
            1: "1 - Facile",
            2: "2 - Moyen",
            3: "3 - Difficile"
        }[x]
    )

debut_niveau = {
    "Mes automatismes": 0,
    "Je m'entraîne": 3,
    "Je résous des problèmes": 6
}

niveau_reel = debut_niveau[type_exercice] + difficulte

st.write(f"**Progression : niveau {niveau_reel} sur 9**")
st.progress(niveau_reel / 9)
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
if (
    st.session_state.get("eleve_id")
    and "exercices_actuels" not in st.session_state
):
    try:
        series_auto = recuperer_exercices_eleve(
            st.session_state["eleve_id"]
        )

        if series_auto:
            derniere_serie = series_auto[0]

            st.session_state.exercices_actuels = derniere_serie["exercices"]
            st.session_state.code_actuel = derniere_serie["code_reprise"]
            reponses = derniere_serie.get("reponses") or {}
            version = st.session_state.get("serie_version", 0)

            for numero, exercice in enumerate(derniere_serie["exercices"], start=1):
                donnees = reponses.get(str(numero))

                if isinstance(donnees, dict) and donnees.get("type") == "banque":
                    champs_sauvegardes = donnees.get("champs") or {}

                    for champ in exercice.get("champs_reponse", []):
                        if champ["id"] not in champs_sauvegardes:
                            continue

                        valeur = champs_sauvegardes[champ["id"]]

                        if champ["type"] == "choix":
                            if valeur not in champ["options"]:
                                valeur = "Choisir..."

                        cle = f"banque_{version}_{numero}_{champ['id']}"
                        st.session_state[cle] = valeur

                    bilan = donnees.get("bilan")

                    if isinstance(bilan, dict):
                        st.session_state[f"bilan_banque_{version}_{numero}"] = bilan

                elif donnees is not None:
                    st.session_state[f"reponse_{version}_{numero}"] = donnees

    except Exception:
        pass

if st.session_state.get("eleve_id"):
    st.subheader("Mes exercices sauvegardés")

    if st.button("Retrouver mes séries") or st.session_state.get("afficher_series", False):
        st.session_state["afficher_series"] = True
        try:
            series = recuperer_exercices_eleve(
                st.session_state["eleve_id"]
            )

            if not series:
                st.info("Aucune série enregistrée pour ce compte.")
            else:
                st.success(f"{len(series)} série(s) retrouvée(s).")
                ids_series = [s["id"] for s in series]

                cle_tout = f"tout_selectionner_{st.session_state['eleve_id']}"

                def cocher_toutes_series():
                    etat = st.session_state[cle_tout]
                    for identifiant in ids_series:
                        st.session_state[f"cocher_serie_{identifiant}"] = etat

                def synchroniser_selection():
                    st.session_state[cle_tout] = all(
                        st.session_state.get(
                            f"cocher_serie_{identifiant}", False
                        )
                        for identifiant in ids_series
                    )

                st.checkbox(
                    "Tout sélectionner",
                    key=cle_tout,
                    on_change=cocher_toutes_series
                )

                selection = [
                    identifiant
                    for identifiant in ids_series
                    if st.session_state.get(
                        f"cocher_serie_{identifiant}", False
                    )
                ]

                if st.button(
                    "Supprimer les séries cochées",
                    disabled=not selection
                ):
                    st.session_state["suppression_en_attente"] = {
                        "mode": "selection",
                        "ids": list(selection),
                        "eleve_id": st.session_state["eleve_id"]
                    }

                demande = st.session_state.get("suppression_en_attente")

                if (
                    demande
                    and demande["eleve_id"] == st.session_state["eleve_id"]
                ):
                    mode = demande["mode"]

                    ids_valides = [
                        identifiant
                        for identifiant in demande["ids"]
                        if identifiant in ids_series
                    ]

                    if mode == "toutes":
                        st.warning(
                            "Attention : toutes tes séries et leurs réponses "
                            "seront définitivement supprimées."
                        )
                    elif ids_valides:
                        st.warning(
                            f"Attention : {len(ids_valides)} série(s) "
                            "seront définitivement supprimée(s)."
                        )

                    if mode == "toutes" or ids_valides:
                        col_c1, col_c2 = st.columns(2)

                        with col_c1:
                            confirmer = st.button(
                                "Oui, supprimer définitivement",
                                key="confirmer_suppression_series"
                            )

                        with col_c2:
                            annuler = st.button(
                                "Annuler",
                                key="annuler_suppression_series"
                            )

                        if annuler:
                            st.session_state.pop(
                                "suppression_en_attente", None
                            )
                            st.rerun()

                        if confirmer:
                            try:
                                requete = (
                                    supabase_privee
                                    .table("series_exercices")
                                    .delete()
                                    .eq(
                                        "eleve_id",
                                        st.session_state["eleve_id"]
                                    )
                                )

                                if mode == "selection":
                                    requete = requete.in_(
                                        "id", ids_valides
                                    )

                                resultat = requete.select("id").execute()

                                ids_supprimes = {
                                    ligne["id"]
                                    for ligne in (resultat.data or [])
                                }

                                if (
                                    mode == "selection"
                                    and ids_supprimes != set(ids_valides)
                                ):
                                    st.error(
                                        "La suppression n'a pas été confirmée "
                                        "pour toutes les séries. "
                                        "Actualise la liste avant de réessayer."
                                    )
                                else:
                                    codes_supprimes = {
                                        s["code_reprise"]
                                        for s in series
                                        if s["id"] in ids_supprimes
                                    }

                                    if (
                                        mode == "toutes"
                                        or st.session_state.get("code_actuel")
                                        in codes_supprimes
                                    ):
                                        st.session_state["exercices_actuels"] = []
                                        st.session_state.pop("code_actuel", None)
                                        st.session_state["serie_version"] = (
                                            st.session_state.get(
                                                "serie_version", 0
                                            ) + 1
                                        )

                                    st.session_state.pop(
                                        "suppression_en_attente", None
                                    )
                                    st.session_state["afficher_series"] = True
                                    st.rerun()

                            except Exception:
                                st.error(
                                    "Impossible de supprimer les séries. "
                                    "Aucune nouvelle tentative automatique "
                                    "ne sera effectuée."
                                )

                for serie in series:
                    col_coche, col_contenu = st.columns([1, 3], gap="small")

                    with col_coche:
                        st.checkbox(
                            f"Série n° {serie['id']}",
                            key=f"cocher_serie_{serie['id']}",
                            on_change=synchroniser_selection
                        )

                    with col_contenu:
                       if st.button(
                         "Ouvrir",
                         key=f"reprendre_serie_{serie['id']}"
                      ):
                         st.session_state.exercices_actuels = serie["exercices"]
                         st.session_state.code_actuel = serie["code_reprise"]

                         reponses = serie.get("reponses") or {}
                         for numero, exercice in enumerate(serie["exercices"], start=1):
                            donnees = reponses.get(str(numero), {})
                        
                            if not isinstance(donnees, dict):
                                continue
                        
                            if donnees.get("type") != "banque":
                                continue
                        
                            champs_sauvegardes = donnees.get("champs") or {}
                            bilan = donnees.get("bilan")

                            cle_bilan = (
                                f"bilan_banque_{st.session_state.get('serie_version', 0)}"
                                f"_{numero}"
                            )
                            
                            if isinstance(bilan, dict):
                                st.session_state[cle_bilan] = bilan
                            else:
                                st.session_state.pop(cle_bilan, None)
                        
                            for champ in exercice.get("champs_reponse", []):
                                cle = (
                                    f"banque_{st.session_state.get('serie_version', 0)}"
                                    f"_{numero}_{champ['id']}"
                                )
                        
                                valeur = champs_sauvegardes.get(champ["id"], "")
                        
                                if champ["type"] == "choix":
                                    if valeur not in champ["options"]:
                                        valeur = "Choisir..."
                        
                                st.session_state[cle] = valeur
                            
                         for numero, exercice in enumerate(
                             serie["exercices"], start=1
                         ):
                             cle = f"reponse_{numero}"
                             valeur = reponses.get(str(numero))

                             if valeur is not None:
                                st.session_state[cle] = valeur
                             elif cle in st.session_state:
                                 del st.session_state[cle]
                         st.session_state["serie_ouverte_depuis_liste"] = True
                         st.session_state["afficher_series"] = False
                         st.rerun()

        except Exception:
            st.error("Impossible de récupérer tes exercices.")
zone_serie_ouverte = st.container()

def generer_code_reprise():
    caracteres = string.ascii_uppercase + string.digits
    return "".join(
        secrets.choice(caracteres) for _ in range(16)
    )
    
def sauvegarder_serie(exercices):
    if not st.session_state.get("eleve_id"):
        raise ValueError("Connecte-toi pour sauvegarder tes exercices.")
         
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

def recuperer_serie(code):
    eleve_id = st.session_state.get("eleve_id")

    if not eleve_id:
        return None

    resultat = (
        supabase_privee.table("series_exercices")
        .select("code_reprise, exercices, reponses, progression")
        .eq("code_reprise", code.strip().upper())
        .eq("eleve_id", eleve_id)
        .limit(1)
        .execute()
    )

    if resultat.data:
        return resultat.data[0]

    return None

def sauvegarder_reponse(code, numero, reponse):
    eleve_id = st.session_state.get("eleve_id")

    if not eleve_id:
        return False

    serie = recuperer_serie(code)

    if not serie:
        return False

    reponses = serie.get("reponses") or {}
    reponses[str(numero)] = reponse

    resultat = (
        supabase_privee.table("series_exercices")
        .update({"reponses": reponses})
        .eq("code_reprise", code.strip().upper())
        .eq("eleve_id", eleve_id)
        .execute()
    )

    return bool(resultat.data)
    
def enregistrer_reponse_auto(numero):
    code = st.session_state.get("code_actuel")
    reponse = st.session_state.get(f"reponse_{numero}")

    if code and reponse is not None:
        try:
            sauvegarder_reponse(code, numero, reponse)
        except Exception:
            st.session_state["erreur_sauvegarde"] = True
def enregistrer_reponses_banque_auto(numero):
    cle_bilan = (
    f"bilan_banque_{st.session_state.get('serie_version', 0)}"
    f"_{numero}"
    )
    st.session_state.pop(cle_bilan, None)
    code = st.session_state.get("code_actuel")

    if not code or not st.session_state.get("eleve_id"):
        return

    exercices = st.session_state.get("exercices_actuels", [])

    if numero > len(exercices):
        return

    exercice = exercices[numero - 1]
    reponses = {}

    for champ in exercice.get("champs_reponse", []):
        cle = (
            f"banque_{st.session_state.get('serie_version', 0)}"
            f"_{numero}_{champ['id']}"
        )

        reponses[champ["id"]] = st.session_state.get(cle, "")

    try:
        sauvegarder_reponse(
            code,
            numero,
            {
                "type": "banque",
                "champs": reponses
            }
        )
    except Exception:
        st.session_state["erreur_sauvegarde"] = True
import random
def generer_exercice_groq(chapitre, partie, difficulte, type_exercice, nombre=1):
    import json

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    consigne = f"""
    Tu es professeur de mathématiques en classe de 5e en France.

    Chapitre : {chapitre}
    Sous-chapitre : {partie}
    Catégorie : {type_exercice}
    Difficulté : {difficulte} sur 3

    Génère exactement {nombre} problèmes différents.

    Consignes pédagogiques :

    1. Respect du programme :
    - Respecte le programme français de mathématiques de 5e.
    - Traite uniquement le chapitre et le sous-chapitre demandés.
    - Choisis des situations concrètes, réalistes et variées.
    - Évite les notions mathématiques hors du sujet étudié.

    2. Progression des difficultés :

    Difficulté 1 (niveau réel 7) :
    - Crée un problème court nécessitant plusieurs calculs liés.
    - Respecte strictement les priorités opératoires.
    - La solution doit pouvoir s'écrire sous la forme
      d'une seule expression numérique avec des parenthèses.
    - Cette expression doit comporter au moins
      4 opérations utiles, dont une multiplication ou division.
    - Propose 2 ou 3 questions progressives maximum.
    - Les questions doivent contribuer au même raisonnement.
    - Évite les questions indépendantes ou inutiles.
    - Ne donne pas directement à l'élève l'ordre des calculs.
    - Dans la correction, montre l'expression complète
      puis explique son calcul étape par étape.
    - Conserve un énoncé court et facile à comprendre.

    Difficulté 2 (niveau réel 8) :
    - Propose un problème nécessitant plusieurs décisions.
    - L'élève doit organiser les données et choisir ses calculs.
    - Guide moins l'élève qu'au niveau 7.

    Difficulté 3 (niveau réel 9) :
    - Propose un problème nécessitant une stratégie.
    - Introduis des contraintes ou des calculs interdépendants.
    - L'élève doit organiser et vérifier sa démarche.

    3. Clarté et présentation :
    - Rédige des énoncés courts avec des phrases simples.
    - Utilise un vocabulaire compréhensible par un élève de 5e.
    - Limite chaque problème à 3 questions maximum.
    - Sépare les questions par des retours à la ligne.
    - Évite les informations inutiles et les histoires compliquées.
    - Augmente la difficulté par le raisonnement, pas par la longueur.
    - Varie les contextes et les méthodes dans une même série.

    4. Fiabilité mathématique :
    - Utilise uniquement des données cohérentes et réalistes.
    - Distingue clairement les quantités achetées, vendues,
      données, utilisées et restantes.
    - Pour les objets indivisibles, choisis des calculs
      donnant des quantités entières.
    - Évite les arrondis arbitraires.
    - Vérifie chaque résultat et sa cohérence avec l'énoncé.
    - Ne crée pas d'étapes artificielles ou inutiles.

    5. Correction :
    - Explique le raisonnement avec des mots simples.
    - Présente chaque étape importante sur une ligne distincte.
    - Montre les opérations et leurs résultats.
    - Termine par une réponse finale avec son unité.
    - Utilise les symboles mathématiques habituels, sans LaTeX.
    
    Réponds uniquement avec un objet JSON valide contenant
    une clé "exercices" dont la valeur est un tableau JSON.
    Chaque élément doit contenir :
    "enonce" : texte complet du problème
    "correction" : correction détaillée

    Le tableau doit contenir exactement {nombre} éléments.
    """

    reponse = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "user", "content": consigne}
        ],
        temperature=0.5,
        max_completion_tokens=8192,
        reasoning_effort="low",
        response_format={"type": "json_object"}
    )

    contenu = reponse.choices[0].message.content

    if not contenu:
        raise ValueError("Réponse Groq vide")

    donnees = json.loads(contenu)

    exercices = donnees["exercices"]

    if not isinstance(exercices, list) or len(exercices) != nombre:
        raise ValueError("Nombre d'exercices Groq incorrect")

    return [
        {
            "enonce": exercice["enonce"],
            "correction": exercice["correction"],
            "reponse_attendue": None
        }
        for exercice in exercices
    ]
def generer_exercice_ia(chapitre, partie, difficulte, type_exercice, nombre=1):
    import json
    import re

    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    consigne = f"""
    Tu es professeur de mathématiques en classe de 5e en France.

    Chapitre : {chapitre}
    Sous-chapitre : {partie}
    Catégorie : {type_exercice}
    Difficulté : {difficulte} sur 3

    Génère exactement {nombre} problèmes différents.

    Consignes :
    - Respecte le programme français de 5e.
    - Adapte réellement la complexité à la difficulté demandée.
    - Varie fortement les contextes et les raisonnements.
    - Évite les répétitions de thèmes dans une même série.
    - Propose des problèmes nécessitant plusieurs étapes.
    - Fournis une correction mathématique détaillée.
    - Utilise le symbole € directement, sans LaTeX.
    - N'utilise pas de commandes LaTeX.
     Exigences pédagogiques :
    - Chaque problème doit présenter une situation réaliste et cohérente.
    - Utilise des contextes variés : sport, sciences, voyages,
      jeux, mesures, environnement, vie quotidienne.
    - Ne répète pas le même contexte dans une série.
    - Niveau 1 : problème guidé avec 2 à 3 étapes simples.
    - Niveau 2 : problème avec 3 à 4 étapes et plusieurs opérations.
    - Niveau 3 : problème plus complexe nécessitant une stratégie.
    - Les questions doivent être progressives.
    - Vérifie tous les calculs avant de rédiger la correction.
    - Présente chaque étape du calcul clairement.
    - Vérifie que la réponse finale correspond exactement à l'énoncé.
    - Évite les ambiguïtés et les données inutiles.
    Réponds uniquement avec un tableau JSON valide.
    Chaque élément doit contenir :
    "enonce" : texte complet du problème
    "correction" : correction détaillée

    Le tableau doit contenir exactement {nombre} éléments.
    """

    reponse = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=consigne,
        config={
            "response_mime_type": "application/json"
        }
    )

    contenu = reponse.text

    if not contenu:
        raise ValueError("Réponse IA vide")

    exercices = json.loads(contenu)

    if not isinstance(exercices, list) or len(exercices) != nombre:
        raise ValueError("Nombre d'exercices IA incorrect")

    resultat = []

    for exercice in exercices:
        enonce = exercice["enonce"]
        correction = exercice["correction"]

        enonce = re.sub(r"\\text\{?euro\}?", "€", enonce)
        correction = re.sub(r"\\text\{?euro\}?", "€", correction)

        resultat.append({
            "enonce": enonce,
            "correction": correction,
            "reponse_attendue": None
        })

    return resultat
def generer_exercice(chapitre, partie, difficulte, type_exercice):
    import random
    enonce = None
    correction = None
    reponse_attendue = None
    champs_reponse = []    

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
            reponse_attendue = round(resultat, 2)

            if type_exercice == "Mes automatismes" and difficulte == 3:
                k = random.randint(2, 5)

                def fr3(valeur):
                    return f"{valeur:g}".replace(".", ",")

                if random.choice([True, False]):
                    produit = round(y * k, 2)
                    resultat = round(x + produit, 2)

                    enonce = (
                        f"Calcule : {fr3(x)} + {fr3(y)} × {k}"
                    )

                    correction = (
                        f"On effectue d'abord la multiplication :\n"
                        f"{fr3(y)} × {k} = {fr3(produit)}.\n\n"
                        f"Puis l'addition :\n"
                        f"{fr3(x)} + {fr3(produit)} "
                        f"= {fr3(resultat)}."
                    )

                else:
                    somme = round(x + y, 2)
                    resultat = round(somme * k, 2)

                    enonce = (
                        f"Calcule : ({fr3(x)} + {fr3(y)}) × {k}"
                    )

                    correction = (
                        f"On calcule d'abord la parenthèse :\n"
                        f"{fr3(x)} + {fr3(y)} = {fr3(somme)}.\n\n"
                        f"Puis la multiplication :\n"
                        f"{fr3(somme)} × {k} "
                        f"= {fr3(resultat)}."
                    )

                reponse_attendue = resultat

            if type_exercice == "Je m'entraîne":
                n = random.randint(4, 7)
                m = random.randint(2, 4)

                a = random.randint(40, 85) / 10
                b = random.randint(15, 45) / 10
                c = random.randint(11, 35) / 10
                d = random.randint(10, 30) / 10
                e = random.randint(10, 30) / 10

                def fr(valeur):
                    return f"{round(valeur, 2):g}".replace(".", ",")

                somme1 = round(a + b, 2)
                produit1 = round(n * somme1, 2)

                if difficulte == 1:
                    variante = random.choice(["calcul", "probleme"])
    
                    if variante == "calcul":
                        somme2 = round(c + d, 2)
                        resultat = round(produit1 - somme2, 2)
    
                        enonce = (
                            f"Calcule : {n} × ({fr(a)} + {fr(b)}) "
                            f"- ({fr(c)} + {fr(d)})"
                        )
    
                        correction = (
                            f"Première parenthèse :\n"
                            f"{fr(a)} + {fr(b)} = {fr(somme1)}.\n\n"
                            f"Deuxième parenthèse :\n"
                            f"{fr(c)} + {fr(d)} = {fr(somme2)}.\n\n"
                            f"Multiplication :\n"
                            f"{n} × {fr(somme1)} = {fr(produit1)}.\n\n"
                            f"Soustraction :\n"
                            f"{fr(produit1)} - {fr(somme2)} "
                            f"= {fr(resultat)}."
                        )
    
                    else:
                        resultat = round(produit1 - c + d, 2)
    
                        enonce = (
                            f"Une association commande {n} kits. "
                            f"Chaque kit contient deux objets "
                            f"coûtant {fr(a)} € et {fr(b)} €.\n\n"
                            f"Le vendeur accorde une réduction "
                            f"de {fr(c)} € sur la commande, "
                            f"mais les frais de livraison sont "
                            f"de {fr(d)} €.\n\n"
                            f"Quel est le montant total à payer ?"
                        )
    
                        correction = (
                            f"Prix d'un kit :\n"
                            f"{fr(a)} + {fr(b)} = {fr(somme1)} €.\n\n"
                            f"Prix des {n} kits :\n"
                            f"{n} × {fr(somme1)} = {fr(produit1)} €.\n\n"
                            f"On retire la réduction, puis "
                            f"on ajoute la livraison :\n"
                            f"{fr(produit1)} - {fr(c)} + {fr(d)} "
                            f"= {fr(resultat)} €."
                        )
                elif difficulte == 2:
                    produit2 = round(m * c, 2)
                    ajout = round(random.randint(15, 95) / 10, 1)
        
                    sous_total = round(produit1 - produit2, 2)
                    resultat = round(sous_total + ajout, 2)
        
                    enonce = (
                        f"Calcule : {n} × ({fr(a)} + {fr(b)}) "
                        f"- {m} × {fr(c)} + {fr(ajout)}"
                    )
        
                    correction = (
                        f"Parenthèse :\n"
                        f"{fr(a)} + {fr(b)} = {fr(somme1)}.\n\n"
                        f"Multiplications :\n"
                        f"{n} × {fr(somme1)} = {fr(produit1)}.\n"
                        f"{m} × {fr(c)} = {fr(produit2)}.\n\n"
                        f"Soustraction :\n"
                        f"{fr(produit1)} - {fr(produit2)} "
                        f"= {fr(sous_total)}.\n\n"
                        f"Addition finale :\n"
                        f"{fr(sous_total)} + {fr(ajout)} "
                        f"= {fr(resultat)}."
                    )

                else:
                    somme2 = round(c + d, 2)
                    produit2 = round(m * somme2, 2)
                    resultat = round(produit1 - produit2 + e, 2)

                    enonce = (
                        f"Calcule : {n} × ({fr(a)} + {fr(b)}) "
                        f"- {m} × ({fr(c)} + {fr(d)}) "
                        f"+ {fr(e)}"
                    )

                    correction = (
                        f"Parenthèses :\n"
                        f"{fr(a)} + {fr(b)} = {fr(somme1)}.\n"
                        f"{fr(c)} + {fr(d)} = {fr(somme2)}.\n\n"
                        f"Multiplications :\n"
                        f"{n} × {fr(somme1)} = {fr(produit1)}.\n"
                        f"{m} × {fr(somme2)} = {fr(produit2)}.\n\n"
                        f"Calcul final : {fr(produit1)} - {fr(produit2)} "
                        f"+ {fr(e)} = {fr(resultat)}."
                    )

                reponse_attendue = resultat
        elif partie == "Division euclidienne, multiples et diviseurs":
            diviseur = random.randint(2, 9)
            quotient = random.randint(2, 5 + difficulte * 5)
            reste = random.randint(0, diviseur - 1)
            dividende = diviseur * quotient + reste

            enonce = f"Effectue la division euclidienne de {dividende} par {diviseur}."
            correction = (
                f"{dividende} = {diviseur} × {quotient} + {reste}"
            )
            champs_reponse = [
                {
                    "id": "quotient",
                    "question": 1,
                    "libelle": "Quotient",
                    "type": "nombre",
                    "attendu": quotient,
                    "unite": ""
                },
                {
                    "id": "reste",
                    "question": 2,
                    "libelle": "Reste",
                    "type": "nombre",
                    "attendu": reste,
                    "unite": ""
                }
            ]
            if type_exercice == "Je m'entraîne":
    
                if difficulte == 1:
                    capacite = random.randint(6, 12)
                    lots = random.randint(9, 17)
                    restant = random.randint(1, capacite - 1)
                    reserve = random.randint(10, 25)
        
                    disponible = capacite * lots + restant
                    total = disponible + reserve
        
                    attendu1 = lots
                    attendu2 = capacite - restant
        
                    enonce = (
                        f"Une école possède {total} crayons.\n\n"
                        f"Elle doit conserver {reserve} crayons "
                        f"pour les activités en classe.\n"
                        f"Avec les autres crayons, elle prépare "
                        f"des trousses de {capacite} crayons.\n\n"
                        f"1. Combien de trousses complètes "
                        f"peut-elle préparer ?\n\n"
                        f"2. Combien de crayons doit-elle acheter "
                        f"pour remplir une trousse supplémentaire "
                        f"sans utiliser sa réserve ?"
                    )
        
                    
                    correction = (
                        f"1. Nombre de crayons disponibles :\n"
                        f"{total} - {reserve} = {disponible} crayons.\n\n"
    
                        f"Division euclidienne :\n"
                        f"{disponible} ÷ {capacite}\n"
                        f"Quotient = {lots}, reste = {restant}.\n"
                        f"Vérification : {disponible} = "
                        f"{capacite} × {lots} + {restant}.\n"
                        f"L'école peut préparer {attendu1} "
                        f"trousses complètes.\n\n"
    
                        f"2. Crayons supplémentaires nécessaires :\n"
                        f"Il reste {restant} crayons.\n"
                        f"Il faut {capacite} crayons par trousse.\n"
                        f"{capacite} - {restant} = {attendu2} crayons."
                    )

        
                    libelle1 = "Nombre de trousses complètes"
                    libelle2 = "Crayons à acheter"
    
                elif difficulte == 2:
                    capacite = random.randint(8, 15)
                    lots = random.randint(15, 25)
                    restant = random.randint(1, capacite - 1)
                    total = capacite * lots + restant
                    livraison = random.randint(capacite, capacite * 2 + 3)
    
                    nouveau_total = total + livraison
                    attendu1 = lots
                    attendu2 = nouveau_total // capacite
                    nouveau_reste = nouveau_total % capacite
    
                    enonce = (
                        f"Un club possède {total} jetons. "
                        f"Il prépare des lots de {capacite} jetons.\n\n"
                        f"Le club reçoit ensuite {livraison} jetons supplémentaires.\n\n"
                        f"1. Combien de lots complets peut-il préparer "
                        f"avant la livraison ?\n\n"
                        f"2. Combien de lots complets pourra-t-il préparer "
                        f"après la livraison ?"
                    )
    
                    
                    correction = (
                        f"1. Avant la livraison :\n"
                        f"Division : {total} ÷ {capacite}\n"
                        f"Quotient = {lots}, reste = {restant}.\n"
                        f"Vérification : {total} = "
                        f"{capacite} × {lots} + {restant}.\n"
                        f"Le club peut préparer {attendu1} "
                        f"lots complets.\n\n"
    
                        f"2. Après la livraison :\n"
                        f"Nombre total de jetons :\n"
                        f"{total} + {livraison} = {nouveau_total}.\n"
                        f"Division : {nouveau_total} ÷ {capacite}\n"
                        f"Quotient = {attendu2}, "
                        f"reste = {nouveau_reste}.\n"
                        f"Vérification : {nouveau_total} = "
                        f"{capacite} × {attendu2} + {nouveau_reste}.\n"
                        f"Le club peut préparer {attendu2} "
                        f"lots complets."
                    )

    
                    libelle1 = "Lots complets avant livraison"
                    libelle2 = "Lots complets après livraison"
    
                else:    
                    petite = random.randint(8, 13)
                    grande = petite + random.randint(4, 7)

                    jeunesse = random.randint(60, 120)
                    adultes = random.randint(50, 100)
                    total = jeunesse + adultes

                    q_jp, r_jp = divmod(jeunesse, petite)
                    q_ap, r_ap = divmod(adultes, petite)

                    q_jg, r_jg = divmod(jeunesse, grande)
                    q_ag, r_ag = divmod(adultes, grande)

                    petites_jeunesse = q_jp + (1 if r_jp else 0)
                    petites_adultes = q_ap + (1 if r_ap else 0)

                    grandes_jeunesse = q_jg + (1 if r_jg else 0)
                    grandes_adultes = q_ag + (1 if r_ag else 0)

                    attendu1 = petites_jeunesse + petites_adultes

                    nombre_grandes = (
                        grandes_jeunesse + grandes_adultes
                    )

                    attendu2 = attendu1 - nombre_grandes

                    enonce = (
                        f"Une bibliothèque doit transporter "
                        f"{total} livres :\n"
                        f"- {jeunesse} livres jeunesse.\n"
                        f"- {adultes} livres adultes.\n\n"
                        f"Elle dispose de petites caisses "
                        f"contenant au maximum {petite} livres "
                        f"et de grandes caisses contenant "
                        f"au maximum {grande} livres.\n\n"
                        f"Les livres jeunesse et adultes "
                        f"ne doivent pas être mélangés "
                        f"dans une même caisse.\n\n"
                        f"1. Combien de petites caisses "
                        f"faut-il au minimum ?\n\n"
                        f"2. Combien de caisses économise-t-elle "
                        f"en utilisant uniquement "
                        f"les grandes caisses ?"
                    )

                    correction = (
                        f"1. Avec les petites caisses :\n\n"

                        f"Livres jeunesse :\n"
                        f"{jeunesse} ÷ {petite} :\n"
                        f"Quotient = {q_jp}, reste = {r_jp}.\n"
                        f"Vérification : {jeunesse} = "
                        f"{petite} × {q_jp} + {r_jp}.\n"
                        f"Il faut {petites_jeunesse} caisses.\n\n"

                        f"Livres adultes :\n"
                        f"{adultes} ÷ {petite} :\n"
                        f"Quotient = {q_ap}, reste = {r_ap}.\n"
                        f"Vérification : {adultes} = "
                        f"{petite} × {q_ap} + {r_ap}.\n"
                        f"Il faut {petites_adultes} caisses.\n\n"

                        f"Total : {petites_jeunesse} + "
                        f"{petites_adultes} = {attendu1} caisses.\n\n"

                        f"2. Avec les grandes caisses :\n\n"

                        f"Livres jeunesse :\n"
                        f"{jeunesse} ÷ {grande} :\n"
                        f"Quotient = {q_jg}, reste = {r_jg}.\n"
                        f"Vérification : {jeunesse} = "
                        f"{grande} × {q_jg} + {r_jg}.\n"
                        f"Il faut {grandes_jeunesse} caisses.\n\n"

                        f"Livres adultes :\n"
                        f"{adultes} ÷ {grande} :\n"
                        f"Quotient = {q_ag}, reste = {r_ag}.\n"
                        f"Vérification : {adultes} = "
                        f"{grande} × {q_ag} + {r_ag}.\n"
                        f"Il faut {grandes_adultes} caisses.\n\n"

                        f"Total : {grandes_jeunesse} + "
                        f"{grandes_adultes} = {nombre_grandes} caisses.\n\n"

                        f"Caisses économisées :\n"
                        f"{attendu1} - {nombre_grandes} "
                        f"= {attendu2} caisses.\n\n"

                        f"Si le reste est différent de zéro, "
                        f"une caisse supplémentaire est nécessaire."
                    )

                    libelle1 = "Nombre de petites caisses"
                    libelle2 = "Nombre de caisses économisées"

    
                champs_reponse = [
                    {
                        "id": "question_1",
                        "question": 1,
                        "libelle": libelle1,
                        "type": "nombre",
                        "attendu": attendu1,
                        "unite": ""
                    },
                    {
                        "id": "question_2",
                        "question": 2,
                        "libelle": libelle2,
                        "type": "nombre",
                        "attendu": attendu2,
                        "unite": ""
                    }
                ]            

        elif partie == "Division par un nombre décimal":
            diviseur = random.randint(2, 9) / 10
            quotient = random.randint(2, 5 + difficulte * 5)
            dividende = round(diviseur * quotient, 2)

            if type_exercice == "Mes automatismes" and difficulte == 3:
                autre_nombre = random.randint(2, 8)
                signe = random.choice(["+", "-"])

                if signe == "+":
                    resultat = quotient + autre_nombre
                else:
                    resultat = quotient - autre_nombre

                enonce = (
                    f"Calcule : {dividende} ÷ {diviseur} "
                    f"{signe} {autre_nombre}"
                )

                correction = (
                    f"On effectue d'abord la division :\n"
                    f"{dividende} ÷ {diviseur} = {quotient}.\n\n"
                    f"Puis : {quotient} {signe} {autre_nombre} "
                    f"= {resultat}."
                )

                reponse_attendue = resultat

            enonce = f"Calcule : {dividende} ÷ {diviseur}"
            correction = f"{dividende} ÷ {diviseur} = {quotient}"
            reponse_attendue = quotient
            
            if type_exercice == "Je m'entraîne":
                reponse_attendue = None

                d = random.choice([0.2, 0.25, 0.4, 0.5, 0.8])
                n1 = random.randint(14, 26)
                n2 = random.randint(6, 15)

                v1 = round(n1 * d, 2)
                v2 = round(n2 * d, 2)

                def fr(valeur):
                    return f"{round(valeur, 2):g}".replace(".", ",")

                if difficulte == 1:
                    retrait = random.randint(3, 8)
                    resultat = n1 + n2 - retrait

                    enonce = (
                        f"Calcule : {fr(v1)} ÷ {fr(d)} "
                        f"+ {fr(v2)} ÷ {fr(d)} - {retrait}"
                    )

                    correction = (
                        f"Divisions :\n"
                        f"{fr(v1)} ÷ {fr(d)} = {n1}.\n"
                        f"{fr(v2)} ÷ {fr(d)} = {n2}.\n\n"
                        f"Calcul final : {n1} + {n2} - {retrait} "
                        f"= {resultat}."
                    )

                    reponse_attendue = resultat

                elif difficulte == 2:
                    fabriques = random.randint(4, n1 - 2)
                    reserve = random.randint(1, n1 - fabriques - 1)
                    ruban_decoration = round(reserve * d, 2)
        
                    restant = round(
                        v1 - fabriques * d - ruban_decoration, 2
                    )
                    attendu2 = n1 - fabriques - reserve
        
                    enonce = (
                        f"Un atelier possède {fr(v1)} m de ruban.\n\n"
                        f"Chaque bracelet nécessite {fr(d)} m de ruban.\n\n"
                        f"1. Combien de bracelets peut-il fabriquer "
                        f"au maximum ?\n\n"
                        f"2. Après avoir fabriqué {fabriques} bracelets, "
                        f"l'atelier utilise également {fr(ruban_decoration)} m "
                        f"pour décorer des paquets. "
                        f"Combien de bracelets supplémentaires "
                        f"peut-il encore fabriquer ?"
                    )
        
                    correction = (
                        f"1. Nombre maximal de bracelets :\n"
                        f"{fr(v1)} ÷ {fr(d)} = {n1} bracelets.\n\n"
                        f"2. Ruban utilisé pour les bracelets :\n"
                        f"{fabriques} × {fr(d)} "
                        f"= {fr(fabriques * d)} m.\n"
                        f"Ruban restant après les décorations :\n"
                        f"{fr(v1)} - {fr(fabriques * d)} "
                        f"- {fr(ruban_decoration)} "
                        f"= {fr(restant)} m.\n"
                        f"Bracelets supplémentaires :\n"
                        f"{fr(restant)} ÷ {fr(d)} "
                        f"= {attendu2} bracelets."
                    )

                    champs_reponse = [
                        {
                            "id": "question_1",
                            "question": 1,
                            "libelle": "Nombre maximal de bracelets",
                            "type": "nombre",
                            "attendu": n1,
                            "unite": "bracelets"
                        },
                        {
                            "id": "question_2",
                            "question": 2,
                            "libelle": "Nombre de bracelets supplémentaires",
                            "type": "nombre",
                            "attendu": attendu2,
                            "unite": "bracelets"
                        }
                    ]

                else:
                    d2 = random.choice(
                        [x for x in [0.2, 0.25, 0.4, 0.5, 0.8] if x != d]
                    )

                    n3 = random.randint(5, 13)
                    v3 = round(n3 * d2, 2)
                    multiplicateur = random.randint(2, 5)
                    retrait = random.randint(3, 10)

                    resultat = n1 + n2 + multiplicateur * n3 - retrait

                    enonce = (
                        f"Calcule : ({fr(v1)} + {fr(v2)}) ÷ {fr(d)} "
                        f"+ {multiplicateur} × "
                        f"({fr(v3)} ÷ {fr(d2)}) - {retrait}"
                    )

                    correction = (
                        f"Première parenthèse :\n"
                        f"{fr(v1)} + {fr(v2)} = {fr(v1 + v2)}.\n\n"
                        f"Divisions :\n"
                        f"{fr(v1 + v2)} ÷ {fr(d)} = {n1 + n2}.\n"
                        f"{fr(v3)} ÷ {fr(d2)} = {n3}.\n\n"
                        f"Multiplication :\n"
                        f"{multiplicateur} × {n3} "
                        f"= {multiplicateur * n3}.\n\n"
                        f"Calcul final :\n"
                        f"{n1 + n2} + {multiplicateur * n3} "
                        f"- {retrait} = {resultat}."
                    )

                    reponse_attendue = resultat
        elif partie == "Priorités opératoires":
            multiplicateur = random.randint(2, 9)

            if type_exercice == "Mes automatismes":
                if difficulte == 1:
                    x = random.randint(2, 15)
                    y = random.randint(2, 9)
                    z = random.randint(2, 5)
                    enonce = f"Calcule : {x} + {y} × {z}"
                    reponse_attendue = x + y * z
                    correction = (
                        f"On commence par la multiplication : "
                        f"{y} × {z} = {y * z}. "
                        f"Puis {x} + {y * z} = {reponse_attendue}."
                    )
    
                elif difficulte == 2:
                    x = random.randint(5, 20)
                    y = random.randint(2, 10)
                    z = random.randint(2, 5)
                    enonce = f"Calcule : ({x} + {y}) × {z}"
                    reponse_attendue = (x + y) * z
                    correction = (
                        f"On calcule d'abord la parenthèse : "
                        f"{x} + {y} = {x + y}. "
                        f"Puis {x + y} × {z} = {reponse_attendue}."
                    )

                else:
                    x = random.randint(20, 50)
                    y = random.randint(2, 6)
                    z = random.randint(3, 9)
                    enonce = f"Calcule : {x} - {y} × ({z} + 2)"
                    reponse_attendue = x - y * (z + 2)
                    correction = (
                        f"On calcule la parenthèse : {z} + 2 = {z + 2}. "
                        f"Puis la multiplication : {y} × {z + 2} = {y * (z + 2)}. "
                        f"Enfin {x} - {y * (z + 2)} = {reponse_attendue}."
                    )            
            elif type_exercice == "Je m'entraîne":
    
                if difficulte == 1:
                    a = random.randint(80, 120)
                    b = random.randint(2, 8)
                    c = random.randint(3, 9)
                    d = random.randint(2, 6)
    
                    enonce = f"Calcule : {a} - {b} × ({c} + {d}) + {c} × {d}"
    
                    reponse_attendue = a - b * (c + d) + c * d
    
                    correction = (
                        f"On commence par la parenthèse : "
                        f"{c} + {d} = {c + d}. "
                        f"Puis les multiplications : "
                        f"{b} × {c + d} = {b * (c + d)} et "
                        f"{c} × {d} = {c * d}. "
                        f"Enfin : {a} - {b * (c + d)} + {c * d} "
                        f"= {reponse_attendue}."
                    )    
                elif difficulte == 2:
                    a = random.randint(3, 8)
                    b = random.randint(2, 7)
                    c = random.randint(2, 5)
                    d = random.randint(b + 1, b + 5)
                    e = random.randint(2, 6)
    
                    dividende = (a + b) * c
    
                    enonce = (
                        f"Calcule : {dividende} ÷ ({a} + {b}) "
                        f"+ {d} × ({c} + {e}) - {b} × {e}"
                    )
    
                    reponse_attendue = c + d * (c + e) - b * e
    
                    correction = (
                        f"Parenthèses : {a} + {b} = {a + b} "
                        f"et {c} + {e} = {c + e}. "
                        f"Division : {dividende} ÷ {a + b} = {c}. "
                        f"Multiplications : {d} × {c + e} = {d * (c + e)} "
                        f"et {b} × {e} = {b * e}. "
                        f"Enfin : {c} + {d * (c + e)} - {b * e} "
                        f"= {reponse_attendue}."
                    )                
                else:
                    a = random.randint(3, 8)
                    b = random.randint(2, 7)
                    c = random.randint(2, 6)
                    d = random.randint(2, 5)
                    e = random.randint(2, 6)
                    f = random.randint(2, 5)
                    g = random.randint(2, 6)
    
                    produit1 = a * (b + c)
                    produit2 = d * e
                    dividende = f * g
    
                    depart = produit1 + produit2 + random.randint(20, 50)
    
                    enonce = (
                        f"Calcule : {depart} - "
                        f"[{a} × ({b} + {c}) - {dividende} ÷ {f}] "
                        f"+ {d} × ({e} + {g})"
                    )
    
                    reponse_attendue = (
                        depart - (produit1 - g) + d * (e + g)
                    )
    
                    correction = (
                        f"Parenthèses : {b} + {c} = {b + c} "
                        f"et {e} + {g} = {e + g}. "
                        f"Multiplications : {a} × {b + c} = {produit1} "
                        f"et {d} × {e + g} = {d * (e + g)}. "
                        f"Division : {dividende} ÷ {f} = {g}. "
                        f"Crochets : {produit1} - {g} = {produit1 - g}. "
                        f"Enfin : {depart} - ({produit1 - g}) "
                        f"+ {d * (e + g)} = {reponse_attendue}."
                    )
            else:
                if difficulte == 1:
                    prix = random.randint(4, 12)
                    quantite = random.randint(5, 20)
                    transport = random.randint(10, 30)
                
                    enonce = (
                        f"Une classe achète {quantite} billets "
                        f"à {prix} € chacun. "
                        f"Le transport coûte {transport} €.\n\n"
                        f"1. Calcule le prix des billets.\n"
                        f"2. Calcule le coût total de la sortie.\n"
                        f"3. Écris une expression avec des "
                        f"parenthèses pour calculer ce coût."
                    )
                
                    reponse_attendue = None
                
                    correction = (
                        f"Prix des billets : {quantite} × {prix} "
                        f"= {quantite * prix} €.\n"
                        f"Coût total : {quantite * prix} + {transport} "
                        f"= {quantite * prix + transport} €.\n"
                        f"Expression : ({quantite} × {prix}) + {transport}."
                    )
                elif difficulte == 2:
                    prix = random.randint(5, 15)
                    quantite = random.randint(8, 25)
                    transport = random.randint(20, 60)
                    budget = quantite * prix + transport + random.randint(30, 100)

                    enonce = (
                        f"Une classe dispose de {budget} € pour une sortie.\n\n"
                        f"Elle achète {quantite} billets à {prix} € chacun.\n"
                        f"Le transport coûte {transport} €.\n\n"
                        f"1. Calcule le prix total des billets.\n"
                        f"2. Calcule la dépense totale.\n"
                        f"3. Calcule l'argent restant.\n"
                        f"4. Écris une expression avec des parenthèses pour calculer cet argent."
                    )

                    depense = quantite * prix + transport
                    reste = budget - depense

                    reponse_attendue = None

                    correction = (
                        f"1. Billets : {quantite} × {prix} = {quantite * prix} €.\n\n"
                        f"2. Dépense totale : {quantite * prix} + {transport} = {depense} €.\n\n"
                        f"3. Argent restant : {budget} - {depense} = {reste} €.\n\n"
                        f"4. Expression : {budget} - ({quantite} × {prix} + {transport}) = {reste} €."
                    ) 
    if partie == "Distributivité simple":
        if type_exercice == "Mes automatismes":

            def afficher_nombre(valeur):
                return f"{valeur:g}".replace(".", ",")

            questions = []
            corrections = []

            nombre_questions = difficulte + 1

            for i in range(1, nombre_questions + 1):

                if difficulte == 1:
                    k = random.randint(2, 5)
                    x = random.randint(2, 9)
                    y = random.randint(2, 9)
                    signe = "+"

                elif difficulte == 2:
                    k = random.randint(3, 8)
                    x = random.randint(10, 25)
                    y = random.randint(2, 9)
                    signe = random.choice(["+", "-"])

                else:
                    k = random.randint(4, 9)
                    x = random.randint(80, 350) / 10
                    y = random.randint(10, 75) / 10
                    signe = random.choice(["+", "-"])

                premier = round(k * x, 2)
                deuxieme = round(k * y, 2)

                if signe == "+":
                    resultat = round(premier + deuxieme, 2)
                else:
                    resultat = round(premier - deuxieme, 2)

                expression = (
                    f"{k} × ({afficher_nombre(x)} "
                    f"{signe} {afficher_nombre(y)})"
                )

                questions.append(f"{i}. {expression}")

                corrections.append(
                    f"{i}. {expression} = "
                    f"{k} × {afficher_nombre(x)} "
                    f"{signe} {k} × {afficher_nombre(y)} "
                    f"= {afficher_nombre(premier)} "
                    f"{signe} {afficher_nombre(deuxieme)} "
                    f"= {afficher_nombre(resultat)}"
                )

                champs_reponse.append({
                    "id": f"calcul_{i}",
                    "question": i,
                    "libelle": f"Résultat du calcul {i}",
                    "type": "nombre",
                    "attendu": resultat,
                    "unite": ""
                })

            enonce = (
                "Utilise la distributivité pour calculer :\n\n"
                + "\n\n".join(questions)
            )

            correction = "\n\n".join(corrections)
        elif type_exercice == "Je m'entraîne":

            if difficulte == 1:
                n = random.randint(5, 12)
                p1 = random.randint(3, 8)
                p2 = random.randint(1, 5)

                objet1, objet2 = random.choice([
                    ("cahier", "stylo"),
                    ("carnet", "crayon"),
                    ("bloc-notes", "feutre")
                ])
                objet1_pluriel = {
                    "cahier": "cahiers",
                    "carnet": "carnets",
                    "bloc-notes": "bloc-notes"
                }[objet1]
                

                supplement = random.randint(2, 5)
    
                attendu1 = n * (p1 + p2)
                attendu2 = attendu1 + supplement * p2
    
                enonce = (
                    f"Un club achète {n} lots de matériel. "
                    f"Chaque lot contient un {objet1} à {p1} € "
                    f"et un {objet2} à {p2} €.\n\n"
                    f"Le club achète également {supplement} "
                    f"{objet2}s supplémentaires à {p2} € chacun.\n\n"
                    f"1. Combien coûtent les {n} lots ?\n"
                    f"2. Quel est le prix total de l'achat ?"
                )
    
                correction = (
                    f"1. Prix des lots :\n"
                    f"{n} × ({p1} + {p2})\n"
                    f"= {n} × {p1} + {n} × {p2}\n"
                    f"= {n * p1} + {n * p2}\n"
                    f"= {attendu1} €.\n\n"
                    f"2. Prix des objets supplémentaires :\n"
                    f"{supplement} × {p2} = {supplement * p2} €.\n"
                    f"Prix total : {attendu1} + {supplement * p2} "
                    f"= {attendu2} €."
                )
    
                libelle1 = "Prix des lots"
                libelle2 = "Prix total de l'achat"
                modele = random.choice([
                    "lots", "atelier", "comparaison", "erreur"
                ])
    
                if modele == "atelier":
                    frais = random.randint(10, 30)
    
                    attendu1 = n * (p1 + p2)
                    attendu2 = attendu1 + frais
    
                    enonce = (
                        f"Une association organise un atelier pour {n} élèves. "
                        f"Chaque élève reçoit un carnet à {p1} € "
                        f"et un feutre à {p2} €. "
                        f"La location de la salle coûte {frais} €.\n\n"
                        f"1. Combien coûtent tous les carnets et feutres ?\n"
                        f"2. Quel est le coût total de l'atelier ?"
                    )
    
                    correction = (
                        f"1. On utilise la distributivité :\n"
                        f"{n} × ({p1} + {p2}) "
                        f"= {n} × {p1} + {n} × {p2}\n"
                        f"= {n * p1} + {n * p2} = {attendu1} €.\n"
                        f"2. {attendu1} + {frais} = {attendu2} €."
                    )
    
                    libelle1 = "Prix du matériel"
                    libelle2 = "Coût total de l'atelier"
    
                elif modele == "comparaison":
                    prix_a = p1 + p2
                    prix_b = p1
    
                    supplement = random.randint(2, 5)
        
                    attendu1 = n * (p1 + p2)
                    attendu2 = attendu1 + supplement * p2
        
                    enonce = (
                        f"Un club achète {n} lots de matériel. "
                        f"Chaque lot contient un {objet1} à {p1} € "
                        f"et un {objet2} à {p2} €.\n\n"
                        f"Le club achète également {supplement} "
                        f"{objet2}s supplémentaires à {p2} € chacun.\n\n"
                        f"1. Combien coûtent les {n} lots ?\n"
                        f"2. Quel est le prix total de l'achat ?"
                    )
        
                    correction = (
                        f"1. Prix des lots :\n"
                        f"{n} × ({p1} + {p2})\n"
                        f"= {n} × {p1} + {n} × {p2}\n"
                        f"= {n * p1} + {n * p2}\n"
                        f"= {attendu1} €.\n\n"
                        f"2. Prix des objets supplémentaires :\n"
                        f"{supplement} × {p2} = {supplement * p2} €.\n"
                        f"Prix total : {attendu1} + {supplement * p2} "
                        f"= {attendu2} €."
                    )
        
                    libelle1 = "Prix des lots"
                    libelle2 = "Prix total de l'achat"

                elif modele == "erreur":
                    attendu1 = n * p1 + p2
                    attendu2 = n * (p1 + p2)
    
                    enonce = (
                        f"Un atelier prépare {n} kits. "
                        f"Chaque kit contient du matériel à {p1} € "
                        f"et un accessoire à {p2} €.\n\n"
                        f"Pour calculer le prix total, Lila écrit : "
                        f"{n} × {p1} + {p2}.\n\n"
                        f"1. Quel résultat trouve Lila ?\n"
                        f"2. Quel est le prix total correct des kits ?"
                    )
    
                    correction = (
                        f"1. Calcul de Lila : {n} × {p1} + {p2} "
                        f"= {n * p1} + {p2} = {attendu1} €.\n"
                        f"2. Lila a oublié de multiplier "
                        f"le prix de l'accessoire par {n}.\n"
                        f"Le calcul correct est :\n"
                        f"{n} × ({p1} + {p2}) "
                        f"= {n} × {p1} + {n} × {p2}\n"
                        f"= {n * p1} + {n * p2} = {attendu2} €."
                    )
    
                    libelle1 = "Résultat trouvé par Lila"
                    libelle2 = "Prix total correct"

            elif difficulte == 2:
                n = random.randint(6, 15)
                prix = random.randint(12, 25)
                remise = random.randint(2, 8)
                livraison = random.randint(5, 15)
    
                produit = random.choice([
                    "jeux de cartes",
                    "mangas d'occasion",
                    "kits créatifs"
                ])
    
                attendu1 = n * prix
                prix_remise = n * (prix - remise)
                depense = prix_remise + livraison
    
                budget = depense + random.randint(20, 80)
                attendu2 = budget - depense
    
                enonce = (
                    f"Une association dispose d'un budget "
                    f"de {budget} €.\n\n"
                    f"Elle commande {n} {produit}.\n"
                    f"Le prix affiché est de {prix} € par article.\n"
                    f"Le vendeur accorde ensuite une remise "
                    f"de {remise} € sur chaque article.\n"
                    f"La livraison coûte {livraison} €.\n\n"
                    f"1. Quel est le prix total des articles "
                    f"au prix affiché, hors livraison ?\n"
                    f"2. Combien d'argent restera-t-il "
                    f"sur le budget après paiement ?"
                )
    
                correction = (
                    f"1. Prix initial :\n"
                    f"{n} × {prix} = {attendu1} €.\n\n"
                    f"2. Réduction totale :\n"
                    f"{n} × {remise} = {n * remise} €.\n"
                    f"Prix après réduction :\n"
                    f"{n} × ({prix} - {remise}) "
                    f"= {attendu1} - {n * remise} "
                    f"= {prix_remise} €.\n"
                    f"Avec la livraison :\n"
                    f"{prix_remise} + {livraison} "
                    f"= {depense} €.\n"
                    f"Budget restant :\n"
                    f"{budget} - {depense} = {attendu2} €."
                )
    
                libelle1 = "Prix initial des articles"
                libelle2 = "Budget restant"


            else:
                na = random.randint(7, 13)
                nb = random.randint(5, 11)
    
                p1 = random.randint(3, 7)
                p2 = random.randint(2, 6)
                p3 = random.randint(4, 9)
                p4 = random.randint(2, 7)
    
                remise = random.randint(2, 4)
                livraison = random.randint(6, 18)
    
                cout_a = na * (p1 + p2)
                cout_b = nb * (p3 + p4)
    
                attendu1 = cout_a + cout_b
    
                remise_totale = nb * remise
                depense = attendu1 - remise_totale + livraison
    
                budget = depense + random.randint(30, 90)
                attendu2 = budget - depense
    
                enonce = (
                    f"Un club dispose d'un budget de {budget} €.\n\n"
                    f"Il commande {na} lots A contenant chacun "
                    f"un carnet à {p1} € et un crayon à {p2} €.\n\n"
                    f"Il commande également {nb} lots B contenant "
                    f"chacun un album à {p3} € et un feutre à {p4} €.\n\n"
                    f"Le vendeur accorde ensuite une remise de "
                    f"{remise} € sur chaque lot B.\n"
                    f"La livraison coûte {livraison} €.\n\n"
                    f"1. Quel est le coût total des lots A et B "
                    f"avant remise, hors livraison ?\n"
                    f"2. Combien d'argent restera-t-il au club "
                    f"après paiement ?"
                )
    
                correction = (
                    f"1. Coût des lots A :\n"
                    f"{na} × ({p1} + {p2}) "
                    f"= {na} × {p1} + {na} × {p2} "
                    f"= {cout_a} €.\n\n"
                    f"Coût des lots B :\n"
                    f"{nb} × ({p3} + {p4}) "
                    f"= {nb} × {p3} + {nb} × {p4} "
                    f"= {cout_b} €.\n\n"
                    f"Coût total avant remise :\n"
                    f"{cout_a} + {cout_b} = {attendu1} €.\n\n"
                    f"2. Remise totale :\n"
                    f"{nb} × {remise} = {remise_totale} €.\n"
                    f"Dépense après remise et livraison :\n"
                    f"{attendu1} - {remise_totale} "
                    f"+ {livraison} = {depense} €.\n"
                    f"Budget restant :\n"
                    f"{budget} - {depense} = {attendu2} €."
                )
    
                libelle1 = "Coût total avant remise"
                libelle2 = "Budget restant"
            
            champs_reponse = [
                {
                    "id": "question_1",
                    "question": 1,
                    "libelle": libelle1,
                    "type": "nombre",
                    "attendu": attendu1,
                    "unite": "€"
                },
                {
                    "id": "question_2",
                    "question": 2,
                    "libelle": libelle2,
                    "type": "nombre",
                    "attendu": attendu2,
                    "unite": "€"
                }
            ]            
    if enonce is None:
        enonce = f"Exercices à développer pour : {partie}"
        correction = "Correction non disponible."
    return {
        "enonce": enonce,
        "correction": correction,
        "reponse_attendue": reponse_attendue,
        "champs_reponse": champs_reponse
    }
   
if "exercices_actuels" not in st.session_state:
    st.session_state.exercices_actuels = []
if st.button("Générer mes exercices"):
        if (
            chapitre == "1. Opérations"
            and type_exercice == "Je résous des problèmes"
        ):
            
            exercices = generer_exercices_priorites(difficulte, nombre)
                    
        elif type_exercice == "Je résous des problèmes":
                try:
                    exercices = generer_exercice_ia(
                        chapitre, partie, difficulte, type_exercice, nombre
                    )
                except Exception:
                    try:
                        exercices = generer_exercice_groq(
                            chapitre, partie, difficulte, type_exercice, nombre
                        )
                    except Exception:
                        st.info(
                            "Les IA sont temporairement indisponibles. "
                            "Des exercices alternatifs ont été générés."
                        )
                        exercices = [
                            generer_exercice(chapitre, partie, difficulte, type_exercice)
                            for _ in range(nombre)
                        ]
        else:
            import random

            if chapitre == "1. Opérations":
                notions_disponibles = chapitres[chapitre]
                notions = notions_disponibles.copy()
                random.shuffle(notions)

                while len(notions) < nombre:
                    notions += random.sample(
                        notions_disponibles,
                        min(nombre - len(notions), len(chapitres[chapitre]))
                    )

                exercices = [
                    generer_exercice(
                        chapitre, notions[i], difficulte, type_exercice
                    )
                    for i in range(nombre)
                ]
            else:
                exercices = [
                    generer_exercice(
                        chapitre, partie, difficulte, type_exercice
                    )
                    for _ in range(nombre)
                ]
        st.session_state.exercices_actuels = exercices
        st.session_state["serie_ouverte_depuis_liste"] = False
        st.session_state["serie_version"] = st.session_state.get("serie_version", 0) + 1
    
        if st.session_state.get("eleve_id"):
            try:
                code = sauvegarder_serie(exercices)
                if code:
                    st.session_state.code_actuel = code
                    st.success("Exercices générés et sauvegardés !")
                else:
                    st.error("Sauvegarde impossible.")
            except Exception:
                st.error("Sauvegarde impossible.")
        else:
            st.session_state.code_actuel = None
            st.info("Connecte-toi pour sauvegarder tes exercices.")
if st.session_state.get("serie_ouverte_depuis_liste", False):
    zone_affichage = zone_serie_ouverte
else:
    zone_affichage = st.container()

with zone_affichage:
    if st.session_state.exercices_actuels:
        for numero, exercice in enumerate(st.session_state.exercices_actuels, start=1):
            st.subheader(f"Exercice {numero}")
            st.write(exercice["enonce"])
    
            if exercice.get("reponse_attendue") is not None:
                reponse_eleve = st.number_input(
                    "Ta réponse :",
                     value=None,
                     step=0.01 if isinstance(exercice.get("reponse_attendue"), float) else 1,
                     key=f"reponse_{st.session_state.get('serie_version', 0)}_{numero}",
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
            elif exercice.get("champs_reponse"):
                for champ in exercice["champs_reponse"]:
                    etiquette = f"Question {champ['question']} — {champ['libelle']}"
                    cle = f"banque_{st.session_state.get('serie_version', 0)}_{numero}_{champ['id']}"
    
                    if champ["type"] == "nombre":
                        st.text_input(
                            etiquette,
                            placeholder=f"Réponse en {champ.get('unite', 'nombre')}",
                            key=cle,
                            on_change=enregistrer_reponses_banque_auto,
                            args=(numero,)
                        )
    
                    elif champ["type"] == "choix":
                        st.selectbox(
                            etiquette,
                            ["Choisir..."] + champ["options"],
                            key=cle,
                            on_change=enregistrer_reponses_banque_auto,
                            args=(numero,)
                        )
    
                    elif champ["type"] == "texte_libre":
                        st.text_area(
                            etiquette,
                            height=90,
                            key=cle,
                            on_change=enregistrer_reponses_banque_auto,
                            args=(numero,)
                        )
                if st.button(
                    "Vérifier mes réponses",
                    key=f"verifier_banque_{st.session_state.get('serie_version', 0)}_{numero}"
                ):
                    bonnes_reponses = 0
                    total_reponses = sum(
                        1 for champ in exercice["champs_reponse"]
                        if champ["type"] != "texte_libre"
                    )
                    for champ in exercice["champs_reponse"]:
                        if champ["type"] == "texte_libre":
                            continue
    
                        cle = (
                            f"banque_{st.session_state.get('serie_version', 0)}"
                            f"_{numero}_{champ['id']}"
                        )
                        saisie = st.session_state.get(cle, "")
    
                        if saisie in ("", "Choisir..."):
                            st.warning(f"{champ['libelle']} : réponse manquante.")
                            continue
    
                        if champ["type"] == "nombre":
                            try:
                                correcte = (
                                    float(str(saisie).replace(",", "."))
                                    == float(champ["attendu"])
                                )
                            except (ValueError, TypeError):
                                correcte = False
                        else:
                            correcte = saisie == champ["attendu"]
    
                        if correcte and champ["type"] == "choix":
                            calculs_corrects = True
                            dependances = champ.get("dependances", [])

                            for autre in exercice["champs_reponse"]:
                                if autre["id"] not in dependances:
                                    continue
        
                                if autre["type"] != "nombre":
                                    continue
        
                                autre_cle = (
                                    f"banque_{st.session_state.get('serie_version', 0)}"
                                    f"_{numero}_{autre['id']}"
                                )
        
                                valeur = st.session_state.get(autre_cle, "")
        
                                try:
                                    valeur_saisie = float(
                                        str(valeur).replace(",", ".")
                                    )
                                    valeur_attendue = float(autre["attendu"])
        
                                    if abs(valeur_saisie - valeur_attendue) > 1e-6:
                                        calculs_corrects = False
        
                                except (ValueError, TypeError):
                                    calculs_corrects = False

    
                            if calculs_corrects:
                                bonnes_reponses += 1
                                st.markdown(f"✓ {champ['libelle']} : :green[Bonne réponse !]")
                            else:
                                st.markdown(
                                    ":orange[⚠ Bon choix, mais certains calculs sont faux "
                                    "ou incomplets. Vérifie-les.]"
                                )
    
                        elif correcte:
                            bonnes_reponses += 1
                            st.markdown(f"✓ {champ['libelle']} : :green[Bonne réponse !]")
    
                        else:
                            st.markdown(f"✗ {champ['libelle']} : :red[Essaie encore.]")
                    st.markdown("---")
                    texte_score = (
                        "bonne réponse" if bonnes_reponses == 1
                        else "bonnes réponses"
                    )
                    st.markdown(
                        f"**Résultat : {bonnes_reponses} "
                        f"{texte_score} sur {total_reponses}**"
                    )
                    code = st.session_state.get("code_actuel")
    
                    if code and st.session_state.get("eleve_id"):
                        reponses_banque = {}
    
                        for champ in exercice["champs_reponse"]:
                            cle = (
                                f"banque_{st.session_state.get('serie_version', 0)}"
                                f"_{numero}_{champ['id']}"
                            )
                            reponses_banque[champ["id"]] = st.session_state.get(cle, "")
    
                        sauvegarder_reponse(
                            code,
                            numero,
                            {
                                "type": "banque",
                                "champs": reponses_banque,
                                "bilan": {
                                    "bonnes": bonnes_reponses,
                                    "total": total_reponses
                                }
                            }
                        )
                cle_bilan = (
                    f"bilan_banque_{st.session_state.get('serie_version', 0)}"
                    f"_{numero}"
                )
    
                bilan = st.session_state.get(cle_bilan)
    
                if isinstance(bilan, dict):
                    st.markdown(
                        f"**Dernier bilan enregistré : "
                        f"{bilan['bonnes']} bonnes réponses "
                        f"sur {bilan['total']}**"
                    )    
            else:
                st.text_area(
                    "Ta réponse :",
                    placeholder="Écris ici tes réponses aux questions de l'exercice.",
                    height=150,
                    key=f"reponse_texte_{st.session_state.get('serie_version', 0)}_{numero}"
                )
                
            with st.expander(
                f"Voir la correction{'​' * (st.session_state.get('serie_version', 0) + 1)}",
                expanded=False
            ):
                st.markdown(exercice["correction"].replace("\n", "  \n"))
            
