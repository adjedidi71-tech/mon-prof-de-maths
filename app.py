import streamlit as st
import time
from html import escape
from pathlib import Path
from io import BytesIO
import base64
import re
from uuid import uuid4
from PIL import Image, ImageOps, UnidentifiedImageError
from google import genai
from groq import Groq
from banque_priorites import generer_exercices_priorites
from supabase import create_client
from mathicap_accueil import afficher_interface_mathicap, _styles as styles_mathicap_communs
from auth_persistante import (
    enregistrer_session,
    supprimer_session,
    effacer_jeton_navigateur,
    enregistrer_jeton_navigateur,
    lire_jeton_navigateur,
    verifier_session
)


# Configuration avant l'affichage du composant navigateur (Streamlit v2).
st.set_page_config(
    page_title="MathiCap Collège",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Mesure facultative des opérations de navigation : ?mesure_nav=1
# Cette instrumentation est désactivée en usage normal.
_mc_nav_debut = time.perf_counter()
_mc_nav_mesure = st.query_params.get("mesure_nav") == "1"


def _mathicap_correction_division_euclidienne(dividende, diviseur, quotient, reste):
    """Présente le quotient, le reste et l'égalité euclidienne pour un collégien."""
    produit = diviseur * quotient
    return (
        f"**{dividende} ÷ {diviseur} → quotient {quotient}, reste {reste}.**\n\n"
        f"**Écriture de la division euclidienne :**\n\n"
        f"{dividende} = {diviseur} × {quotient} + {reste}\n\n"
        f"**Vérification :** {diviseur} × {quotient} = {produit}, "
        f"puis {produit} + {reste} = {dividende}.\n\n"
        f"Le reste {reste} est inférieur au diviseur {diviseur}."
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


# Gestion des mots de passe : API publique Supabase Auth, sans accès administrateur.
def _mathicap_client_auth_temporaire():
    # Un client par opération évite de partager la session d'un élève avec un autre.
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


def _mathicap_mot_de_passe_valide(valeur):
    return len(valeur) >= 10 and len(valeur) <= 128


# Champs sensibles : toujours purgés AVANT leur reconstruction par Streamlit.
# Ne jamais modifier la valeur d'un widget déjà créé pendant le même rerun.
_CHAMPS_MDP_RECUP = (
    "mathicap_recup_email",
    "mathicap_recup_code",
    "mathicap_recup_nouveau",
    "mathicap_recup_confirmation",
)
_CHAMPS_MDP_PROFIL = (
    "mathicap_mdp_profil_actuel",
    "mathicap_mdp_profil_nouveau",
    "mathicap_mdp_profil_confirmation",
)


def _mathicap_effacer_champs_mdp(champs):
    for nom in champs:
        st.session_state.pop(nom, None)


def _mathicap_formulaire_recuperation():
    """Récupération en deux étapes, avec une seule adresse e-mail."""
    st.markdown("### Réinitialiser mon mot de passe")
    adresse_confirmee = st.session_state.get("mathicap_recup_adresse", "")

    # Largeur maîtrisée sur PC, fluide sur smartphone.
    with st.container(key="mathicap_recup_etroit"):
        if not adresse_confirmee:
            st.caption("Un code de vérification sera envoyé à ton adresse e-mail.")
            with st.form("mathicap_demande_recuperation"):
                adresse = st.text_input(
                    "Adresse e-mail du compte",
                    value=st.session_state.get("email_connexion", ""),
                    key="mathicap_recup_email",
                )
                demander = st.form_submit_button("Recevoir un code")

            if demander:
                if not adresse.strip() or "@" not in adresse:
                    st.warning("Saisis une adresse e-mail valide.")
                else:
                    try:
                        _mathicap_client_auth_temporaire().auth.reset_password_for_email(
                            adresse.strip()
                        )
                        st.session_state["mathicap_recup_adresse"] = adresse.strip()
                        st.rerun()
                    except Exception:
                        st.error("Envoi momentanément impossible. Réessaie plus tard.")
        else:
            st.info(
                "Si cette adresse possède un compte, un code a été envoyé à "
                f"{adresse_confirmee}. Vérifie aussi les indésirables.",
                width=500,
            )
            with st.form("mathicap_validation_recuperation"):
                code = st.text_input(
                    "Code reçu par e-mail",
                    key="mathicap_recup_code",
                    max_chars=10,
                    help="Saisis tous les chiffres du code envoyé par Supabase. "
                         "Sa longueur dépend des réglages de ton projet (6 à 10 chiffres).",
                )
                nouveau = st.text_input(
                    "Nouveau mot de passe (10 caractères minimum)",
                    type="password",
                    key="mathicap_recup_nouveau",
                )
                confirmation = st.text_input(
                    "Confirmer le nouveau mot de passe",
                    type="password",
                    key="mathicap_recup_confirmation",
                )
                valider = st.form_submit_button("Enregistrer mon nouveau mot de passe")

            if valider:
                code_normalise = code.strip()
                if not (code_normalise.isascii() and code_normalise.isdigit()
                        and 6 <= len(code_normalise) <= 10):
                    st.warning("Saisis le code numérique complet reçu par e-mail.")
                elif not _mathicap_mot_de_passe_valide(nouveau):
                    st.warning("Choisis un mot de passe entre 10 et 128 caractères.")
                elif nouveau != confirmation:
                    st.warning("Les deux mots de passe ne correspondent pas.")
                else:
                    try:
                        client = _mathicap_client_auth_temporaire()
                        resultat = client.auth.verify_otp({
                            "email": adresse_confirmee,
                            "token": code_normalise,
                            "type": "recovery",
                        })
                        if not resultat.session or not resultat.user:
                            raise ValueError("Vérification refusée")
                        client.auth.update_user({"password": nouveau})
                        client.auth.sign_out()
                        # Les champs seront purgés avant le prochain affichage.
                        # Le formulaire disparaît, et la connexion redevient visible.
                        st.session_state["mathicap_recup_succes_email"] = adresse_confirmee
                        st.session_state["mathicap_afficher_recuperation"] = False
                        st.session_state.pop("mathicap_recup_adresse", None)
                        st.rerun()
                    except Exception:
                        st.error(
                            "Code invalide ou expiré, ou modification impossible. "
                            "Demande un nouveau code si nécessaire."
                        )

            if st.button(
                "Utiliser une autre adresse e-mail",
                key="mathicap_recup_autre_email",
            ):
                st.session_state.pop("mathicap_recup_adresse", None)
                # Effacement réalisé avant de réafficher les champs.
                st.session_state["mathicap_recup_recommencer"] = True
                st.rerun()

        if st.button("Retour à la connexion", key="mathicap_retour_connexion_mdp"):
            st.session_state["mathicap_afficher_recuperation"] = False
            st.session_state.pop("mathicap_recup_adresse", None)
            st.session_state["mathicap_recup_recommencer"] = True
            st.rerun()


def _mathicap_formulaire_changement_mdp(email_compte, identifiant):
    # Au rerun suivant une réussite : vider les trois champs et fermer le volet.
    if st.session_state.pop("mathicap_mdp_profil_replier", False):
        _mathicap_effacer_champs_mdp(_CHAMPS_MDP_PROFIL)
        st.session_state["mathicap_mdp_profil_ouvert"] = False

    if st.session_state.pop("mathicap_mdp_profil_succes", False):
        st.toast("Mot de passe modifié. Utilise-le lors de ta prochaine connexion.", icon="✅", duration=3)

    with st.expander(
        "Changer mon mot de passe",
        expanded=False,
        key="mathicap_mdp_profil_ouvert",
        width=500,
        on_change="rerun",
    ):
        st.caption("Pour protéger ton compte, confirme ton mot de passe actuel.")
        with st.container(key="mathicap_mdp_profil_etroit"):
            with st.form("mathicap_changement_mdp", border=False):
                actuel = st.text_input(
                    "Mot de passe actuel",
                    type="password",
                    key="mathicap_mdp_profil_actuel",
                )
                nouveau = st.text_input(
                    "Nouveau mot de passe (10 caractères minimum)",
                    type="password",
                    key="mathicap_mdp_profil_nouveau",
                )
                confirmation = st.text_input(
                    "Confirmer le nouveau mot de passe",
                    type="password",
                    key="mathicap_mdp_profil_confirmation",
                )
                changer = st.form_submit_button("Modifier mon mot de passe")

        if changer:
            if not email_compte or not actuel:
                st.warning("Le mot de passe actuel est nécessaire.")
            elif not _mathicap_mot_de_passe_valide(nouveau):
                st.warning("Choisis un mot de passe entre 10 et 128 caractères.")
            elif nouveau != confirmation:
                st.warning("Les deux nouveaux mots de passe ne correspondent pas.")
            elif actuel == nouveau:
                st.warning("Le nouveau mot de passe doit être différent de l'ancien.")
            else:
                try:
                    client = _mathicap_client_auth_temporaire()
                    resultat = client.auth.sign_in_with_password({
                        "email": email_compte,
                        "password": actuel,
                    })
                    if not resultat.user or resultat.user.id != identifiant:
                        raise ValueError("Compte incorrect")
                    client.auth.update_user({"password": nouveau})
                    client.auth.sign_out()
                    st.session_state["mathicap_mdp_profil_replier"] = True
                    st.session_state["mathicap_mdp_profil_succes"] = True
                    st.rerun()
                except Exception:
                    st.error(
                        "Modification impossible. Vérifie ton mot de passe actuel "
                        "ou réessaie plus tard."
                    )

# Le pont navigateur doit être monté une seule fois, à chaque exécution,
# y compris lorsque l'élève est connecté (sauvegarde/suppression du jeton).
jeton_navigateur = lire_jeton_navigateur()

if not st.session_state.get("eleve_id"):
    jeton = jeton_navigateur
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
            # V7: verification recente reutilisee au plus 15 s, pour ce jeton uniquement.
            eleve_id = verifier_session(supabase_privee, jeton, cache_seconds=15)
        except Exception:
            eleve_id = None
    else:
        eleve_id = None

    if not eleve_id or eleve_id != st.session_state["eleve_id"]:
        st.session_state.pop("eleve_id", None)
        st.session_state.pop("jeton_persistant", None)
        st.session_state.pop("session_eleve", None)

_mc_nav_auth_ms = round((time.perf_counter() - _mc_nav_debut) * 1000)

from pathlib import Path
# EN-TÊTE MATHICAP + COMPTE ÉLÈVE
# Remplacer l'ancien affichage du grand logo ET tout l'ancien bloc
# « Mon compte élève » par ce code.
# Ne pas modifier les 2 lignes « afficher_interface_mathicap() »
# ni « chapitres = { » plus bas.
# Réinitialiser les champs AVANT leur éventuelle création.
if st.session_state.pop("vider_champs_connexion", False):
    st.session_state["email_connexion"] = ""
    st.session_state["mdp_connexion"] = ""

est_connecte = bool(st.session_state.get("eleve_id"))
# Synchronisation de la classe avec le compte Supabase
CLASSES_MATHICAP = ("6e", "5e", "4e", "3e")


def _mathicap_initiale_pseudo(pseudo):
    """Première lettre du pseudo, sans exiger de nom ni de prénom."""
    if not isinstance(pseudo, str):
        return ""
    return next((caractere.upper()[0] for caractere in pseudo if caractere.isalpha()), "")


if est_connecte:
    identifiant = st.session_state["eleve_id"]

    if st.session_state.get("_classe_identifiant") != identifiant:
        # Une autre connexion ne doit jamais reprendre l'avatar de l'ancien compte.
        st.session_state["mathicap_avatar_type"] = "defaut"
        st.session_state["mathicap_avatar_choix"] = ""
        st.session_state["mathicap_avatar_fichier"] = ""
        st.session_state["mathicap_avatar_pseudo"] = ""
        try:
            compte = supabase_privee.auth.admin.get_user_by_id(identifiant)
            donnees_compte = compte.user.user_metadata or {}
            classe_compte = donnees_compte.get("mathicap_classe")
            st.session_state["mathicap_avatar_pseudo"] = donnees_compte.get("pseudo") or ""
            st.session_state["mathicap_avatar_type"] = donnees_compte.get(
                "mathicap_avatar_type", "defaut"
            )
            st.session_state["mathicap_avatar_choix"] = donnees_compte.get(
                "mathicap_avatar_choix", ""
            )
            st.session_state["mathicap_avatar_fichier"] = donnees_compte.get(
                "mathicap_avatar_fichier", ""
            )

            st.session_state["mathicap_classe"] = (
                classe_compte
                if classe_compte in CLASSES_MATHICAP
                else "5e"
            )
            st.session_state["_classe_enregistree"] = classe_compte
            st.session_state["_classe_identifiant"] = identifiant

        except Exception:
            st.warning("Impossible de récupérer la classe du compte.")

    classe_choisie = st.session_state.get("mathicap_classe")

    if (
        st.session_state.get("_classe_identifiant") == identifiant
        and classe_choisie in CLASSES_MATHICAP
        and classe_choisie != st.session_state.get("_classe_enregistree")
    ):
        try:
            compte = supabase_privee.auth.admin.get_user_by_id(identifiant)
            infos = dict(compte.user.user_metadata or {})
            infos["mathicap_classe"] = classe_choisie

            supabase_privee.auth.admin.update_user_by_id(
                identifiant,
                {"user_metadata": infos}
            )

            st.session_state["_classe_enregistree"] = classe_choisie

        except Exception:
            st.warning("Impossible d'enregistrer la classe.")

else:
    st.session_state.pop("_classe_identifiant", None)
    st.session_state.pop("_classe_enregistree", None)
    st.session_state.pop("mathicap_avatar_type", None)
    st.session_state.pop("mathicap_avatar_choix", None)
    st.session_state.pop("mathicap_avatar_fichier", None)
    st.session_state.pop("mathicap_avatar_pseudo", None)
styles_mathicap_communs()

st.markdown("""
<style>

/* En-tête : les trois boutons ont de vraies zones de clic. */
.st-key-mathicap_zone_profil {
    position: relative !important;
    transform: translateY(-30px) !important;
    width: calc(var(--mc-avatar) + var(--mc-ico) + var(--mc-ico-gap)) !important;
    min-width: calc(var(--mc-avatar) + var(--mc-ico) + var(--mc-ico-gap)) !important;
}

.st-key-mathicap_zone_profil .st-key-mathicap_avatar_clic {
    position: static !important;
    width: var(--mc-avatar) !important;
    min-width: var(--mc-avatar) !important;
    max-width: var(--mc-avatar) !important;
    height: var(--mc-avatar) !important;
    min-height: var(--mc-avatar) !important;
    max-height: var(--mc-avatar) !important;
    margin: 0 !important;
    padding: 0 !important;
    z-index: 10 !important;
}

.st-key-mathicap_zone_profil .st-key-mathicap_avatar_clic [data-testid="stButton"],
.st-key-mathicap_zone_profil .st-key-mathicap_avatar_clic button {
    width: 100% !important;
    height: 100% !important;
    min-height: 0 !important;
}

.st-key-mathicap_zone_profil .st-key-mathicap_avatar_clic button {
    padding: 0 !important;
    border: none !important;
    border-radius: 50% !important;
    background: transparent !important;
    box-shadow: none !important;
    font-size: 0 !important;
    color: transparent !important;
    cursor: pointer !important;
}

.st-key-mathicap_zone_profil .st-key-mathicap_avatar_clic button:focus-visible {
    outline: 2px solid #2563eb !important;
    outline-offset: 3px !important;
}
.st-key-mathicap_zone_profil
.st-key-mathicap_avatar_clic button p {
    opacity: 0 !important;
}
/* ============================================================
   EN-TÊTE MATHICAP : tout est limité à l'en-tête
   (classes .mathicap-* et clé mathicap_zone_profil)
   ============================================================ */

/* Conteneur de l'en-tête : grille « logo flexible | compte à largeur automatique » */
[data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic) {
    /* Tailles ordinateur (> 1024 px) */
    /* Logo et slogan utilisent une dimension de référence commune. */
    --mc-brand-w: 250px;
    --mc-logo-w: var(--mc-brand-w);
    --mc-slogan: calc(var(--mc-brand-w) * 0.078);
    --mc-ico: 40px;
    --mc-avatar: 52px;
    --mc-ico-gap: 18px;
    --mc-statut: 14px;
    --mc-btn-h: 32px;
    --mc-btn-fs: 13px;

    display: grid !important;
    /* La recherche occupe jusqu'à 320px, mais se réduit progressivement
       avec la fenêtre plutôt que d'empiéter sur la marque ou le profil. */
    grid-template-columns:
        minmax(0, 1fr)
        minmax(0, clamp(180px, calc(100vw - 430px), 320px))
        auto !important;
    align-items: start !important;
    column-gap: 12px !important;
    row-gap: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: clip !important;
}

[data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic)
> [data-testid="stColumn"] {
    flex: none !important;
    width: auto !important;
    min-width: 0 !important;
    max-width: 100% !important;
}

/* Dans la grille de l'en-tête, chaque bloc a un emplacement identifié. */
[data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic)
> [data-testid="stColumn"]:nth-child(2) {
    width: 100% !important;
    max-width: 320px !important;
    min-width: 0 !important;
    justify-self: end !important;
}
[data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic)
> [data-testid="stColumn"]:nth-child(3) {
    justify-self: end !important;
}

/* Le vrai bouton Streamlit porte directement le logo et le slogan.
   Il n'y a plus de bouton transparent superposé à une image. */
.st-key-mathicap_logo_clic {
    width: var(--mc-brand-w) !important;
    min-width: 0 !important;
    max-width: 100% !important;
}

.st-key-mathicap_logo_clic [data-testid="stButton"] {
    display: block !important;
    width: 100% !important;
}

.st-key-mathicap_logo_clic button {
    position: relative !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
    justify-content: flex-start !important;
    gap: calc(var(--mc-brand-w) * 0.016) !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    height: auto !important;
    min-height: 0 !important;
    padding: 0 !important;
    border: none !important;
    border-radius: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
    text-align: left !important;
    cursor: pointer !important;
}

/* L'image est peinte directement sur le bouton : toute l'image est cliquable.
   L'aspect-ratio réel de l'image et son contenu sont précisés plus bas. */
.st-key-mathicap_logo_clic button::before {
    content: "";
    display: block !important;
    width: 100% !important;
    flex: none !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    background-size: 100% 100% !important;
    pointer-events: none !important;
}

.st-key-mathicap_logo_clic button::after {
    content: "J'apprends  •  Je réussis";
    display: block !important;
    width: 100% !important;
    font-size: var(--mc-slogan) !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
    letter-spacing: 0 !important;
    white-space: nowrap !important;
    text-align: left !important;
    background: linear-gradient(90deg, #0b3d91 0%, #1f7ae0 55%, #f3a11a 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    pointer-events: none !important;
}

/* Le libellé pour lecteurs d'écran n'ajoute aucune hauteur au bouton. */
.st-key-mathicap_logo_clic button [data-testid="stMarkdownContainer"] {
    position: absolute !important;
    width: 1px !important;
    height: 1px !important;
    overflow: hidden !important;
    clip-path: inset(50%) !important;
}

.st-key-mathicap_logo_clic button p {
    position: absolute !important;
    width: 1px !important;
    height: 1px !important;
    overflow: hidden !important;
    clip-path: inset(50%) !important;
    white-space: nowrap !important;
    padding: 0 !important;
    margin: 0 !important;
}

.st-key-mathicap_logo_clic button:focus-visible {
    outline: 2px solid #2563eb !important;
    outline-offset: 3px !important;
}

/* Zone compte : tout aligné à droite */
.st-key-mathicap_zone_profil [data-testid="stVerticalBlock"] {
    gap: 12px !important;
    align-items: flex-end !important;
}

.st-key-mathicap_zone_profil .mathicap-connecte {
    display: block !important;
    padding-bottom: 6px !important;
}

.st-key-mathicap_zone_profil [data-testid="stElementContainer"] {
    width: 100% !important;
}

/* Cloche et avatar placés côte à côte dans un vrai conteneur horizontal.
   Aucun bouton n'est superposé : les deux restent visibles sur smartphone. */
.st-key-mathicap_icones_actions,
.st-key-mathicap_icones_actions [data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    justify-content: flex-end !important;
    align-items: center !important;
    column-gap: var(--mc-ico-gap) !important;
    width: 100% !important;
    min-width: 0 !important;
    overflow: visible !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_icones_actions [data-testid="stElementContainer"] {
    flex: 0 0 auto !important;
    width: auto !important;
    min-width: 0 !important;
    max-width: none !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_icones_actions .st-key-mathicap_notifications_clic {
    flex: 0 0 var(--mc-ico) !important;
    width: var(--mc-ico) !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_icones_actions .st-key-mathicap_avatar_clic {
    flex: 0 0 var(--mc-avatar) !important;
    width: var(--mc-avatar) !important;
}

/* Cloche : bouton natif avec une surface de clic stable sur tous les écrans. */
.st-key-mathicap_zone_profil .st-key-mathicap_notifications_clic {
    position: static !important;
    width: var(--mc-ico) !important;
    min-width: var(--mc-ico) !important;
    max-width: var(--mc-ico) !important;
    height: var(--mc-ico) !important;
    min-height: var(--mc-ico) !important;
    max-height: var(--mc-ico) !important;
    margin: 0 !important;
    padding: 0 !important;
    z-index: 12 !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_notifications_clic [data-testid="stButton"] {
    display: block !important;
    width: var(--mc-ico) !important;
    min-width: var(--mc-ico) !important;
    height: var(--mc-ico) !important;
    margin: 0 !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_notifications_clic button {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: var(--mc-ico) !important;
    min-width: var(--mc-ico) !important;
    max-width: var(--mc-ico) !important;
    height: var(--mc-ico) !important;
    min-height: var(--mc-ico) !important;
    max-height: var(--mc-ico) !important;
    padding: 0 !important;
    border: none !important;
    border-radius: 50% !important;
    background: transparent !important;
    box-shadow: none !important;
    color: #12315f !important;
    cursor: pointer !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_notifications_clic button:hover {
    background-color: #eaf1fc !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_notifications_clic button:focus-visible {
    outline: 2px solid #2563eb !important;
    outline-offset: 2px !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_notifications_clic button p {
    position: absolute !important;
    width: 1px !important;
    height: 1px !important;
    margin: 0 !important;
    overflow: hidden !important;
    clip-path: inset(50%) !important;
}
/* Le pictogramme est peint directement sur le fond du bouton,
   comme l'avatar. Aucun pseudo-element n'est necessaire. */
.st-key-mathicap_zone_profil .st-key-mathicap_notifications_clic button {
    background-position: center center !important;
    background-repeat: no-repeat !important;
    background-size: calc(var(--mc-ico) * .72) calc(var(--mc-ico) * .72) !important;
}

.st-key-mathicap_zone_profil .mathicap-avatar {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex: none;
    width: var(--mc-avatar);
    height: var(--mc-avatar);
    border-radius: 50%;
    overflow: hidden;
    background: #dbeafe;
    color: #2563eb;
}

.st-key-mathicap_zone_profil .mathicap-avatar img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center center;
}

.st-key-mathicap_zone_profil .mathicap-avatar svg {
    width: 62%;
    height: 62%;
}

/* Statut de connexion */
.st-key-mathicap_zone_profil .mathicap-connecte {
    color: #18864b !important;
    font-size: var(--mc-statut) !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
    white-space: nowrap !important;
    text-align: right !important;
    margin: 0 !important;
}

.st-key-mathicap_zone_profil .mathicap-connecte.mathicap-deconnecte {
    color: #6b7280 !important;
}

/* Bouton Déconnexion : largeur = texte, compact */
.st-key-mathicap_zone_profil [data-testid="stButton"] {
    display: flex !important;
    justify-content: flex-end !important;
    width: 100% !important;
}

.st-key-mathicap_zone_profil [data-testid="stButton"] button {
    width: auto !important;
    min-width: 0 !important;
    max-width: 100% !important;
    height: var(--mc-btn-h) !important;
    min-height: var(--mc-btn-h) !important;
    padding: 0 12px !important;
    font-size: var(--mc-btn-fs) !important;
    line-height: 1 !important;
    white-space: nowrap !important;
    box-sizing: border-box !important;
}

.st-key-mathicap_zone_profil [data-testid="stButton"] button p {
    font-size: inherit !important;
    line-height: 1 !important;
    margin: 0 !important;
}

/* Tablette : 768 à 1024 px */
@media (max-width: 1024px) {
    [data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic) {
        --mc-brand-w: 210px;
        --mc-ico: 38px;
        --mc-avatar: 48px;
        --mc-ico-gap: 14px;
    }
}

/* Smartphone : moins de 768 px */
@media (max-width: 767px) {
    [data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic) {
        --mc-brand-w: clamp(112px, 36vw, 170px);
        --mc-ico: 32px;
        --mc-avatar: 52px;
        --mc-ico-gap: 8px;
        --mc-statut: 12px;
        --mc-btn-h: 28px;
        --mc-btn-fs: 11px;
        column-gap: 8px !important;
    }
}

/* Très petit écran : 360 px et moins (dont 320 px) */
@media (max-width: 360px) {
    [data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic) {
        --mc-brand-w: 112px;
        --mc-ico: 28px;
        --mc-avatar: 44px;
        --mc-ico-gap: 6px;
        --mc-statut: 11px;
        --mc-btn-h: 26px;
        --mc-btn-fs: 10.5px;
    }
}
/* Déconnexion compacte sur smartphone uniquement : ne pas toucher aux icônes. */
@media (max-width: 767px) {
    .st-key-mathicap_zone_profil .st-key-mathicap_deconnexion_entete [data-testid="stButton"] {
        width: fit-content !important;
        margin-left: auto !important;
    }
    .st-key-mathicap_zone_profil .st-key-mathicap_deconnexion_entete button {
        width: auto !important;
        min-width: 0 !important;
        height: 24px !important;
        min-height: 24px !important;
        padding: 1px 4px !important;
    }
    .st-key-mathicap_zone_profil .st-key-mathicap_deconnexion_entete button p {
        font-size: 10px !important;
    }
}
/* Logo au plus haut sous la barre Streamlit, PC et smartphone.
   Même règle en plein écran, demi-écran et orientation paysage. */
[data-testid="stMainBlockContainer"]:has(.st-key-mathicap_logo_clic) {
    padding-top: 2rem !important;
}
/* Zone cliquable exactement aux dimensions de l'avatar */
.st-key-mathicap_zone_profil
.st-key-mathicap_avatar_clic [data-testid="stButton"] button {
    width: var(--mc-avatar) !important;
    min-width: var(--mc-avatar) !important;
    max-width: var(--mc-avatar) !important;
    height: var(--mc-avatar) !important;
    min-height: var(--mc-avatar) !important;
    max-height: var(--mc-avatar) !important;
    padding: 0 !important;
    border-radius: 50% !important;
}
/* Avatar parfaitement circulaire sur smartphone */
@media (max-width: 767px) {
    .st-key-mathicap_zone_profil
    .st-key-mathicap_avatar_clic
    [data-testid="stButton"] button {
        width: var(--mc-avatar) !important;
        min-width: var(--mc-avatar) !important;
        max-width: var(--mc-avatar) !important;
        height: var(--mc-avatar) !important;
        min-height: var(--mc-avatar) !important;
        max-height: var(--mc-avatar) !important;
        aspect-ratio: 1 / 1 !important;
        border-radius: 50% !important;
        box-sizing: border-box !important;
        background-size: cover !important;
    }
}
/* PC et smartphone paysage : rapprocher les icônes */
@media (min-width: 768px), (orientation: landscape) {

    /* Les icônes gardent leur taille de bouton à toute orientation. */
}
/* Séries enregistrées : alignement sur smartphone */
@media (max-width: 767px) {

    [data-testid="stHorizontalBlock"]:has(
        [class*="st-key-reprendre_serie_"]
    ) {
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 10px !important;
    }

    [data-testid="stHorizontalBlock"]:has(
        [class*="st-key-reprendre_serie_"]
    ) > [data-testid="stColumn"]:first-child {
        flex: 0 0 120px !important;
        width: auto !important;
        min-width: 0 !important;
    }

    [data-testid="stHorizontalBlock"]:has(
        [class*="st-key-reprendre_serie_"]
    ) > [data-testid="stColumn"]:last-child {
        flex: 0 0 auto !important;
        width: auto !important;
        min-width: 0 !important;
    }
}

/* Recherche MathiCap intégrée à la page (aucune fenêtre flottante).
   Au repos : loupe seule. Champ dévoilé par clic ; disparition sur clic extérieur.
   Sur smartphone : saisie sous la loupe et dans le flux normal de la page. */
.st-key-mathicap_barre_recherche {
    --mc-recherche-h: 40px;
    --mc-recherche-bouton-w: 40px;
    width: min(320px, 100%) !important;
    max-width: 100% !important;
    min-width: 0 !important;
    margin: 9px 0 0 !important;
    padding: 0 !important;
}
.st-key-mathicap_barre_recherche [data-testid="stForm"] {
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}
.st-key-mathicap_barre_recherche [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}
.st-key-mathicap_barre_recherche [data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    justify-content: flex-end !important;
    gap: 0 !important;
    width: 100% !important;
    min-width: 0 !important;
}
.st-key-mathicap_barre_recherche [data-testid="stHorizontalBlock"]
> [data-testid="stColumn"]:first-child {
    flex: 1 1 auto !important;
    min-width: 0 !important;
    width: auto !important;
}
/* La saisie existe dans Streamlit mais ne prend aucune place tant que
   l'utilisateur n'a pas cliqué sur la loupe. */
.st-key-mathicap_barre_recherche:not(.mc-recherche-ouverte) [data-testid="stHorizontalBlock"]
> [data-testid="stColumn"]:first-child {
    display: none !important;
}
.st-key-mathicap_barre_recherche [data-testid="stHorizontalBlock"]
> [data-testid="stColumn"]:last-child {
    flex: 0 0 var(--mc-recherche-bouton-w) !important;
    width: var(--mc-recherche-bouton-w) !important;
    min-width: var(--mc-recherche-bouton-w) !important;
    max-width: var(--mc-recherche-bouton-w) !important;
}
.st-key-mathicap_barre_recherche [data-baseweb="input"] {
    height: var(--mc-recherche-h) !important;
    min-height: var(--mc-recherche-h) !important;
    border: 0 !important;
    border-bottom: 1px solid #94a3b8 !important;
    border-radius: 0 !important;
    padding: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}
.st-key-mathicap_barre_recherche [data-baseweb="input"]:focus-within {
    border-bottom: 2px solid #2563eb !important;
}
.st-key-mathicap_barre_recherche input {
    min-width: 0 !important;
    width: 100% !important;
    height: var(--mc-recherche-h) !important;
    padding: 0 6px !important;
    font-size: 14px !important;
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
}
/* La loupe est le véritable bouton de validation Streamlit :
   le premier clic l'ouvre sans envoyer de formulaire ;
   une fois ouvert, elle permet aussi de lancer la recherche. */
.st-key-mathicap_barre_recherche [data-testid="stFormSubmitButton"] button {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: var(--mc-recherche-bouton-w) !important;
    min-width: var(--mc-recherche-bouton-w) !important;
    max-width: var(--mc-recherche-bouton-w) !important;
    height: var(--mc-recherche-h) !important;
    min-height: var(--mc-recherche-h) !important;
    max-height: var(--mc-recherche-h) !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    border-radius: 50% !important;
    background: transparent !important;
    box-shadow: none !important;
    color: #12315f !important;
    text-decoration: none !important;
    cursor: pointer !important;
}
.st-key-mathicap_barre_recherche [data-testid="stFormSubmitButton"] button:hover {
    background: rgba(31,122,224,.08) !important;
    text-decoration: none !important;
}
.st-key-mathicap_barre_recherche [data-testid="stFormSubmitButton"] button:focus-visible {
    outline: 2px solid #2563eb !important;
    outline-offset: 2px !important;
}
.st-key-mathicap_barre_recherche [data-testid="stFormSubmitButton"] button p {
    font-size: 23px !important;
    line-height: 1 !important;
    text-decoration: none !important;
    margin: 0 !important;
}
@media (max-width: 620px) {
    [data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic) {
        grid-template-columns: minmax(0, 1fr) auto !important;
        row-gap: 8px !important;
    }
    [data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic)
    > [data-testid="stColumn"]:first-child {
        grid-column: 1 !important;
        grid-row: 1 !important;
    }
    [data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic)
    > [data-testid="stColumn"]:nth-child(2) {
        grid-column: 1 / -1 !important;
        grid-row: 2 !important;
        justify-self: start !important;
        align-self: start !important;
        width: min(230px, 100%) !important;
        max-width: 230px !important;
        margin-top: 0 !important;
    }
    [data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic)
    > [data-testid="stColumn"]:nth-child(3) {
        grid-column: 2 !important;
        grid-row: 1 !important;
    }
    .st-key-mathicap_barre_recherche {
        --mc-recherche-h: 36px;
        --mc-recherche-bouton-w: 36px;
        width: min(230px, 100%) !important;
        max-width: 100% !important;
        margin: 0 !important;
    }
    /* La loupe reste à gauche, et le champ ouvert descend en dessous. */
    .st-key-mathicap_barre_recherche [data-testid="stHorizontalBlock"] {
        flex-direction: column-reverse !important;
        align-items: flex-start !important;
        justify-content: flex-start !important;
    }
    .st-key-mathicap_barre_recherche [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:last-child {
        flex: 0 0 36px !important;
    }
    .st-key-mathicap_barre_recherche [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:first-child {
        flex: 1 1 auto !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    .st-key-mathicap_barre_recherche input {
        font-size: 13px !important;
    }
}
/* Position du profil : réglable indépendamment selon la largeur.
   Sur mobile, -30px remplace l'ancien -50px demandé. */
@media (max-width: 767px) {
    .st-key-mathicap_zone_profil {
        transform: translateY(-30px) !important;
    }
}
/* En demi-écran PC, conserver la position du profil validee. */
@media (min-width: 768px) and (max-width: 1100px) {
    .st-key-mathicap_zone_profil {
        transform: translateY(-30px) !important;
    }
}
/* Profil : lisibilite du score de correction sur smartphone uniquement */
@media (max-width: 767px) {
    .st-key-mathicap_score_corrections [data-testid="stMetricValue"],
    .st-key-mathicap_score_corrections [data-testid="stMetricValue"] > div {
        font-size: clamp(1rem, 4.6vw, 1.3rem) !important;
        line-height: 1.35 !important;
        white-space: normal !important;
        overflow-wrap: break-word !important;
        max-width: 100% !important;
    }
}

/* Galerie d'avatars : boutons circulaires de la taille de l'avatar,
   uniquement dans la fenêtre de sélection (PC et smartphone). */
[class*="st-key-mathicap_avatar_galerie_"] button {
    width: 48px !important;
    min-width: 48px !important;
    max-width: 48px !important;
    height: 48px !important;
    min-height: 48px !important;
    padding: 0 !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
}
[class*="st-key-mathicap_avatar_galerie_"] button p {
    font-size: 27px !important;
    line-height: 1 !important;
    margin: 0 !important;
}

/* Mots de passe : panneaux compacts sur PC et adaptatifs sur mobile.
   Ne change ni les champs de connexion ni les exercices. */
.st-key-mathicap_recup_etroit {
    width: min(100%, 460px) !important;
    max-width: 460px !important;
}
.st-key-mathicap_mdp_profil_etroit {
    width: min(100%, 420px) !important;
    max-width: 420px !important;
}
/* Le champ du code est visuellement court, sans tronquer les codes existants. */
.st-key-mathicap_recup_code {
    width: min(100%, 185px) !important;
    max-width: 185px !important;
}
@media (max-width: 620px) {
    .st-key-mathicap_recup_etroit,
    .st-key-mathicap_mdp_profil_etroit {
        width: 100% !important;
        max-width: 100% !important;
    }
}

/* ===== MathiCap : page exercices, disposition harmonisée ===== */
@media (min-width: 768px) {
    .st-key-mathicap_reglages_exercices { max-width: 880px !important; }
}
.st-key-mathicap_reglages_exercices [data-testid="stSelectbox"] {
    width: min(480px, 100%) !important;
    max-width: 100% !important;
}
.st-key-mathicap_reglages_exercices [data-testid="stProgress"] {
    max-width: 740px !important;
}
/* Exception au style global « boutons en texte » : action de génération. */
.st-key-mathicap_action_generer {
    width: min(100%, 480px) !important;
    margin: 6px 0 10px !important;
}
.st-key-mathicap_action_generer [data-testid="stButton"] button {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    min-height: 52px !important;
    padding: 12px 18px !important;
    border: 1px solid #1456b8 !important;
    border-radius: 12px !important;
    background: #1456b8 !important;
    color: #fff !important;
    box-shadow: 0 2px 6px rgba(20, 86, 184, .15) !important;
    font-size: 1.05rem !important;
    font-weight: 750 !important;
    text-align: center !important;
    text-decoration: none !important;
}
.st-key-mathicap_action_generer [data-testid="stButton"] button p {
    color: #fff !important;
    font-size: 1.05rem !important;
    font-weight: 750 !important;
    text-align: center !important;
    text-decoration: none !important;
    margin: 0 !important;
}
.st-key-mathicap_action_generer [data-testid="stButton"] button:hover {
    background: #0b3d91 !important;
    border-color: #0b3d91 !important;
    color: #fff !important;
    text-decoration: none !important;
}
.st-key-mathicap_action_generer [data-testid="stButton"] button:hover p {
    color: #fff !important;
    text-decoration: none !important;
}
.st-key-mathicap_action_generer [data-testid="stButton"] button:focus-visible {
    outline: 3px solid #82b6ff !important;
    outline-offset: 2px !important;
}
@media (max-width: 640px) {
    .st-key-mathicap_action_generer {
        width: 100% !important;
        max-width: 100% !important;
    }
    .st-key-mathicap_action_generer [data-testid="stButton"] button {
        min-height: 56px !important;
    }
}
/* Exercices : aucune hauteur fixe et aucun défilement propre aux questions.
   Garder la disposition native de Streamlit pour les rangées courtes. */
.st-key-mathicap_zone_exercices_affichage [data-testid="stHorizontalBlock"]:has([class*="st-key-banque_"]),
.st-key-mathicap_zone_exercices_affichage [data-testid="stHorizontalBlock"]:has([class*="st-key-reponse_"]) {
    max-width: min(100%, 640px) !important;
    width: 100% !important;
    align-items: flex-start !important;
    height: auto !important;
    min-height: 0 !important;
    overflow: visible !important;
    margin-bottom: 12px !important;
}
.st-key-mathicap_zone_exercices_affichage [data-testid="stHorizontalBlock"]:has([class*="st-key-banque_"]) > [data-testid="stColumn"],
.st-key-mathicap_zone_exercices_affichage [data-testid="stHorizontalBlock"]:has([class*="st-key-reponse_"]) > [data-testid="stColumn"] {
    min-width: 0 !important;
    height: auto !important;
    min-height: 0 !important;
    overflow: visible !important;
}
.st-key-mathicap_zone_exercices_affichage [data-testid="stHorizontalBlock"]:has([class*="st-key-banque_"]) > [data-testid="stColumn"] [data-testid="stVerticalBlock"],
.st-key-mathicap_zone_exercices_affichage [data-testid="stHorizontalBlock"]:has([class*="st-key-reponse_"]) > [data-testid="stColumn"] [data-testid="stVerticalBlock"] {
    height: auto !important;
    min-height: 0 !important;
    overflow: visible !important;
}
.st-key-mathicap_zone_exercices_affichage [data-testid="stMarkdownContainer"] p {
    white-space: normal !important;
    overflow-wrap: anywhere !important;
    height: auto !important;
    max-height: none !important;
    line-height: 1.45 !important;
}
/* Les énoncés gardent une largeur de lecture raisonnable sur grand écran. */
.st-key-mathicap_zone_exercices_affichage [class*="st-key-mathicap_enonce_"],
.st-key-mathicap_zone_exercices_affichage [class*="st-key-mathicap_question_"] {
    max-width: min(100%, 880px) !important;
    width: 100% !important;
    height: auto !important;
    overflow: visible !important;
}
/* Intitulés et réponses se suivent dans le flux normal de la page. */
.st-key-mathicap_zone_exercices_affichage [class*="st-key-mathicap_champ_reponse_"] {
    width: min(100%, 280px) !important;
    max-width: 100% !important;
    margin: 2px 0 12px !important;
}
.st-key-mathicap_zone_exercices_affichage [class*="st-key-mathicap_reponse_texte_"] {
    width: min(100%, 580px) !important;
    max-width: 100% !important;
    margin: 2px 0 12px !important;
}
.st-key-mathicap_zone_exercices_affichage [data-testid="stExpander"] {
    max-width: min(100%, 880px) !important;
}
.st-key-mathicap_zone_exercices_affichage [data-testid="stNumberInput"] input,
.st-key-mathicap_zone_exercices_affichage [data-testid="stTextInput"] input,
.st-key-mathicap_zone_exercices_affichage [data-testid="stSelectbox"] {
    width: 100% !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
}
/* Sur smartphone, conserver la visibilité des nombres saisis. */
@media (max-width: 620px) {
    .st-key-mathicap_zone_exercices_affichage [data-testid="stNumberInput"] button {
        display: none !important;
    }
    .st-key-mathicap_zone_exercices_affichage [data-testid="stNumberInput"] input,
    .st-key-mathicap_zone_exercices_affichage [data-testid="stTextInput"] input {
        padding-inline: 8px !important;
    }
}


/* MathiCap : titres déroulants cliquables, sans encadrement.
   La balise native details/summary garde le fonctionnement au clavier. */
[data-testid="stExpander"],
[data-testid="stExpander"] details {
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    background: transparent !important;
}
[data-testid="stExpander"] summary {
    padding: 6px 0 !important;
    border: 0 !important;
    border-radius: 0 !important;
    background: transparent !important;
    cursor: pointer !important;
}
[data-testid="stExpander"] summary:hover {
    text-decoration: underline !important;
    text-underline-offset: 3px !important;
}
[data-testid="stExpander"] summary:focus-visible {
    outline: 2px solid #2563eb !important;
    outline-offset: 3px !important;
}
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    border: 0 !important;
    padding: 8px 0 12px !important;
    background: transparent !important;
}
/* Navigation : uniquement du texte cliquable. Ne pas toucher aux boutons
   qui enregistrent, suppriment ou vérifient une réponse. */
:is(.st-key-mathicap_retour_accueil,
    .st-key-mathicap_notifications_retour,
    .st-key-mathicap_profil_mes_series,
    .st-key-mathicap_exercices_mes_series,
    .st-key-mathicap_retour_connexion_mdp) button {
    width: auto !important;
    min-width: 0 !important;
    min-height: 0 !important;
    height: auto !important;
    padding: 5px 0 !important;
    background: transparent !important;
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    color: #0b3d91 !important;
    font-weight: 600 !important;
    cursor: pointer !important;
}
:is(.st-key-mathicap_retour_accueil,
    .st-key-mathicap_notifications_retour,
    .st-key-mathicap_profil_mes_series,
    .st-key-mathicap_exercices_mes_series,
    .st-key-mathicap_retour_connexion_mdp) button:hover {
    text-decoration: underline !important;
    text-underline-offset: 3px !important;
    background: transparent !important;
}
:is(.st-key-mathicap_retour_accueil,
    .st-key-mathicap_notifications_retour,
    .st-key-mathicap_profil_mes_series,
    .st-key-mathicap_exercices_mes_series,
    .st-key-mathicap_retour_connexion_mdp) button:focus-visible {
    outline: 2px solid #2563eb !important;
    outline-offset: 3px !important;
}


/* MathiCap — fiches Mes séries, sans impact sur les autres pages. */
[class*="st-key-mathicap_series_carte_"] {
    max-width: 900px !important;
}
[class*="st-key-mathicap_series_actions_"] button {
    min-height: 40px !important;
    padding-inline: 14px !important;
}
@media (max-width: 640px) {
    [class*="st-key-mathicap_series_actions_"] button {
        min-height: 44px !important;
        padding-inline: 12px !important;
    }
}

/* MathiCap — liens de déplacement : cibles tactiles sur PC et smartphone.
   Ne s'applique ni au bouton de génération ni aux actions sur les réponses. */
:is(.st-key-mathicap_exercices_retour_accueil,
    .st-key-mathicap_exercices_mes_series,
    .st-key-mathicap_series_retour_exercices,
    .st-key-mathicap_series_retour_profil,
    .st-key-mathicap_series_retour_accueil) button {
    min-height: 40px !important;
    height: auto !important;
    padding: 7px 10px !important;
    border-radius: 8px !important;
    color: #0b3d91 !important;
    background: transparent !important;
    white-space: normal !important;
    text-decoration: none !important;
}
:is(.st-key-mathicap_exercices_retour_accueil,
    .st-key-mathicap_exercices_mes_series,
    .st-key-mathicap_series_retour_exercices,
    .st-key-mathicap_series_retour_profil,
    .st-key-mathicap_series_retour_accueil) button:hover {
    background: #edf4ff !important;
    text-decoration: underline !important;
}
@media (max-width: 640px) {
    :is(.st-key-mathicap_exercices_retour_accueil,
        .st-key-mathicap_exercices_mes_series,
        .st-key-mathicap_series_retour_exercices,
        .st-key-mathicap_series_retour_profil,
        .st-key-mathicap_series_retour_accueil) button {
        min-height: 44px !important;
        padding: 8px 6px !important;
        font-size: 0.88rem !important;
    }
}

/* =========================================================
   MATHICAP — PRÉSENTATION COMMUNE : TITRES ET ACTIONS SANS CADRE
   Les contrôles gardent leur sémantique native (clavier, état, clic).
   Les sélecteurs sont volontairement de faible spécificité pour
   préserver les commandes spéciales : classe, recherche, logo, avatar.
   ========================================================= */

/* Titres de sections déroulantes : aucun rectangle, flèche conservée. */
:where([data-testid="stExpander"], [data-testid="stExpander"] details) {
    border: 0 !important;
    border-radius: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}
:where([data-testid="stExpander"] summary) {
    border: none !important;
    border-radius: 0 !important;
    background: transparent !important;
    padding: 8px 0 !important;
    cursor: pointer !important;
}
:where([data-testid="stExpander"] summary:hover) {
    text-decoration: underline !important;
    text-underline-offset: 3px !important;
}
:where([data-testid="stExpander"] summary:focus-visible) {
    outline: 2px solid #2563eb !important;
    outline-offset: 3px !important;
}
:where([data-testid="stExpander"] [data-testid="stExpanderDetails"]) {
    border: 0 !important;
    background: transparent !important;
    padding: 8px 0 12px !important;
}

/* Boutons, actions de formulaires et déclencheurs de fenêtres contextuelles :
   du texte cliquable, sans rectangle. Les formulaires de saisie conservent
   les bordures nécessaires autour des champs e-mail, mot de passe, réponse. */
:where([data-testid="stButton"] button,
       [data-testid="stFormSubmitButton"] button,
       [data-testid="stPopover"] button,
       [data-testid="stPopoverButton"] button) {
    border: 0 !important;
    border-radius: 3px !important;
    box-shadow: none !important;
    background: transparent !important;
    color: #0b3d91 !important;
    font-weight: 600 !important;
    text-align: left !important;
    width: fit-content !important;
    max-width: 100% !important;
    min-width: 0 !important;
    min-height: 0 !important;
    height: auto !important;
    padding: 6px 3px !important;
    cursor: pointer !important;
    white-space: normal !important;
    overflow-wrap: anywhere !important;
}
:where([data-testid="stButton"] button:hover,
       [data-testid="stFormSubmitButton"] button:hover,
       [data-testid="stPopover"] button:hover,
       [data-testid="stPopoverButton"] button:hover) {
    border-color: transparent !important;
    background: transparent !important;
    text-decoration: underline !important;
    text-underline-offset: 3px !important;
}
:where([data-testid="stButton"] button:focus-visible,
       [data-testid="stFormSubmitButton"] button:focus-visible,
       [data-testid="stPopover"] button:focus-visible,
       [data-testid="stPopoverButton"] button:focus-visible) {
    outline: 2px solid #2563eb !important;
    outline-offset: 3px !important;
}
:where([data-testid="stButton"] button:disabled,
       [data-testid="stFormSubmitButton"] button:disabled) {
    opacity: 0.50 !important;
    cursor: not-allowed !important;
    text-decoration: none !important;
}

/* Suppression : rouge même sans fond ou bordure. */
.st-key-mathicap_supprimer_series_cochees button,
.st-key-confirmer_suppression_series button {
    color: #b42318 !important;
    font-weight: 750 !important;
}

/* Popovers : déclencheur sans cadre ; la fenêtre ouverte reste distincte. */
:where([data-testid="stPopover"] > button,
       [data-testid="stPopoverButton"] > button) {
    border: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}

/* Cadres de formulaires et de blocs décoratifs : pas de cadre externe.
   Les champs de saisie, les sélecteurs et les confirmations restent visibles. */
:where([data-testid="stForm"], [data-testid="stVerticalBlockBorderWrapper"]) {
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    background: transparent !important;
}

/* Tous les messages : texte et icône natifs, sans bandeau ni bordure.
   Les couleurs et symboles de succès, information, alerte et erreur
   restent ceux de Streamlit. */
:where([data-testid="stAlert"],
       [data-testid="stAlert"] [data-baseweb="notification"]) {
    width: min(100%, 500px) !important;
    max-width: min(100%, 500px) !important;
    border: 0 !important;
    border-radius: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}
:where([data-testid="stAlert"] [data-baseweb="notification"]) {
    padding: 7px 0 !important;
}

/* Exceptions de lisibilité : sélecteur de classe 6e/5e/4e/3e.
   Ce sont des choix de valeur, pas des titres à ouvrir :
   on conserve leur couleur et leur état visuel. */
.st-key-mathicap_ligne_classes button,
[class*="st-key-mathicap_bouton_"] button {
    width: 100% !important;
    min-height: 48px !important;
    text-align: center !important;
    justify-content: center !important;
}

/* Six cartes d'activité : restaurer une séparation visuelle.
   Exception volontaire au style général « texte sans cadre » :
   chaque carte entière reste cliquable (3 colonnes PC / 2 mobile). */
.st-key-mathicap_cartes button {
    width: 100% !important;
    min-height: 155px !important;
    height: 100% !important;
    padding: 16px !important;
    text-align: left !important;
    align-items: flex-start !important;
    justify-content: flex-start !important;
    color: #092c63 !important;
    border: 1px solid #d5e2f2 !important;
    border-radius: 14px !important;
    background: #ffffff !important;
    box-shadow: 0 2px 5px rgba(0, 0, 0, .04) !important;
    text-decoration: none !important;
    overflow-wrap: normal !important;
}
.st-key-mathicap_cartes button:hover {
    background: #eef6ff !important;
    border-color: #3182ed !important;
    box-shadow: 0 3px 9px rgba(9, 44, 99, .09) !important;
    text-decoration: none !important;
}
.st-key-mathicap_cartes button p,
.st-key-mathicap_cartes button:hover p {
    text-decoration: none !important;
}
.st-key-mathicap_cartes button:focus-visible {
    outline: 3px solid #3182ed !important;
    outline-offset: 2px !important;
}
@media (max-width: 640px) {
    .st-key-mathicap_cartes button {
        min-height: 165px !important;
        padding: 12px !important;
    }
}


/* QCM — exceptions explicites aux boutons sans cadre de MathiCap.
   Uniquement les clés du questionnaire : ne change ni l'en-tête ni les exercices. */
[class*="st-key-mc_qcm_demarrer"] button {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    min-height: 54px !important;
    height: auto !important;
    padding: 12px 18px !important;
    border: 2px solid #3b78d2 !important;
    border-radius: 14px !important;
    background: #dcecff !important;
    background-color: #dcecff !important;
    color: #153a70 !important;
    font-size: 1.16rem !important;
    font-weight: 800 !important;
    text-align: center !important;
    text-decoration: none !important;
    box-shadow: 0 3px 9px rgba(26, 78, 154, .12) !important;
}
[class*="st-key-mc_qcm_demarrer"] button p {
    font-size: 1.16rem !important;
    font-weight: 800 !important;
    color: #153a70 !important;
    text-align: center !important;
    text-decoration: none !important;
}
[class*="st-key-mc_qcm_demarrer"] button:hover {
    background: #c8e0ff !important;
    border-color: #245daa !important;
    text-decoration: none !important;
}
[class*="st-key-mc_qcm_reprise_zone"] [data-testid="stExpander"] summary {
    min-height: 48px !important;
    padding: 10px 15px !important;
    border: 1px solid #b0ccef !important;
    border-radius: 12px !important;
    background: #eff6ff !important;
    text-decoration: none !important;
}
[class*="st-key-mc_qcm_reprise_zone"] [data-testid="stExpander"] summary p {
    font-size: 1.04rem !important;
    font-weight: 750 !important;
    color: #153a70 !important;
}
[class*="st-key-mc_qcm_reprise_zone"] button {
    min-height: 43px !important;
    padding: 10px 13px !important;
    border: 1px solid #c4d8f4 !important;
    border-radius: 10px !important;
    background: #f7fbff !important;
    color: #154680 !important;
    text-align: left !important;
    text-decoration: none !important;
}
[class*="st-key-mc_qcm_reprise_zone"] button p {
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: #154680 !important;
    text-decoration: none !important;
}
@media (max-width: 640px) {
    [class*="st-key-mc_qcm_demarrer"] button,
    [class*="st-key-mc_qcm_demarrer"] button p {
        font-size: 1.04rem !important;
    }
}

/* MathiCap : logo cliquable sans soulignement, même au survol. */
.st-key-mathicap_logo_clic button,
.st-key-mathicap_logo_clic button:hover,
.st-key-mathicap_logo_clic button:focus,
.st-key-mathicap_logo_clic button::before,
.st-key-mathicap_logo_clic button::after,
.st-key-mathicap_logo_clic button:hover::after,
.st-key-mathicap_logo_clic button * {
    text-decoration: none !important;
    text-decoration-line: none !important;
}

/* Notifications Streamlit : supprimer le fond, le contour et les marges
   internes des boîtes tout en conservant la couleur et l'icône natives. */
[data-testid="stAlert"],
[data-testid="stAlert"] > div,
[data-testid="stAlert"] [data-baseweb="notification"],
[data-testid="stAlert"] [data-baseweb="notification"] > div {
    background: transparent !important;
    background-color: transparent !important;
    background-image: none !important;
    border: 0 !important;
    border-left: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}
[data-testid="stAlert"] {
    width: min(100%, 500px) !important;
    max-width: 500px !important;
    padding: 0 !important;
}
[data-testid="stAlert"] [data-baseweb="notification"] {
    padding: 5px 0 !important;
}


/* ==============================================================
   MathiCap – correctif smartphone : loupe dans l'en-tête.
   Seule la présentation change ; formulaire, validation et fermeture
   au clic extérieur restent inchangés.
   ============================================================== */
@media (max-width: 620px) {
    /* Logo | loupe | cloche et avatar : une ligne unique. */
    [data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic) {
        display: grid !important;
        grid-template-columns: minmax(0, 1fr) 36px auto !important;
        grid-template-rows: auto !important;
        gap: 8px !important;
        align-items: start !important;
        position: relative !important;
        overflow: visible !important;
    }
    [data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic)
    > [data-testid="stColumn"]:first-child {
        grid-row: 1 !important;
        grid-column: 1 !important;
        min-width: 0 !important;
    }
    [data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic)
    > [data-testid="stColumn"]:nth-child(2) {
        grid-row: 1 !important;
        grid-column: 2 !important;
        align-self: start !important;
        justify-self: center !important;
        width: 36px !important;
        min-width: 36px !important;
        max-width: 36px !important;
        margin: 0 !important;
        position: static !important;
        overflow: visible !important;
    }
    [data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic)
    > [data-testid="stColumn"]:nth-child(3) {
        grid-row: 1 !important;
        grid-column: 3 !important;
        justify-self: end !important;
    }
    .st-key-mathicap_barre_recherche {
        --mc-recherche-h: 36px;
        --mc-recherche-bouton-w: 36px;
        width: 36px !important;
        max-width: 36px !important;
        margin: 18px 0 0 !important;
        padding: 0 !important;
        position: static !important;
        overflow: visible !important;
    }
    /* Les conteneurs ne doivent pas retenir le champ sous la loupe. */
    .st-key-mathicap_barre_recherche form,
    .st-key-mathicap_barre_recherche [data-testid="stForm"],
    .st-key-mathicap_barre_recherche [data-testid="stVerticalBlock"],
    .st-key-mathicap_barre_recherche [data-testid="stHorizontalBlock"],
    .st-key-mathicap_barre_recherche [data-testid="stElementContainer"] {
        position: static !important;
        overflow: visible !important;
    }
    .st-key-mathicap_barre_recherche [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: flex-start !important;
        justify-content: flex-end !important;
        width: 36px !important;
        min-width: 36px !important;
        max-width: 36px !important;
        gap: 0 !important;
    }
    .st-key-mathicap_barre_recherche [data-testid="stHorizontalBlock"]
    > [data-testid="stColumn"]:last-child {
        flex: 0 0 36px !important;
        width: 36px !important;
        min-width: 36px !important;
        max-width: 36px !important;
    }
    /* Champ dévoilé sous le bloc logo/profil, dans le flux visuel de la page.
       Il ne recouvre ni le slogan ni les boutons du compte. */
    .st-key-mathicap_barre_recherche.mc-recherche-ouverte
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {
        display: block !important;
        position: absolute !important;
        top: calc(100% + 10px) !important;
        left: 0 !important;
        right: auto !important;
        width: min(230px, 100%) !important;
        min-width: 0 !important;
        max-width: 230px !important;
        height: auto !important;
        z-index: 5 !important;
    }
    /* Réserver la place pour le champ uniquement lorsqu'il est ouvert. */
    [data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic):has(.mc-recherche-ouverte) {
        margin-bottom: 50px !important;
    }
}


/* Mes séries : panneau de filtres coloré, isolé des autres formulaires. */
.st-key-mathicap_series_filtres {
    width: min(100%, 940px) !important;
    box-sizing: border-box !important;
    padding: 16px 18px 14px !important;
    margin: 12px 0 14px !important;
    background: linear-gradient(115deg, #edf5ff 0%, #f5f0ff 55%, #edf9f6 100%) !important;
    border: 1px solid #d2e2f6 !important;
    border-radius: 16px !important;
    box-shadow: 0 3px 12px rgba(29, 78, 137, 0.055) !important;
}
.st-key-mathicap_series_filtres .mc-series-filtres-titre {
    color: #173e79 !important;
    font-size: 1rem !important;
    font-weight: 750 !important;
    margin: 0 0 10px !important;
    line-height: 1.3 !important;
}
.st-key-mathicap_series_filtres [data-testid="stSelectbox"] label p {
    color: #264363 !important;
    font-size: .92rem !important;
    font-weight: 700 !important;
}
.st-key-mathicap_series_filtres [data-baseweb="select"] > div {
    background: #fff !important;
    min-height: 43px !important;
    border: 1px solid #cbdcf4 !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 3px rgba(35, 67, 110, .04) !important;
}
.st-key-mathicap_series_filtre_chapitre_couleur [data-baseweb="select"] > div {
    border-left: 4px solid #2b74d9 !important;
}
.st-key-mathicap_series_filtre_niveau_couleur [data-baseweb="select"] > div {
    border-left: 4px solid #8256c9 !important;
}
.st-key-mathicap_series_filtre_etat_couleur [data-baseweb="select"] > div {
    border-left: 4px solid #158567 !important;
}
.st-key-mathicap_series_filtres [data-baseweb="select"] > div:focus-within {
    outline: 2px solid rgba(59, 130, 246, .40) !important;
    outline-offset: 2px !important;
}
@media (max-width: 640px) {
    .st-key-mathicap_series_filtres {
        padding: 14px 12px 12px !important;
        border-radius: 13px !important;
    }
    .st-key-mathicap_series_filtres [data-baseweb="select"] > div {
        min-height: 46px !important;
    }
}
/* Mes séries : filtres pleine largeur avec pagination compacte dans le titre. */
.st-key-mathicap_series_filtres {
    width: min(100%, 940px) !important;
    max-width: 100% !important;
    min-width: 0 !important;
}
.st-key-mathicap_series_entete_filtres {
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    margin: 0 0 10px !important;
}
.st-key-mathicap_series_entete_filtres .mc-series-filtres-titre {
    margin: 0 !important;
    white-space: nowrap !important;
}
/* Le titre occupe l'espace disponible, le label et la petite liste
   restent ensemble à l'extrémité droite du panneau. */
.st-key-mathicap_series_entete_filtres
[data-testid="stElementContainer"]:has(.mc-series-filtres-titre) {
    flex: 1 1 auto !important;
    min-width: 0 !important;
    margin-right: auto !important;
}
.st-key-mathicap_series_entete_filtres .mc-series-taille-label {
    color: #264363 !important;
    font-size: .81rem !important;
    font-weight: 650 !important;
    white-space: nowrap !important;
}
.st-key-mathicap_series_entete_filtres [data-testid="stSelectbox"] {
    flex: 0 0 auto !important;
    width: 82px !important;
    min-width: 76px !important;
    max-width: 82px !important;
}
.st-key-mathicap_series_entete_filtres [data-baseweb="select"] > div {
    min-height: 36px !important;
    border-radius: 8px !important;
    padding-left: 2px !important;
    border: 1px solid #cbdcf4 !important;
}
/* Une barre sur la largeur des filtres et des fiches, navigation à droite. */
.st-key-mathicap_series_pagination_bas {
    box-sizing: border-box !important;
    width: min(100%, 940px) !important;
    max-width: 100% !important;
    min-width: 0 !important;
    padding: 9px 12px !important;
    margin: 14px 0 8px 0 !important;
    border-radius: 12px !important;
    border: 1px solid #dce7f7 !important;
    background: #f5f9ff !important;
}
.st-key-mathicap_series_pagination_bas [data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-wrap: wrap !important;
    align-items: center !important;
    justify-content: flex-end !important;
    gap: 8px !important;
}
.st-key-mathicap_series_pagination_bas [data-testid="stCaptionContainer"] p {
    margin: 0 !important;
    white-space: nowrap !important;
}
@media (max-width: 640px) {
    .st-key-mathicap_series_entete_filtres .mc-series-filtres-titre {
        font-size: .90rem !important;
    }
    .st-key-mathicap_series_entete_filtres .mc-series-taille-label {
        font-size: .74rem !important;
    }
    .st-key-mathicap_series_entete_filtres [data-testid="stSelectbox"] {
        width: 76px !important;
        min-width: 70px !important;
    }
    .st-key-mathicap_series_pagination_bas {
        padding: 7px 8px !important;
    }
    .st-key-mathicap_series_pagination_bas button {
        font-size: .85rem !important;
        padding-inline: 8px !important;
    }
}

/* Mes séries — adaptation réelle des fiches sur petit écran.
   Cible uniquement les fiches de la page Mes séries : pas l'en-tête,
   pas les exercices, pas les autres pages. */
@media (max-width: 640px) {
    [class*="st-key-mathicap_series_carte_"] {
        box-sizing: border-box !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
    }
    /* Case de sélection étroite + détail flexible, au lieu des colonnes
       Streamlit pouvant conserver une largeur minimale trop grande. */
    [class*="st-key-mathicap_series_carte_"]
    [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"] [data-testid="stCheckbox"]) {
        display: grid !important;
        grid-template-columns: 28px minmax(0, 1fr) !important;
        gap: 8px !important;
        align-items: start !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
    }
    [class*="st-key-mathicap_series_carte_"]
    [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"] [data-testid="stCheckbox"])
    > [data-testid="stColumn"] {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        flex: none !important;
    }
    [class*="st-key-mathicap_series_carte_"] [data-testid="stColumn"],
    [class*="st-key-mathicap_series_carte_"] [data-testid="stVerticalBlock"],
    [class*="st-key-mathicap_series_carte_"] [data-testid="stElementContainer"],
    [class*="st-key-mathicap_series_carte_"] [data-testid="stProgress"] {
        min-width: 0 !important;
        max-width: 100% !important;
    }
    /* Libellés longs : retour à la ligne sans agrandir la page. */
    [class*="st-key-mathicap_series_carte_"] [data-testid="stMarkdownContainer"],
    [class*="st-key-mathicap_series_carte_"] [data-testid="stMarkdownContainer"] p,
    [class*="st-key-mathicap_series_carte_"] [data-testid="stCaptionContainer"] p {
        white-space: normal !important;
        overflow-wrap: anywhere !important;
    }
    [class*="st-key-mathicap_series_carte_"] [data-testid="stProgress"] > div {
        box-sizing: border-box !important;
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
    }
    [class*="st-key-mathicap_series_actions_"] {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
    }
    [class*="st-key-mathicap_series_actions_"] [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        max-width: 100% !important;
        min-width: 0 !important;
    }
    .st-key-mathicap_series_filtres,
    .st-key-mathicap_series_pagination_bas {
        box-sizing: border-box !important;
        min-width: 0 !important;
        max-width: 100% !important;
    }
}

</style>
""", unsafe_allow_html=True)

# Interactions légères et isolées à la seule barre de recherche.
# Pas d'iframe/popover, pas de nouveau composant ni de modification Supabase.
# st.html autorise ce script statique sous Streamlit 1.66.0.
st.html(
    """<script>
    (() => {
      const rootSelector = '.st-key-mathicap_barre_recherche';
      const buttonSelector = '[data-testid="stFormSubmitButton"] button';
      const listenerKey = '__mathicap_recherche_inline_20261104';
      const getRoot = () => document.querySelector(rootSelector);
      // Après une recherche ou un changement de page, l'en-tête est replié.
      getRoot()?.classList.remove('mc-recherche-ouverte');
      if (window[listenerKey]) return;
      window[listenerKey] = true;

      document.addEventListener('click', (event) => {
        const root = getRoot();
        if (!root || !(event.target instanceof Element)) return;
        const button = event.target.closest(buttonSelector);
        if (button && root.contains(button)) {
          if (!root.classList.contains('mc-recherche-ouverte')) {
            // Ce premier clic sert à ouvrir le champ, pas à envoyer le formulaire.
            event.preventDefault();
            event.stopPropagation();
            event.stopImmediatePropagation();
            root.classList.add('mc-recherche-ouverte');
            requestAnimationFrame(() => root.querySelector('input')?.focus());
          }
          return;
        }
        if (!root.contains(event.target)) {
          root.classList.remove('mc-recherche-ouverte');
        }
      }, true);

      document.addEventListener('keydown', (event) => {
        if (event.key !== 'Escape') return;
        const root = getRoot();
        if (!root?.classList.contains('mc-recherche-ouverte')) return;
        root.classList.remove('mc-recherche-ouverte');
        if (root.contains(document.activeElement)) document.activeElement.blur();
      }, true);
    })();
    </script>""",
    unsafe_allow_javascript=True,
)

def _image_en_data_uri(nom_fichier: str) -> str:
    """Charge une image PNG du dépôt, si elle existe."""
    import base64

    chemin = Path(__file__).with_name(nom_fichier)
    if not chemin.is_file():
        return ""
    return "data:image/png;base64," + base64.b64encode(
        chemin.read_bytes()
    ).decode("ascii")
# Choix de la galerie enregistré dans Supabase Auth ; photos dans un bucket privé.
# Aucune photo volumineuse n'est insérée dans les métadonnées d'authentification.
BUCKET_AVATARS_MATHICAP = "mathicap-avatars"
AVATARS_MATHICAP = {
    "renard": ("🦊", "Renard", "#ffe5c2"),
    "panda": ("🐼", "Panda", "#e4edf5"),
    "chat": ("🐱", "Chat", "#ffe2e0"),
    "lapin": ("🐰", "Lapin", "#f0e3ff"),
    "grenouille": ("🐸", "Grenouille", "#dcf7d7"),
    "lion": ("🦁", "Lion", "#ffe9a8"),
    "pingouin": ("🐧", "Pingouin", "#dceeff"),
    "licorne": ("🦄", "Licorne", "#fce0f4"),
}


def _mathicap_chemin_avatar_valide(identifiant, chemin):
    """Empêcher la lecture des photos appartenant à un autre compte."""
    return bool(
        isinstance(identifiant, str)
        and isinstance(chemin, str)
        and re.fullmatch(r"[0-9a-fA-F-]{36}/[0-9a-f]{32}\.jpg", chemin)
        and chemin.startswith(identifiant + "/")
    )


def _mathicap_preparer_photo(fichier):
    """Photo carrée, miniature JPEG sans métadonnées EXIF (20 Ko maximum)."""
    brut = fichier.getvalue()
    if not brut or len(brut) > 3 * 1024 * 1024:
        raise ValueError("Choisis une image de 3 Mo maximum.")

    try:
        with Image.open(BytesIO(brut)) as image:
            if image.format not in {"JPEG", "PNG", "WEBP"}:
                raise ValueError("Format non reconnu : utilise JPG, PNG ou WEBP.")
            largeur, hauteur = image.size
            if largeur * hauteur > 20_000_000:
                raise ValueError("Image trop grande : utilise une photo plus petite.")
            image.load()
            image = ImageOps.exif_transpose(image)
            image = Image.alpha_composite(
                Image.new("RGBA", image.size, (255, 255, 255, 255)),
                image.convert("RGBA"),
            ).convert("RGB")
            for cote, qualite in ((160, 78), (144, 70), (128, 62), (112, 55)):
                carre = ImageOps.fit(
                    image, (cote, cote), method=Image.Resampling.LANCZOS,
                    centering=(0.5, 0.5)
                )
                sortie = BytesIO()
                carre.save(sortie, format="JPEG", quality=qualite, optimize=True)
                miniature = sortie.getvalue()
                if len(miniature) <= 20_000:
                    return miniature
    except (OSError, UnidentifiedImageError) as exc:
        raise ValueError("L'image ne peut pas être lue.") from exc

    raise ValueError("Image trop complexe : essaie une autre photo.")


def _mathicap_verifier_stockage_prive():
    """Créer le bucket à la première importation, jamais en mode public."""
    stockage = supabase_privee.storage
    try:
        bucket = stockage.get_bucket(BUCKET_AVATARS_MATHICAP)
    except Exception:
        try:
            stockage.create_bucket(
                BUCKET_AVATARS_MATHICAP,
                options={
                    "public": False,
                    "allowed_mime_types": ["image/jpeg"],
                    "file_size_limit": 200_000,
                },
            )
        except Exception:
            # En cas de création simultanée, vérifier s'il existe à présent.
            pass
        try:
            bucket = stockage.get_bucket(BUCKET_AVATARS_MATHICAP)
        except Exception as exc:
            raise ValueError(
                "Stockage des avatars indisponible dans Supabase."
            ) from exc

    est_public = (
        bucket.get("public", False)
        if isinstance(bucket, dict)
        else getattr(bucket, "public", False)
    )
    if est_public:
        raise ValueError(
            "Le bucket des avatars est public : passe-le en privé dans Supabase."
        )


@st.cache_data(ttl=300, show_spinner=False)
def _mathicap_lire_avatar_prive(identifiant, chemin):
    """Transmettre uniquement la petite photo du compte connecté."""
    if not _mathicap_chemin_avatar_valide(identifiant, chemin):
        return ""
    try:
        miniature = supabase_privee.storage.from_(BUCKET_AVATARS_MATHICAP).download(
            chemin
        )
        if not isinstance(miniature, bytes) or not (
            0 < len(miniature) <= 30_000 and miniature.startswith(b"\xff\xd8")
        ):
            return ""
        return "data:image/jpeg;base64," + base64.b64encode(
            miniature
        ).decode("ascii")
    except Exception:
        return ""


def _mathicap_enregistrer_avatar(identifiant, mode, choix="", chemin=""):
    """Conserver le pseudo et la classe et supprimer l'ancienne photo si besoin."""
    if mode not in ("defaut", "galerie", "photo"):
        raise ValueError("Type d'avatar non valide")
    if mode == "galerie" and choix not in AVATARS_MATHICAP:
        raise ValueError("Avatar non valide")
    if mode == "photo" and not _mathicap_chemin_avatar_valide(
        identifiant, chemin
    ):
        raise ValueError("Photo non valide")

    compte = supabase_privee.auth.admin.get_user_by_id(identifiant)
    if not compte.user:
        raise ValueError("Compte introuvable")
    infos = dict(compte.user.user_metadata or {})
    ancienne_photo = infos.get("mathicap_avatar_fichier", "")
    infos["mathicap_avatar_type"] = mode
    infos["mathicap_avatar_choix"] = choix if mode == "galerie" else ""
    infos["mathicap_avatar_fichier"] = chemin if mode == "photo" else ""
    supabase_privee.auth.admin.update_user_by_id(
        identifiant, {"user_metadata": infos}
    )
    st.session_state["mathicap_avatar_type"] = mode
    st.session_state["mathicap_avatar_choix"] = infos["mathicap_avatar_choix"]
    st.session_state["mathicap_avatar_fichier"] = infos["mathicap_avatar_fichier"]
    st.session_state["mathicap_avatar_sauve"] = True

    # L'échec d'un nettoyage ne doit pas annuler l'enregistrement réussi.
    if (
        ancienne_photo != infos["mathicap_avatar_fichier"]
        and _mathicap_chemin_avatar_valide(identifiant, ancienne_photo)
    ):
        try:
            supabase_privee.storage.from_(BUCKET_AVATARS_MATHICAP).remove(
                [ancienne_photo]
            )
        except Exception:
            pass


def _mathicap_importer_avatar(identifiant, photo_jpeg):
    """Sauver la photo privée, puis la référencer dans le compte élève."""
    _mathicap_verifier_stockage_prive()
    chemin = f"{identifiant}/{uuid4().hex}.jpg"
    stockage = supabase_privee.storage.from_(BUCKET_AVATARS_MATHICAP)
    stockage.upload(
        chemin,
        photo_jpeg,
        file_options={"content-type": "image/jpeg", "upsert": "false"},
    )
    try:
        _mathicap_enregistrer_avatar(identifiant, "photo", chemin=chemin)
    except Exception:
        try:
            stockage.remove([chemin])
        except Exception:
            pass
        raise


# Catalogue commun aux exercices et à la recherche, sans duplication.
CHAPITRES_MATHICAP = {
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

# Retour à l'accueil depuis toutes les pages, sans effacer la série en cours.
def _mathicap_retour_accueil_logo():
    st.session_state.pop("mathicap_recherche_active", None)
    st.session_state["mathicap_recherche_popover"] = False
    st.session_state["mathicap_page"] = "Accueil"
    st.session_state["afficher_series"] = False
    st.query_params["vue"] = "accueil"


def _mathicap_ouvrir_profil_rapide():
    """La navigation est préparée avant le rendu, sans double exécution."""
    st.session_state["mathicap_recherche_popover"] = False
    st.query_params["vue"] = "profil"


def _mathicap_profil_ouvrir_series():
    """Le bouton « Mes séries » du profil est une navigation, pas une sauvegarde."""
    st.session_state["mathicap_recherche_popover"] = False
    st.session_state["mathicap_page"] = "Mes séries"
    st.session_state["afficher_series"] = True
    st.query_params["vue"] = "series"


def _mathicap_reprendre_series_depuis_exercices():
    """Ouvrir la liste enregistrée sans perdre la série courante."""
    st.session_state["mathicap_recherche_popover"] = False
    st.session_state["mathicap_page"] = "Mes séries"
    st.session_state["afficher_series"] = True
    st.query_params["vue"] = "series"


def _mathicap_ouvrir_icone(vue):
    """Ouvre une rubrique sans effacer la série en cours ni la connexion."""
    st.session_state["mathicap_recherche_popover"] = False
    st.query_params["vue"] = vue


def _mathicap_ouvrir_chapitre_recherche(chapitre):
    """Depuis la recherche, ouvre le chapitre réellement disponible."""
    st.session_state["mathicap_recherche_popover"] = False
    st.session_state.pop("mathicap_recherche_active", None)
    st.session_state["_mathicap_chapitre_a_ouvrir"] = chapitre
    st.session_state["mathicap_page"] = "Exercices"
    st.session_state["afficher_series"] = False
    st.query_params["vue"] = "accueil"


def _mathicap_texte_recherche(texte):
    """Normalise une recherche sans distinguer les accents ou la casse."""
    import unicodedata
    return "".join(
        lettre for lettre in unicodedata.normalize("NFD", str(texte).casefold())
        if unicodedata.category(lettre) != "Mn"
    )


def _mathicap_valider_recherche_entete():
    """Recherche par Entrée ou loupe ; ferme la fenêtre après validation."""
    terme = st.session_state.get("mathicap_mot_cle_entete", "").strip()
    if terme:
        st.session_state["mathicap_recherche_active"] = terme
    # st.popover(on_change="rerun") peut être fermé depuis un callback.
    st.session_state["mathicap_recherche_popover"] = False


def _mathicap_fermer_recherche_entete():
    """Ferme les résultats et remet la recherche à zéro."""
    st.session_state.pop("mathicap_recherche_active", None)
    st.session_state["mathicap_recherche_popover"] = False
    st.session_state["mathicap_mot_cle_entete"] = ""


# Lorsqu'on navigue vers une autre page, le popover se referme également.
# Un clic en dehors est géré automatiquement par Streamlit lui-même.
_mathicap_recherche_page_courante = (
    str(st.query_params.get("vue", "accueil")),
    str(st.session_state.get("mathicap_page", "Accueil")),
)
if st.session_state.get("_mathicap_recherche_page_precedente") != _mathicap_recherche_page_courante:
    st.session_state["mathicap_recherche_popover"] = False
    st.session_state["_mathicap_recherche_page_precedente"] = _mathicap_recherche_page_courante
    st.session_state.pop("mathicap_recherche_active", None)


# En-tête unifié : logo à gauche, recherche centrale, compte à droite.
# La disposition est pilotée par CSS pour le PC et le smartphone.
col_logo, col_recherche, col_profil = st.columns(
    [3, 2, 1],
    vertical_alignment="top",
    gap="small",
    wrap=False,
)

with col_logo:
    import base64

    logo_principal = Path(__file__).with_name("mathicap_logo.png")

    logo_base64 = base64.b64encode(
        logo_principal.read_bytes()
    ).decode("ascii")

    # Dimensions natives : pas d'étirement du logo quel que soit l'écran.
    with Image.open(logo_principal) as image_logo:
        largeur_logo, hauteur_logo = image_logo.size

    # st.html avec uniquement du CSS ne crée pas de décalage vertical.
    # Le PNG est affiché comme image de fond du véritable bouton cliquable.
    st.html(
        f"""<style>
        .st-key-mathicap_logo_clic button::before {{
            aspect-ratio: {largeur_logo} / {hauteur_logo} !important;
            background-image: url('data:image/png;base64,{logo_base64}') !important;
        }}
        </style>"""
    )
    st.button(
        "MathiCap Collège — Retour à l'accueil",
        key="mathicap_logo_clic",
        on_click=_mathicap_retour_accueil_logo,
    )

with col_recherche:
    # Recherche dans le flux de la page : loupe seule au repos.
    # Au premier clic : le champ devient visible, à gauche sur PC
    # et en dessous sur smartphone. Un clic extérieur le replie.
    # Une fois ouvert, Entrée ou la loupe valident la recherche.
    with st.container(key="mathicap_barre_recherche"):
        with st.form(
            "mathicap_recherche_formulaire",
            border=False,
            clear_on_submit=False,
            enter_to_submit=True,
        ):
            col_saisie, col_loupe = st.columns(
                [8, 1], gap=None, vertical_alignment="center", wrap=False
            )
            with col_saisie:
                st.text_input(
                    "Mot-clé à rechercher",
                    placeholder="Chercher un chapitre…",
                    label_visibility="collapsed",
                    key="mathicap_mot_cle_entete",
                )
            with col_loupe:
                st.form_submit_button(
                    "🔍",
                    key="mathicap_recherche_valider",
                    on_click=_mathicap_valider_recherche_entete,
                    help="Ouvrir la recherche / lancer la recherche",
                    use_container_width=True,
                )

with col_profil:
    with st.container(key="mathicap_zone_profil"):
        _avatar_mode = st.session_state.get("mathicap_avatar_type", "defaut")
        _avatar_choix = st.session_state.get("mathicap_avatar_choix", "")
        _fichier_avatar = st.session_state.get("mathicap_avatar_fichier", "")
        _avatar_initiale = _mathicap_initiale_pseudo(
            st.session_state.get("mathicap_avatar_pseudo", "")
        )
        if _avatar_mode == "photo":
            _avatar_uri = _mathicap_lire_avatar_prive(
                st.session_state.get("eleve_id", ""), _fichier_avatar
            ) or _image_en_data_uri("mathicap_avatar.png")
        elif _avatar_mode == "galerie" and _avatar_choix in AVATARS_MATHICAP:
            _avatar_uri = ""  # Galerie : avatar dessiné par CSS.
        elif _avatar_mode == "defaut" and _avatar_initiale:
            _avatar_uri = ""  # Sans avatar choisi : initiale du pseudo.
        else:
            _avatar_uri = _image_en_data_uri("mathicap_avatar.png")

        if _avatar_uri:
            _avatar_html = f'<img src="{_avatar_uri}" alt="">'
        else:
            _avatar_html = (
                '<svg viewBox="0 0 24 24" fill="currentColor" '
                'aria-hidden="true"><circle cx="12" cy="9" r="4"/>'
                '<path d="M4.5 21c0-4 3.4-6.5 7.5-6.5s7.5 2.5 7.5 6.5z"/>'
                '</svg>'
            )

        # SVG conservés : mêmes pictogrammes, mais boutons natifs cliquables.
        import base64
        _icone_svg_debut = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
            'fill="none" stroke="#12315f" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round">'
        )
        _svg_notifications = (
            _icone_svg_debut
            + '<path d="M6 16v-5a6 6 0 0 1 12 0v5l1.5 2h-15z"/>'
            + '<path d="M10 20.5a2 2 0 0 0 4 0"/></svg>'
        )
        _notifications_b64 = base64.b64encode(_svg_notifications.encode()).decode()
        # Image de fond directement sur le vrai bouton : meme approche
        # que le bouton-avatar, deja valide sur PC et smartphone.
        st.markdown(
            f"""<style>
            .st-key-mathicap_zone_profil
            .st-key-mathicap_notifications_clic button {{
                background-image: url("data:image/svg+xml;base64,{_notifications_b64}") !important;
            }}
            </style>""",
            unsafe_allow_html=True,
        )
        if _avatar_uri:
            st.markdown(
                f"""
                <style>
                .st-key-mathicap_zone_profil
                .st-key-mathicap_avatar_clic button {{
                    background-image: url("{_avatar_uri}") !important;
                    background-size: cover !important;
                    background-position: center !important;
                    background-repeat: no-repeat !important;
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )
        elif _avatar_mode == "galerie" and _avatar_choix in AVATARS_MATHICAP:
            _emoji, _, _couleur_fond = AVATARS_MATHICAP[_avatar_choix]
            # Emoji et couleur issus de la liste interne, non de texte libre.
            st.markdown(
                f"""
                <style>
                .st-key-mathicap_zone_profil
                .st-key-mathicap_avatar_clic button {{
                    background: {_couleur_fond} !important;
                    position: relative !important;
                }}
                .st-key-mathicap_zone_profil
                .st-key-mathicap_avatar_clic button::after {{
                    content: "{_emoji}";
                    position: absolute;
                    inset: 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: calc(var(--mc-avatar) * 0.59);
                    line-height: 1;
                    color: initial !important;
                    -webkit-text-fill-color: initial !important;
                    pointer-events: none;
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )
        elif _avatar_mode == "defaut" and _avatar_initiale:
            st.markdown(
                f"""
                <style>
                .st-key-mathicap_zone_profil
                .st-key-mathicap_avatar_clic button {{
                    background: #dceafe !important;
                    position: relative !important;
                }}
                .st-key-mathicap_zone_profil
                .st-key-mathicap_avatar_clic button::after {{
                    content: "{_avatar_initiale}";
                    position: absolute;
                    inset: 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: calc(var(--mc-avatar) * 0.54);
                    line-height: 1;
                    font-weight: 700;
                    color: #2056a5 !important;
                    -webkit-text-fill-color: #2056a5 !important;
                    pointer-events: none;
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )
        # Deux véritables boutons voisins, dans le flux du document.
        # Résout la disparition de la cloche sur les écrans étroits.
        with st.container(
            horizontal=True,
            wrap=False,
            horizontal_alignment="right",
            vertical_alignment="center",
            gap=None,
            key="mathicap_icones_actions",
        ):
            st.button(
                "Notifications",
                key="mathicap_notifications_clic",
                help="Accéder aux notifications",
                on_click=_mathicap_ouvrir_icone,
                args=("notifications",),
            )
            st.button(
                "Ouvrir mon profil",
                key="mathicap_avatar_clic",
                disabled=not est_connecte,
                on_click=_mathicap_ouvrir_profil_rapide,
            )
        if est_connecte:
            st.markdown(
                '<div class="mathicap-connecte">● Connecté</div>',
                unsafe_allow_html=True
            )
            if st.button("Déconnexion", key="mathicap_deconnexion_entete"):
                jeton = st.session_state.pop("jeton_persistant", None)
                if jeton:
                    try:
                        supprimer_session(supabase_privee, jeton)
                    except Exception:
                        pass

                # Le jeton doit aussi être retiré du navigateur ; sinon
                # le compte risquerait d'être restauré à la prochaine visite.
                effacer_jeton_navigateur()

                try:
                    supabase.auth.sign_out()
                except Exception:
                    pass

                for cle in (
                    "supabase_client",
                    "eleve_id",
                    "session_eleve",
                    "exercices_actuels",
                    "code_actuel",
                    "jeton_persistant",
                    "mathicap_avatar_type",
                    "mathicap_avatar_choix",
                    "mathicap_avatar_fichier",
                    "mathicap_avatar_pseudo",
                    "mathicap_avatar_sauve",
                ):
                    st.session_state.pop(cle, None)

                st.session_state["vider_champs_connexion"] = True
                st.rerun()
        else:
            st.markdown(
                '<div class="mathicap-connecte mathicap-deconnecte">'
                '● Déconnecté</div>',
                unsafe_allow_html=True,
            )

def _mathicap_reponse_renseignee(valeur):
    """Une réponse vide ou le choix par défaut ne compte pas."""
    if valeur is None:
        return False
    if isinstance(valeur, str):
        return valeur.strip() not in ("", "Choisir...")
    return isinstance(valeur, (int, float)) and not isinstance(valeur, bool)


def _mathicap_statistiques_progression(series):
    """Bilan fondé uniquement sur les exercices et réponses sauvegardés."""
    statistiques = {
        "exercices_total": 0,
        "exercices_avec_reponse": 0,
        "reponses_renseignees": 0,
        "bonnes_verifiees": 0,
        "questions_verifiees": 0,
        "par_chapitre": {},
        "par_niveau": {},
        "non_classes": 0,
    }

    for serie in series:
        exercices = serie.get("exercices") or []
        reponses = serie.get("reponses") or {}
        if not isinstance(exercices, list):
            continue
        if not isinstance(reponses, dict):
            reponses = {}

        for numero, exercice in enumerate(exercices, start=1):
            if not isinstance(exercice, dict):
                continue
            statistiques["exercices_total"] += 1
            reponse = reponses.get(str(numero))
            compte_reponses = 0

            if isinstance(reponse, dict) and reponse.get("type") == "banque":
                champs_saisis = reponse.get("champs") or {}
                if isinstance(champs_saisis, dict):
                    champs_attendus = exercice.get("champs_reponse") or []
                    if isinstance(champs_attendus, list) and champs_attendus:
                        identifiants = [
                            champ.get("id") for champ in champs_attendus
                            if isinstance(champ, dict) and champ.get("id")
                        ]
                    else:
                        identifiants = list(champs_saisis)
                    compte_reponses = sum(
                        1 for identifiant in identifiants
                        if _mathicap_reponse_renseignee(
                            champs_saisis.get(identifiant)
                        )
                    )

                bilan = reponse.get("bilan")
                if isinstance(bilan, dict):
                    bonnes = bilan.get("bonnes")
                    total = bilan.get("total")
                    if (
                        type(bonnes) is int and type(total) is int
                        and 0 <= bonnes <= total and total > 0
                    ):
                        statistiques["bonnes_verifiees"] += bonnes
                        statistiques["questions_verifiees"] += total

            elif isinstance(reponse, dict) and reponse.get("type") == "simple":
                compte_reponses = int(_mathicap_reponse_renseignee(reponse.get("valeur")))
                bilan_simple = reponse.get("bilan")
                if isinstance(bilan_simple, dict):
                    bonnes = bilan_simple.get("bonnes")
                    total = bilan_simple.get("total")
                    if type(bonnes) is int and type(total) is int and 0 <= bonnes <= total and total > 0:
                        statistiques["bonnes_verifiees"] += bonnes
                        statistiques["questions_verifiees"] += total
            elif _mathicap_reponse_renseignee(reponse):
                compte_reponses = 1

            statistiques["reponses_renseignees"] += compte_reponses
            a_repondu = compte_reponses > 0
            if a_repondu:
                statistiques["exercices_avec_reponse"] += 1

            chapitre = exercice.get("mathicap_chapitre")
            niveau = exercice.get("mathicap_niveau")
            chapitre_valide = isinstance(chapitre, str) and bool(chapitre.strip())
            niveau_valide = type(niveau) is int and 1 <= niveau <= 9

            if chapitre_valide:
                compteurs = statistiques["par_chapitre"].setdefault(
                    chapitre, {"total": 0, "avec_reponse": 0}
                )
                compteurs["total"] += 1
                compteurs["avec_reponse"] += int(a_repondu)

            if niveau_valide:
                compteurs = statistiques["par_niveau"].setdefault(
                    niveau, {"total": 0, "avec_reponse": 0}
                )
                compteurs["total"] += 1
                compteurs["avec_reponse"] += int(a_repondu)

            if not (chapitre_valide and niveau_valide):
                statistiques["non_classes"] += 1

    return statistiques


# Les résultats s'affichent sous l'en-tête, sans changer de page.
recherche_active = st.session_state.get("mathicap_recherche_active", "")
if recherche_active:
    terme = _mathicap_texte_recherche(recherche_active)
    trouves = [
        (nom, [n for n in notions if terme in _mathicap_texte_recherche(n)])
        for nom, notions in CHAPITRES_MATHICAP.items()
        if terme in _mathicap_texte_recherche(nom)
        or any(terme in _mathicap_texte_recherche(n) for n in notions)
    ]
    with st.container(border=True):
        st.markdown(f"**Résultats pour : {escape(recherche_active)}**")
        if trouves:
            st.caption(f"{len(trouves)} chapitre(s) trouvé(s).")
            for indice, (nom, notions) in enumerate(trouves):
                col_detail, col_ouvrir = st.columns(
                    [3, 1], vertical_alignment="center"
                )
                with col_detail:
                    st.markdown(f"**{nom}**")
                    if notions:
                        st.caption("Notions correspondantes : " + ", ".join(notions))
                with col_ouvrir:
                    st.button(
                        "Ouvrir", key=f"mathicap_recherche_resultat_{indice}",
                        on_click=_mathicap_ouvrir_chapitre_recherche, args=(nom,),
                    )
        else:
            st.info("Aucun chapitre ou notion ne correspond à ce mot-clé.", width=500)
        st.button(
            "Fermer les résultats",
            key="mathicap_fermer_recherche",
            on_click=_mathicap_fermer_recherche_entete,
        )

_mc_nav_entete_ms = round((time.perf_counter() - _mc_nav_debut) * 1000)

if est_connecte and st.query_params.get("vue") == "profil":

    st.html("""<style>
    .mc-profile-shell {max-width:1120px;width:100%;margin:4px 0 18px;min-width:0;color:#153060}
    .mc-profile-title {font-size:clamp(1.7rem,3.2vw,2.1rem);margin:6px 0 15px;color:#122958;font-weight:850}
    .mc-profile-hero {position:relative;isolation:isolate;overflow:hidden;
       background:linear-gradient(112deg,#dcecff 0%,#e5f9ff 58%,#fff0cd 100%);
       border:1px solid #b4d5fc;border-radius:23px;min-height:156px;
       padding:22px 28px;display:flex;gap:20px;align-items:center;
       box-shadow:0 7px 20px rgba(42,87,150,.07)}
    .mc-profile-hero::after {content:'π   +   x²   ÷';position:absolute;right:14px;top:10px;
       color:rgba(30,108,201,.18);font-weight:900;font-size:clamp(18px,2vw,32px);letter-spacing:9px;z-index:-1}
    .mc-profile-portrait {height:99px;width:99px;border-radius:50%;display:flex;flex-shrink:0;
       align-items:center;justify-content:center;background:#f0f7ff;color:#1454a6;
       border:5px solid #fff;box-shadow:0 2px 12px #1b4f9820;font-size:38px;font-weight:850}
    .mc-profile-greeting {font-weight:850;font-size:clamp(1.25rem,2.5vw,1.9rem);
       line-height:1.25;color:#103672;margin:0 0 8px}
    .mc-profile-class {display:inline-block;border-radius:99px;background:#1f63cf;color:white;
       font-size:.83rem;padding:5px 12px;font-weight:750}
    .mc-profile-gentle {margin-top:10px;color:#2d5d92;line-height:1.5;font-size:.91rem}
    .mc-profile-section-title {font-size:clamp(1.1rem,2.1vw,1.4rem);font-weight:800;
       margin:21px 0 10px;color:#183b73}
    .mc-profile-infos {display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:11px;max-width:1120px;width:100%}
    .mc-profile-info {border-radius:14px;border:1px solid #e0eaf8;background:#f5f9ff;
       padding:14px 16px;min-width:0}
    .mc-profile-info:nth-child(2){background:#f4f6ff}
    .mc-profile-info:nth-child(3){background:#f0fbf5}
    .mc-profile-info:nth-child(4){background:#fff8eb}
    .mc-profile-label {font-size:.77rem;font-weight:750;color:#436182;margin-bottom:5px}
    .mc-profile-value {font-size:1rem;font-weight:700;color:#17315d;overflow-wrap:anywhere}
    .mc-profile-stats {width:100%;max-width:1120px;display:grid;
       grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:9px 0}
    .mc-profile-stat {min-width:0;border-radius:17px;padding:16px 12px 14px;
       background:linear-gradient(145deg,#eaf5ff,#d4eaff);border:1px solid #bfddfd;
       transition:transform .16s ease,box-shadow .16s ease}
    .mc-profile-stat:nth-child(2){background:linear-gradient(145deg,#fff8e7,#ffe4b7);border-color:#f7ddaf}
    .mc-profile-stat:nth-child(3){background:linear-gradient(145deg,#eafff0,#c8efd6);border-color:#b7e5c5}
    .mc-profile-stat:nth-child(4){background:linear-gradient(145deg,#f8f0ff,#e6d6ff);border-color:#dfc9fb}
    .mc-profile-stat .mc-profile-emoji{font-size:1.35rem;display:block;margin-bottom:5px}
    .mc-profile-stat .mc-profile-number{font-size:clamp(1.2rem,2.4vw,1.85rem);
       font-weight:850;color:#173365;line-height:1.3;font-variant-numeric:tabular-nums}
    .mc-profile-stat .mc-profile-desc{font-size:.82rem;line-height:1.35;font-weight:750;
       color:#355677;margin-top:4px}
    .mc-profile-track{height:10px;border-radius:20px;background:#dfebfa;overflow:hidden;
       margin-top:12px;max-width:1120px}
    .mc-profile-track-fill{height:100%;background:linear-gradient(90deg,#3d9de8,#3860d5);
       border-radius:20px;min-width:0}
    .mc-profile-muted {font-size:.8rem;color:#627c99;margin-top:7px;line-height:1.5}
    .mc-profile-avatar-heading {font-size:1.3rem;color:#174379;margin:15px 0 10px;font-weight:800}
    /* MathiCap — Profil : titres interactifs colorés sans cadres. */
    [data-testid="stMainBlockContainer"]:has(.mc-profile-hero) [data-testid="stExpander"] summary,
    [data-testid="stMainBlockContainer"]:has(.mc-profile-hero) [data-testid="stExpander"] summary * {
       font-size:clamp(1rem,1.15vw,1.1rem)!important;
       font-weight:780!important;
       color:#2159a2!important;
       text-decoration:none!important;
    }
    [data-testid="stMainBlockContainer"]:has(.mc-profile-hero) [data-testid="stExpander"] summary {
       padding:11px 2px!important;
       transition:color .16s ease, transform .16s ease;
    }
    [data-testid="stMainBlockContainer"]:has(.mc-profile-hero) [data-testid="stExpander"] summary:hover,
    [data-testid="stMainBlockContainer"]:has(.mc-profile-hero) [data-testid="stExpander"] summary:hover * {
       color:#0d4089!important;text-decoration:none!important;
    }
    /* Ciblage individuel des trois commandes, sans changer leur fonction. */
    [data-testid="stMainBlockContainer"]:has(.mc-profile-hero) .st-key-mathicap_mdp_profil_ouvert summary,
    [data-testid="stMainBlockContainer"]:has(.mc-profile-hero) .st-key-mathicap_mdp_profil_ouvert summary * {
       color:#7144b2!important;
    }
    [data-testid="stMainBlockContainer"]:has(.mc-profile-hero) .st-key-mc_profile_progression summary,
    [data-testid="stMainBlockContainer"]:has(.mc-profile-hero) .st-key-mc_profile_progression summary * {
       color:#13815c!important;
    }
    [data-testid="stMainBlockContainer"]:has(.mc-profile-hero) .st-key-mc_profile_pseudo summary,
    [data-testid="stMainBlockContainer"]:has(.mc-profile-hero) .st-key-mc_profile_pseudo summary * {
       color:#1d68b4!important;
    }
    .mc-profile-qcm-heading {
       color:#264680;font-weight:850;
       font-size:clamp(1.15rem,2vw,1.5rem);
       background:linear-gradient(100deg,#e9f0ff 0%,#f5edff 66%,#e6f9f1 100%);
       border-left:4px solid #8061db;
       padding:12px 16px;border-radius:0 14px 14px 0;
       margin:20px 0 13px;max-width:650px;
    }
    @media(prefers-reduced-motion:reduce){
       [data-testid="stMainBlockContainer"]:has(.mc-profile-hero) [data-testid="stExpander"] summary {
           transition:none!important;
       }
    }
    [data-testid='stMainBlockContainer']:has(.mc-profile-hero) [data-testid='stExpander'] {
       max-width:min(100%,520px)!important}
    [data-testid='stMainBlockContainer']:has(.mc-profile-hero) [data-testid='stTextInput']{
       max-width:100%!important}
    @media(hover:hover){.mc-profile-stat:hover{transform:translateY(-2px);
       box-shadow:0 5px 16px rgba(26,83,158,.10)}}
    @media(max-width:850px){
       .mc-profile-stats {grid-template-columns:repeat(2,minmax(0,1fr))}
       .mc-profile-hero{min-height:140px;padding:17px 20px}
    }
    @media(max-width:520px){
       .mc-profile-infos {grid-template-columns:1fr;gap:8px}
       .mc-profile-stat {padding:13px 10px}
       .mc-profile-stats{gap:9px}
       .mc-profile-hero{padding:15px 13px;border-radius:18px;gap:12px;min-height:0}
       .mc-profile-portrait{width:62px;height:62px;font-size:27px;border-width:3px}
       .mc-profile-hero::after{font-size:17px;letter-spacing:3px;top:4px;right:4px}
       .mc-profile-greeting{font-size:1.25rem}
       .mc-profile-class{font-size:.76rem}
       .mc-profile-gentle{font-size:.78rem;margin-top:6px}
    }
    @media(max-width:320px){.mc-profile-stats{grid-template-columns:1fr 1fr}
       .mc-profile-stat .mc-profile-number{font-size:1.2rem}}
    @media(prefers-reduced-motion:reduce){.mc-profile-stat{transition:none!important}}
    </style>""")


    identifiant_eleve = st.session_state["eleve_id"]
    email_eleve = None
    pseudo_eleve = ""
    date_inscription = None
    profil_charge = False

    # Récupérer les informations du compte existant
    _mc_nav_profil_debut = time.perf_counter()
    try:
        resultat_profil = supabase_privee.auth.admin.get_user_by_id(
            identifiant_eleve
        )
        utilisateur_profil = resultat_profil.user

        if utilisateur_profil is None:
            raise ValueError("Compte introuvable")

        email_eleve = utilisateur_profil.email
        pseudo_eleve = (
            (utilisateur_profil.user_metadata or {}).get("pseudo") or ""
        )
        st.session_state["mathicap_avatar_pseudo"] = pseudo_eleve
        date_inscription = utilisateur_profil.created_at
        donnees_avatar = utilisateur_profil.user_metadata or {}
        st.session_state["mathicap_avatar_type"] = donnees_avatar.get(
            "mathicap_avatar_type", "defaut"
        )
        st.session_state["mathicap_avatar_choix"] = donnees_avatar.get(
            "mathicap_avatar_choix", ""
        )
        st.session_state["mathicap_avatar_fichier"] = donnees_avatar.get(
            "mathicap_avatar_fichier", ""
        )
        profil_charge = True

    except Exception:
        st.warning("Informations du compte momentanément indisponibles.")
    _mc_nav_profil_ms = round((time.perf_counter() - _mc_nav_profil_debut) * 1000)

    # Classe et date d'inscription
    classe_eleve = st.session_state.get("mathicap_classe")

    if date_inscription:
        date_affichee = date_inscription.strftime("%d/%m/%Y")
    else:
        date_affichee = "Information non disponible"

    # Profil lisible, cartes s'adaptant à la largeur réelle du navigateur.
    classe_etiquette = escape(classe_eleve or "Non définie")
    nom_affiche = escape(pseudo_eleve.strip() or "élève")
    st.html(
        '<div class="mc-profile-shell">'
        '<div class="mc-profile-title">Mon profil</div>'
        '<div class="mc-profile-hero">'
        '<div><div class="mc-profile-greeting">Bonjour, ' + nom_affiche + ' !</div>'
        f'<span class="mc-profile-class">Classe : {classe_etiquette}</span>'
        '<div class="mc-profile-gentle">Ton espace pour progresser à ton rythme.</div>'
        '</div></div>'
        '<div class="mc-profile-section-title">Mes informations</div>'
        '<div class="mc-profile-infos">'
        '<div class="mc-profile-info"><div class="mc-profile-label">Pseudo</div>'
        f'<div class="mc-profile-value">{nom_affiche}</div></div>'
        '<div class="mc-profile-info"><div class="mc-profile-label">Adresse e-mail</div>'
        f'<div class="mc-profile-value">{escape(email_eleve or "Information indisponible")}</div></div>'
        '<div class="mc-profile-info"><div class="mc-profile-label">Ma classe</div>'
        f'<div class="mc-profile-value">{classe_etiquette}</div></div>'
        '<div class="mc-profile-info"><div class="mc-profile-label">Inscription</div>'
        f'<div class="mc-profile-value">{escape(date_affichee)}</div></div>'
        '</div></div>'
    )

    # Personnalisation de l'avatar, propre au compte de chaque élève.
    st.html('<div class="mc-profile-avatar-heading">Mon avatar</div>')
    if st.session_state.pop("mathicap_avatar_sauve", False):
        st.toast("Avatar enregistré. Il sera retrouvé sur tes appareils.", icon="✅", duration=3)

    avatar_type = st.session_state.get("mathicap_avatar_type", "defaut")
    avatar_choix = st.session_state.get("mathicap_avatar_choix", "")
    avatar_fichier = st.session_state.get("mathicap_avatar_fichier", "")
    if avatar_type == "galerie" and avatar_choix in AVATARS_MATHICAP:
        emoji_apercu, nom_apercu, fond_apercu = AVATARS_MATHICAP[avatar_choix]
        st.html(
            f'<div role="img" aria-label="Avatar {escape(nom_apercu)}" '
            'style="width:104px;height:104px;border-radius:50%;'
            f'background:{fond_apercu};display:flex;align-items:center;'
            'justify-content:center;font-size:48px;">'
            f'{emoji_apercu}</div>'
        )
    else:
        if avatar_type == "photo":
            photo_apercu = _mathicap_lire_avatar_prive(
                identifiant_eleve, avatar_fichier
            )
        elif avatar_type == "defaut" and _mathicap_initiale_pseudo(pseudo_eleve):
            initiale = _mathicap_initiale_pseudo(pseudo_eleve)
            st.html(
                '<div role="img" aria-label="Initiale du pseudo" '
                'style="width:104px;height:104px;border-radius:50%;'
                'background:#dceafe;color:#2056a5;display:flex;'
                'align-items:center;justify-content:center;font-size:43px;'
                'font-weight:700;">'
                f'{escape(initiale)}</div>'
            )
            photo_apercu = ""
        else:
            photo_apercu = _image_en_data_uri("mathicap_avatar.png")
        if photo_apercu:
            st.html(
                '<img alt="Mon avatar actuel" '
                'style="width:104px;height:104px;border-radius:50%;'
                'object-fit:cover;object-position:center center;display:block;" '
                f'src="{photo_apercu}">'
            )

    st.caption(
        "Sans avatar choisi, la première lettre du pseudo s'affiche. "
        "Sans pseudo, l'avatar MathiCap apparaît."
    )

    if profil_charge:
        # Les options occupent une seule ligne ; la galerie est cachée tant
        # que l'élève ne clique pas pour l'ouvrir.
        with st.container(horizontal=True, horizontal_alignment="left", gap="small"):
            with st.popover("Galerie d’avatars"):
                st.caption("Sélectionne un avatar.")
                avatars_items = list(AVATARS_MATHICAP.items())
                for index in range(0, len(avatars_items), 4):
                    colonnes = st.columns(4, gap="small")
                    for colonne, (identifiant_avatar, (emoji, nom, _)) in zip(
                        colonnes, avatars_items[index:index + 4]
                    ):
                        with colonne:
                            if st.button(
                                emoji,
                                key=f"mathicap_avatar_galerie_{identifiant_avatar}",
                                help=f"Choisir {nom}",
                            ):
                                try:
                                    _mathicap_enregistrer_avatar(
                                        identifiant_eleve, "galerie", identifiant_avatar
                                    )
                                    st.rerun()
                                except Exception:
                                    st.error("Impossible d'enregistrer cet avatar.")

            with st.popover("Importer une photo"):
                fichier_avatar = st.file_uploader(
                    "Choisir une photo (JPG, PNG ou WEBP, 3 Mo maximum)",
                    type=["jpg", "jpeg", "png", "webp"],
                    accept_multiple_files=False,
                    key="mathicap_fichier_avatar",
                )
                st.caption(
                    "La photo est recadrée au centre du cercle "
                    "et enregistrée dans un espace privé."
                )
                if st.button(
                    "Utiliser cette photo",
                    disabled=fichier_avatar is None,
                    key="mathicap_avatar_valider_photo",
                ):
                    try:
                        photo_prete = _mathicap_preparer_photo(fichier_avatar)
                        _mathicap_importer_avatar(identifiant_eleve, photo_prete)
                        st.rerun()
                    except ValueError as erreur:
                        st.warning(str(erreur))
                    except Exception:
                        st.error("Impossible d'enregistrer cette photo.")

        if avatar_type != "defaut" and st.button(
            "Revenir à l'avatar par défaut",
            key="mathicap_avatar_defaut",
        ):
            try:
                _mathicap_enregistrer_avatar(identifiant_eleve, "defaut")
                st.rerun()
            except Exception:
                st.error("Impossible de rétablir l'avatar par défaut.")
    else:
        st.info("Connecte-toi à ton profil pour personnaliser l'avatar.", width=500)

    # Confirmation après enregistrement
    if st.session_state.pop("mathicap_pseudo_sauve", False):
        st.toast("Pseudo enregistré avec succès.", icon="✅", duration=3)

    # Modifier le pseudo sans toucher aux autres informations
    if profil_charge:
        with st.expander("Modifier mon pseudo", width=500, key="mc_profile_pseudo"):
            with st.form("mathicap_formulaire_pseudo", border=False):
                nouveau_pseudo = st.text_input(
                    "Nouveau pseudo",
                    value=pseudo_eleve,
                    max_chars=30,
                    width=420,
                    help="Facultatif. Laisse vide pour retirer ton pseudo."
                )

                enregistrer_pseudo = st.form_submit_button("Enregistrer")

            if enregistrer_pseudo:
                nouveau_pseudo = nouveau_pseudo.strip()

                if nouveau_pseudo == pseudo_eleve.strip():
                    st.info("Aucune modification à enregistrer.", width=500)

                else:
                    try:
                        compte_actuel = supabase_privee.auth.admin.get_user_by_id(
                            identifiant_eleve
                        )

                        if compte_actuel.user is None:
                            raise ValueError("Compte introuvable")

                        infos = dict(
                            compte_actuel.user.user_metadata or {}
                        )

                        infos["pseudo"] = nouveau_pseudo

                        supabase_privee.auth.admin.update_user_by_id(
                            identifiant_eleve,
                            {"user_metadata": infos}
                        )

                        st.session_state["mathicap_avatar_pseudo"] = nouveau_pseudo
                        st.session_state["mathicap_pseudo_sauve"] = True
                        st.rerun()

                    except Exception:
                        st.error("Impossible d'enregistrer le pseudo.")
                        
    if profil_charge:
        _mathicap_formulaire_changement_mdp(email_eleve, identifiant_eleve)

    # Statistiques existantes, affichées en cartes adaptées à chaque largeur.
    series_profil = None
    _mc_nav_stat_debut = time.perf_counter()

    try:
        resultat_series = (
            supabase_privee.table("series_exercices")
            # Les memes colonnes que la liste « Mes series » : un seul chargement.
            .select("id, code_reprise, exercices, reponses, progression, created_at")
            .eq("eleve_id", identifiant_eleve)
            .order("created_at", desc=True)
            .execute()
        )

        series_profil = resultat_series.data or []
        # Reutilisation courte pour le passage immediat Profil -> Mes series.
        # Le cache sera consomme UNE FOIS ; il n'est jamais partage entre eleves.
        st.session_state["_mathicap_nav_series_profil_v7"] = {
            "eleve_id": identifiant_eleve,
            "jeton": st.session_state.get("jeton_persistant"),
            "charge_le": time.monotonic(),
            "series": series_profil,
        }

        total_series = len(series_profil)
        series_avec_reponses = sum(
            1 for serie in series_profil
            if serie.get("reponses")
        )


    except Exception:
        st.info("Impossible de charger les statistiques pour le moment.", width=500)
    _mc_nav_stat_ms = round((time.perf_counter() - _mc_nav_stat_debut) * 1000)

    st.html('<div class="mc-profile-section-title">Mes statistiques et ma progression</div>')
    if series_profil is None:
        st.info("La progression est momentanément indisponible.", width=500)
    else:
        statistiques = _mathicap_statistiques_progression(series_profil)
        nb_total = statistiques['exercices_total']
        nb_renseignes = statistiques['exercices_avec_reponse']
        nb_bonnes = statistiques['bonnes_verifiees']
        nb_verifiees = statistiques['questions_verifiees']
        taux_repondu = int(round(100 * nb_renseignes / nb_total)) if nb_total else 0
        st.html(
            '<div class="mc-profile-stats">'
            '<div class="mc-profile-stat"><span class="mc-profile-emoji">📚</span>'
            f'<div class="mc-profile-number">{total_series}</div>'
            '<div class="mc-profile-desc">Séries enregistrées</div></div>'
            '<div class="mc-profile-stat"><span class="mc-profile-emoji">✏️</span>'
            f'<div class="mc-profile-number">{nb_renseignes} / {nb_total}</div>'
            '<div class="mc-profile-desc">Exercices avec réponse</div></div>'
            '<div class="mc-profile-stat"><span class="mc-profile-emoji">✅</span>'
            f'<div class="mc-profile-number">{nb_bonnes} / {nb_verifiees}</div>'
            '<div class="mc-profile-desc">Bonnes réponses vérifiées</div></div>'
            '<div class="mc-profile-stat"><span class="mc-profile-emoji">📝</span>'
            f'<div class="mc-profile-number">{statistiques["reponses_renseignees"]}</div>'
            '<div class="mc-profile-desc">Réponses renseignées</div></div>'
            '</div>'
            '<div class="mc-profile-track" role="progressbar"'
            f' aria-valuenow="{taux_repondu}" aria-valuemin="0" aria-valuemax="100"'
            ' aria-label="Proportion d’exercices avec au moins une réponse">'
            f'<div class="mc-profile-track-fill" style="width:{taux_repondu}%"></div></div>'
            f'<div class="mc-profile-muted">{taux_repondu} % des exercices enregistrés ont au moins une réponse. '
            'Cette barre ne mesure pas la réussite.</div>'
        )
        st.caption(f"Séries avec au moins une réponse : {series_avec_reponses} sur {total_series}.")

        st.caption(
            "Un exercice est compté dès qu'au moins une réponse est "
            "enregistrée. Cela ne signifie pas qu'il est terminé ou réussi."
        )

        if statistiques["questions_verifiees"]:
            st.caption(
                "Résultats calculés uniquement à partir des bilans "
                "de vérification sauvegardés ; les exercices sans bilan "
                "ne sont pas notés."
            )
        else:
            st.caption(
                "Aucun bilan de correction enregistré pour le moment. "
                "Aucune note n'est estimée."
            )

        with st.expander("Progression par chapitre et par niveau", width=500, key="mc_profile_progression"):
            par_chapitre = statistiques["par_chapitre"]
            par_niveau = statistiques["par_niveau"]
            if not par_chapitre and not par_niveau:
                st.info(
                    "Les anciennes séries ne contiennent pas de chapitre "
                    "ni de niveau enregistrés. Ce suivi apparaîtra "
                    "avec les nouvelles séries.",
                    width=500,
                )
            else:
                if par_chapitre:
                    st.markdown("**Par chapitre**")
                    for nom, compteurs in sorted(par_chapitre.items()):
                        total = compteurs["total"]
                        repondus = compteurs["avec_reponse"]
                        st.write(f"{nom} — {repondus}/{total} exercices avec réponse")
                        # Limiter la barre à la moitié de la largeur sur PC.
                        # Les colonnes deviennent verticales sur smartphone.
                        col_barre, _ = st.columns([1, 1], gap="small")
                        with col_barre:
                            st.progress(repondus / total)

                if par_niveau:
                    st.markdown("**Par niveau**")
                    for niveau, compteurs in sorted(par_niveau.items()):
                        total = compteurs["total"]
                        repondus = compteurs["avec_reponse"]
                        st.write(
                            f"Niveau {niveau} — "
                            f"{repondus}/{total} exercices avec réponse"
                        )
                        # Limiter la barre à la moitié de la largeur sur PC.
                        # Les colonnes deviennent verticales sur smartphone.
                        col_barre, _ = st.columns([1, 1], gap="small")
                        with col_barre:
                            st.progress(repondus / total)

            if statistiques["non_classes"]:
                st.caption(
                    f"{statistiques['non_classes']} exercice(s) "
                    "sans chapitre ou niveau enregistré(s) ne figurent "
                    "pas dans tous ces regroupements."
                )
            st.caption(
                "Ces barres mesurent la saisie de réponses, "
                "pas la maîtrise des notions."
            )

    # Résultats QCM, indépendants des statistiques des séries d'exercices.
    from mathicap_qcm_resultats import afficher_progression_qcm
    _mc_nav_qcm_debut = time.perf_counter()
    afficher_progression_qcm()
    _mc_nav_qcm_ms = round((time.perf_counter() - _mc_nav_qcm_debut) * 1000)

    if _mc_nav_mesure:
        st.caption(
            "Mesure navigation — préparation/en-tête : "
            f"{_mc_nav_entete_ms} ms (dont session : {_mc_nav_auth_ms} ms) ; "
            f"profil : {_mc_nav_profil_ms} ms ; "
            f"statistiques : {_mc_nav_stat_ms} ms ; "
            f"résultats QCM : {_mc_nav_qcm_ms} ms ; "
            f"total serveur : {round((time.perf_counter()-_mc_nav_debut)*1000)} ms."
        )

    st.button(
        "Voir mes séries enregistrées",
        key="mathicap_profil_mes_series",
        on_click=_mathicap_profil_ouvrir_series,
    )
    st.button(
        "Retour à l'accueil",
        key="mathicap_retour_accueil",
        on_click=_mathicap_retour_accueil_logo,
    )


# Avant connexion seulement : formulaire compact, sous l'en-tête.
if not est_connecte:
    # Effacer les données sensibles AVANT que Streamlit instancie les widgets.
    _mathicap_recup_succes = st.session_state.pop(
        "mathicap_recup_succes_email", None
    )
    if _mathicap_recup_succes:
        _mathicap_effacer_champs_mdp(_CHAMPS_MDP_RECUP)
        st.session_state["email_connexion"] = _mathicap_recup_succes
        st.session_state["mdp_connexion"] = ""
    elif st.session_state.pop("mathicap_recup_recommencer", False):
        _mathicap_effacer_champs_mdp(_CHAMPS_MDP_RECUP)
    zone_compte, _ = st.columns([7, 3])
    with zone_compte:
        st.markdown(
            '<div style="padding-top: 12px; font-weight: 600;">Mon compte élève</div>',
            unsafe_allow_html=True
        )
        with st.container(border=True):
            with st.form("formulaire_connexion"):
                col_email, col_mdp, col_action = st.columns(
                    [3, 3, 2], vertical_alignment="bottom"
                )
                with col_email:
                    email_connexion = st.text_input(
                        "Adresse e-mail",
                        placeholder="Adresse e-mail",
                        label_visibility="collapsed",
                        key="email_connexion",
                    )
                with col_mdp:
                    mdp_connexion = st.text_input(
                        "Mot de passe",
                        placeholder="Mot de passe",
                        type="password",
                        label_visibility="collapsed",
                        key="mdp_connexion",
                    )
                with col_action:
                    connexion = st.form_submit_button(
                        "Se connecter", use_container_width=True
                    )

            if _mathicap_recup_succes:
                st.success(
                    "Mot de passe réinitialisé. Tu peux te connecter avec "
                    "ton nouveau mot de passe.",
                    width=500,
                )

            if st.button("Mot de passe oublié ?", key="mathicap_mdp_oublie"):
                st.session_state["mathicap_afficher_recuperation"] = True
                st.rerun()
            if st.session_state.get("mathicap_afficher_recuperation"):
                _mathicap_formulaire_recuperation()

            with st.popover("Créer un compte"):
                with st.form("formulaire_inscription"):
                    email = st.text_input("Adresse e-mail")
                    pseudo = st.text_input("Pseudonyme (facultatif)")
                    mot_de_passe = st.text_input(
                        "Mot de passe", type="password"
                    )
                    confirmer_mdp = st.text_input(
                        "Confirmer le mot de passe", type="password"
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
                                st.secrets["SUPABASE_KEY"],
                            )
                            client_inscription.auth.sign_up({
                                "email": email.strip(),
                                "password": mot_de_passe,
                                "options": {"data": {"pseudo": pseudo.strip()}},
                            })
                            st.success(
                                "Inscription demandée. Consulte ton e-mail "
                                "pour confirmer ton compte.",
                                width=500,
                            )
                        except Exception:
                            st.error(
                                "Inscription impossible. Vérifie les informations "
                                "ou réessaie plus tard."
                            )

        if connexion:
            if not email_connexion.strip() or not mdp_connexion:
                st.warning("Renseigne ton e-mail et ton mot de passe.")
            else:
                try:
                    resultat = supabase.auth.sign_in_with_password({
                        "email": email_connexion.strip(),
                        "password": mdp_connexion,
                    })
                    if resultat.user and resultat.session:
                        st.session_state["eleve_id"] = resultat.user.id
                        st.session_state["session_eleve"] = resultat.session
                        jeton_persistant = enregistrer_session(
                            supabase_privee, resultat.user.id
                        )
                        st.session_state["jeton_persistant"] = jeton_persistant
                        # L'écriture locale est appliquée au rerun suivant par
                        # le pont natif Streamlit. Aucun composant externe à charger.
                        enregistrer_jeton_navigateur(jeton_persistant)
                        st.session_state["vider_champs_connexion"] = True
                        st.rerun()  
                    else:
                        st.error("Connexion impossible.")
                except Exception:
                    st.error("Une erreur est survenue lors de la connexion.")
# Rubriques accessibles depuis les icônes de l'en-tête.
# La page active est gardée dans l'URL : une actualisation y revient.
vue_icone = st.query_params.get("vue")
if vue_icone == "recherche":
    # Compatibilité des anciens liens : la recherche se fait désormais dans l'en-tête.
    st.query_params["vue"] = "accueil"

if vue_icone == "notifications":
    st.subheader("Notifications")
    if est_connecte:
        st.info("Aucune notification pour le moment.", width=500)
        st.caption("Les notifications seront disponibles lorsqu'un service de notification sera activé dans MathiCap.")
    else:
        st.info("Connecte-toi pour accéder à tes notifications.", width=500)
    st.button(
        "← Accueil",
        key="mathicap_notifications_retour",
        on_click=_mathicap_retour_accueil_logo,
    )
    st.stop()

# Nouvelle interface MathiCap Collège
# Synchroniser le menu avec l'URL, y compris lors d'une véritable actualisation.
# Ne pas écraser la page choisie au menu lorsque la session est déjà active.
_vue_mathicap = st.query_params.get("vue")
_page_en_memoire = st.session_state.get("mathicap_page")
if _page_en_memoire is None and _vue_mathicap == "exercices":
    st.session_state["mathicap_page"] = "Exercices"
elif _page_en_memoire is not None and _vue_mathicap != "profil":
    if _page_en_memoire == "Exercices" and _vue_mathicap != "exercices":
        st.query_params["vue"] = "exercices"
    elif _page_en_memoire == "Mes séries" and _vue_mathicap != "series":
        st.query_params["vue"] = "series"
    elif _page_en_memoire not in ("Exercices", "Mes séries") and _vue_mathicap in ("exercices", "series"):
        st.query_params["vue"] = "accueil"

if est_connecte and st.query_params.get("vue") == "profil":
    st.stop()

# Une série ouverte depuis « Mes séries » s'affiche dans « Exercices ».
# La navigation est préparée ici, avant la création du widget de menu.
if st.session_state.pop("_mathicap_ouvrir_serie", False):
    st.session_state["mathicap_page"] = "Exercices"
    st.session_state["afficher_series"] = False

# Tableau de bord : lecture du compte connecté, jamais d'un autre élève.
# Seules les séries sauvegardées sont comptées ; aucune note inventée.
@st.cache_data(ttl=30, show_spinner=False)
def _mathicap_donnees_tableau_bord(identifiant):
    reponse = (
        supabase_privee.table("series_exercices")
        .select("id, exercices, reponses")
        .eq("eleve_id", identifiant)
        .execute()
    )
    series = reponse.data or []
    statistiques = _mathicap_statistiques_progression(series)
    return {
        "disponible": True,
        "nb_series": len(series),
        "bonnes": statistiques["bonnes_verifiees"],
        "questions_verifiees": statistiques["questions_verifiees"],
        "exercices_repondus": statistiques["exercices_avec_reponse"],
        "exercices_total": statistiques["exercices_total"],
    }

if est_connecte and st.session_state.get("mathicap_page", "Accueil") == "Accueil":
    try:
        st.session_state["_mathicap_dashboard_donnees"] = (
            _mathicap_donnees_tableau_bord(st.session_state["eleve_id"])
        )
    except Exception:
        # Ne pas bloquer le reste de MathiCap si les statistiques sont indisponibles.
        st.session_state["_mathicap_dashboard_donnees"] = {"disponible": False}
else:
    st.session_state.pop("_mathicap_dashboard_donnees", None)

if _mc_nav_mesure and st.query_params.get("vue") != "profil":
    st.caption(
        "Mesure navigation (avant affichage de la rubrique) : "
        f"{round((time.perf_counter()-_mc_nav_debut)*1000)} ms "
        f"(dont session : {_mc_nav_auth_ms} ms)."
    )

page_mathicap = afficher_interface_mathicap()

# Hors de la rubrique Exercices, aucun clic de génération n'est possible.
demande_generation = False
if page_mathicap == "Exercices":
    with st.container(key="mathicap_reglages_exercices"):
        # Deux raccourcis utiles, sans perdre la série en cours ni refaire de requête.
        # La navigation s'adapte automatiquement à la largeur smartphone.
        with st.container(horizontal=True, horizontal_alignment="left", gap="small"):
            st.button(
                "← Accueil",
                key="mathicap_exercices_retour_accueil",
                on_click=_mathicap_retour_accueil_logo,
            )
            st.button(
                "Mes séries enregistrées →",
                key="mathicap_exercices_mes_series",
                on_click=_mathicap_reprendre_series_depuis_exercices,
            )
        # Réserver les sélecteurs et la génération à la rubrique Exercices.
        chapitres = CHAPITRES_MATHICAP

        # Lorsqu'on vient de la loupe, le bon chapitre est présélectionné.
        # Le choix reste modifiable normalement dans la page Exercices.
        chapitre_recherche = st.session_state.pop("_mathicap_chapitre_a_ouvrir", None)
        if chapitre_recherche in chapitres:
            st.session_state["mathicap_choix_chapitre"] = chapitre_recherche
        chapitre = st.selectbox(
            "Chapitre",
            list(chapitres.keys()),
            key="mathicap_choix_chapitre",
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
                max-width: 740px;
                box-sizing: border-box;
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

        # Une seule action pour les niveaux 1 à 9 : aucun générateur n'est déplacé.
        # Le clic est récupéré plus bas, après les fonctions de sauvegarde.
        with st.container(key="mathicap_action_generer"):
            demande_generation = st.button(
                "Générer mes exercices",
                key="mathicap_generer_exercices",
                type="primary",
                width="stretch",
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
def _mathicap_retablir_serie(serie, *, nouvelle_version=False):
    """Réhydrate tous les widgets depuis Supabase AVANT leur création Streamlit."""
    if not isinstance(serie, dict) or not isinstance(serie.get("exercices"), list):
        return False
    exercices = serie["exercices"]
    reponses = serie.get("reponses") or {}
    if not isinstance(reponses, dict):
        reponses = {}

    version = st.session_state.get("serie_version", 0) + (1 if nouvelle_version else 0)
    st.session_state["serie_version"] = version
    st.session_state["exercices_actuels"] = exercices
    st.session_state["code_actuel"] = serie.get("code_reprise")
    cle_cache = (st.session_state.get("eleve_id"), str(serie.get("code_reprise", "")).upper())
    st.session_state.setdefault("_mathicap_reponses_cache", {})[cle_cache] = dict(reponses)
    st.session_state["serie_ouverte_depuis_liste"] = True
    if serie.get("id") is not None:
        st.session_state["serie_id_actuel"] = serie["id"]

    for numero, exercice in enumerate(exercices, start=1):
        if not isinstance(exercice, dict):
            continue
        valeur = reponses.get(str(numero))
        cle_bilan_banque = f"bilan_banque_{version}_{numero}"
        cle_bilan_simple = f"bilan_simple_{version}_{numero}"
        st.session_state.pop(cle_bilan_banque, None)
        st.session_state.pop(cle_bilan_simple, None)

        if isinstance(valeur, dict) and valeur.get("type") == "banque":
            champs_sauvegardes = valeur.get("champs") or {}
            if not isinstance(champs_sauvegardes, dict):
                champs_sauvegardes = {}
            for champ in exercice.get("champs_reponse", []):
                if champ.get("id") not in champs_sauvegardes:
                    continue
                saisie = champs_sauvegardes[champ["id"]]
                if champ.get("type") == "choix" and saisie not in champ.get("options", []):
                    saisie = "Choisir..."
                st.session_state[f"banque_{version}_{numero}_{champ['id']}"] = saisie
            if isinstance(valeur.get("bilan"), dict):
                st.session_state[cle_bilan_banque] = valeur["bilan"]
        elif exercice.get("reponse_attendue") is not None:
            if isinstance(valeur, dict) and valeur.get("type") == "simple":
                saisie = valeur.get("valeur")
                if isinstance(valeur.get("bilan"), dict):
                    st.session_state[cle_bilan_simple] = valeur["bilan"]
            else:
                saisie = valeur
            if isinstance(saisie, (int, float)) and not isinstance(saisie, bool):
                st.session_state[f"reponse_{version}_{numero}"] = saisie
        elif not exercice.get("champs_reponse"):
            if isinstance(valeur, str):
                st.session_state[f"reponse_texte_{version}_{numero}"] = valeur
    return True


# Réhydrater une série seulement quand l'élève consulte les exercices.
# Les autres rubriques, notamment « Mes séries », n'en ont pas besoin.
if (page_mathicap == "Exercices" and st.session_state.get("eleve_id")
        and "exercices_actuels" not in st.session_state):
    try:
        series_auto = recuperer_exercices_eleve(st.session_state["eleve_id"])
        if series_auto:
            # Priorité à la série exacte ouverte avant actualisation.
            identifiant_url = st.query_params.get("serie_id")
            cible = next(
                (serie for serie in series_auto if str(serie.get("id")) == str(identifiant_url)),
                None,
            ) if identifiant_url else None
            if cible is None:
                cible = series_auto[0]
            _mathicap_retablir_serie(cible)
    except Exception:
        st.session_state["erreur_reprise_series"] = True

# Ne garder les séries en cache que pendant la consultation de cette rubrique.
# Une visite sur les Exercices supprimera la copie, pour relire les réponses
# modifiées lors du prochain retour sur la liste.
if page_mathicap != "Mes séries":
    st.session_state.pop("_mathicap_series_pagination_cache", None)

if page_mathicap == "Mes séries" and st.session_state.get("eleve_id"):
    # La rubrique « Mes séries » ouvre directement la liste enregistrée.
    try:
        _mc_nav_series_debut = time.perf_counter()
        cache_page = st.session_state.get("_mathicap_series_pagination_cache")
        valide_page = (
            isinstance(cache_page, dict)
            and cache_page.get("eleve_id") == st.session_state["eleve_id"]
            and cache_page.get("jeton") == st.session_state.get("jeton_persistant")
            and isinstance(cache_page.get("series"), list)
            and isinstance(cache_page.get("charge_le"), (int, float))
            and 0 <= time.monotonic() - cache_page["charge_le"] <= 60
        )
        cache_profil = st.session_state.pop("_mathicap_nav_series_profil_v7", None)
        valide_depuis_profil = (
            isinstance(cache_profil, dict)
            and cache_profil.get("eleve_id") == st.session_state["eleve_id"]
            and cache_profil.get("jeton") == st.session_state.get("jeton_persistant")
            and isinstance(cache_profil.get("series"), list)
            and isinstance(cache_profil.get("charge_le"), (int, float))
            and 0 <= time.monotonic() - cache_profil["charge_le"] <= 20
        )
        if valide_page:
            # Les boutons et filtres ne déclenchent pas une nouvelle lecture.
            series = cache_page["series"]
            _mc_nav_series_source = "cache de la liste"
        elif valide_depuis_profil:
            # Evite une seconde requete quand on vient directement du profil.
            series = cache_profil["series"]
            _mc_nav_series_source = "reutilisees depuis le profil"
        else:
            series = recuperer_exercices_eleve(st.session_state["eleve_id"])
            _mc_nav_series_source = "lecture Supabase"
        if not valide_page:
            # Cache réservé à cette session Streamlit et au jeton de cet élève.
            st.session_state["_mathicap_series_pagination_cache"] = {
                "eleve_id": st.session_state["eleve_id"],
                "jeton": st.session_state.get("jeton_persistant"),
                "charge_le": time.monotonic(),
                "series": series,
            }
        _mc_nav_series_ms = round((time.perf_counter() - _mc_nav_series_debut) * 1000)
        if _mc_nav_mesure:
            st.caption(
                "Mesure navigation — préparation/en-tête : "
                f"{_mc_nav_entete_ms} ms (dont session : {_mc_nav_auth_ms} ms) ; "
                f"séries ({_mc_nav_series_source}) : {_mc_nav_series_ms} ms ; "
                f"total avant affichage : {round((time.perf_counter()-_mc_nav_debut)*1000)} ms."
            )

        if not series:
            st.info("Aucune série enregistrée pour ce compte.", width=500)
        else:
            st.caption(f"{len(series)} série(s) enregistrée(s) · plus récente(s) en premier.")
            ids_series = [s["id"] for s in series]

            # Préparer une fois les informations déjà sauvegardées, sans appel
            # Supabase supplémentaire. La numérotation utilise la liste complète
            # (pas la liste filtrée) : elle reste stable pendant un filtrage.
            compteurs_chapitres = {}
            fiches_series = []
            for serie in series:
                bilan_serie = _mathicap_statistiques_progression([serie])
                total = bilan_serie["exercices_total"]
                renseignes = bilan_serie["exercices_avec_reponse"]
                pourcentage = round(100 * renseignes / total) if total else 0

                exercices_serie = serie.get("exercices") or []
                chapitres_serie = sorted({
                    exercice["mathicap_chapitre"].strip()
                    for exercice in exercices_serie
                    if isinstance(exercice, dict)
                    and isinstance(exercice.get("mathicap_chapitre"), str)
                    and exercice["mathicap_chapitre"].strip()
                }) if isinstance(exercices_serie, list) else []
                niveaux_serie = sorted({
                    exercice["mathicap_niveau"]
                    for exercice in exercices_serie
                    if isinstance(exercice, dict)
                    and type(exercice.get("mathicap_niveau")) is int
                    and 1 <= exercice["mathicap_niveau"] <= 9
                }) if isinstance(exercices_serie, list) else []

                titre_chapitre = (
                    chapitres_serie[0] if len(chapitres_serie) == 1
                    else "Plusieurs chapitres" if chapitres_serie else "Chapitre non précisé"
                )
                titres_niveaux = (
                    "Niveau " + str(niveaux_serie[0]) if len(niveaux_serie) == 1
                    else "Niveaux " + ", ".join(map(str, niveaux_serie))
                    if niveaux_serie else "Niveau non précisé"
                )
                numero_serie = compteurs_chapitres.get(titre_chapitre, 0) + 1
                compteurs_chapitres[titre_chapitre] = numero_serie

                etat_serie = (
                    "À commencer" if renseignes == 0
                    else "Tous renseignés" if total and renseignes == total
                    else "En cours"
                )
                fiches_series.append({
                    "serie": serie,
                    "chapitres": chapitres_serie,
                    "niveaux": niveaux_serie,
                    "titre_chapitre": titre_chapitre,
                    "titres_niveaux": titres_niveaux,
                    "numero": numero_serie,
                    "total": total,
                    "renseignes": renseignes,
                    "pourcentage": pourcentage,
                    "etat": etat_serie,
                })

            chapitres_disponibles = sorted({
                chap for fiche in fiches_series for chap in fiche["chapitres"]
            }, key=str.casefold)
            if any(not fiche["chapitres"] for fiche in fiches_series):
                chapitres_disponibles.append("Chapitre non précisé")
            # Toujours montrer le parcours complet de 1 à 9 ; un niveau sans
            # série affichera simplement un résultat vide (aucune requête en plus).
            options_chapitres = ["Tous les chapitres", *chapitres_disponibles]
            options_niveaux = ["Tous les niveaux", *[f"Niveau {n}" for n in range(1, 10)]]
            if any(not fiche["niveaux"] for fiche in fiches_series):
                options_niveaux.append("Niveau non précisé")
            options_etats = ["Tous les avancements", "À commencer", "En cours", "Tous renseignés"]

            eleve_courant = st.session_state["eleve_id"]
            cle_tout = f"tout_selectionner_{eleve_courant}"
            cle_chapitre = f"mathicap_series_filtre_chapitre_{eleve_courant}"
            cle_niveau = f"mathicap_series_filtre_niveau_{eleve_courant}"
            cle_etat = f"mathicap_series_filtre_etat_{eleve_courant}"
            cle_taille_page = f"mathicap_series_taille_page_{eleve_courant}"
            cle_page = f"mathicap_series_page_{eleve_courant}"

            def effacer_selection_series():
                # Ne jamais conserver une sélection cachée sur une autre page.
                st.session_state[cle_tout] = False
                for identifiant in ids_series:
                    st.session_state.pop(f"cocher_serie_{identifiant}", None)
                st.session_state.pop("suppression_en_attente", None)

            def reinitialiser_selection_apres_filtre():
                effacer_selection_series()
                st.session_state[cle_page] = 1

            def changer_taille_page():
                effacer_selection_series()
                st.session_state[cle_page] = 1

            def naviguer_page(decalage):
                # Callback : exécuté avant la création du sélecteur de page.
                st.session_state[cle_page] += decalage
                effacer_selection_series()

            for cle, choix_possibles in (
                (cle_chapitre, options_chapitres),
                (cle_niveau, options_niveaux),
                (cle_etat, options_etats),
            ):
                if st.session_state.get(cle) not in choix_possibles:
                    st.session_state[cle] = choix_possibles[0]

            # Conserver le même choix 5/10/20, mais l'intégrer au titre
            # des filtres : pas de cadre de pagination séparé ni d'espace vide.
            if st.session_state.get(cle_taille_page) not in (5, 10, 20):
                st.session_state[cle_taille_page] = 5

            with st.container(key="mathicap_series_filtres"):
                with st.container(
                    horizontal=True,
                    horizontal_alignment="right",
                    vertical_alignment="center",
                    gap="xsmall",
                    key="mathicap_series_entete_filtres",
                ):
                    st.html('<div class="mc-series-filtres-titre">Filtrer mes séries</div>')
                    st.html('<span class="mc-series-taille-label">Séries par page</span>')
                    st.selectbox(
                        "Séries par page", (5, 10, 20),
                        key=cle_taille_page, on_change=changer_taille_page,
                        label_visibility="collapsed", width=82,
                    )
                col_chapitre, col_niveau, col_etat = st.columns([2, 1.1, 1.3], gap="small")
                with col_chapitre:
                    with st.container(key="mathicap_series_filtre_chapitre_couleur"):
                        filtre_chapitre = st.selectbox(
                            "Chapitre", options_chapitres, key=cle_chapitre,
                            on_change=reinitialiser_selection_apres_filtre,
                        )
                with col_niveau:
                    with st.container(key="mathicap_series_filtre_niveau_couleur"):
                        filtre_niveau = st.selectbox(
                            "Niveau", options_niveaux, key=cle_niveau,
                            on_change=reinitialiser_selection_apres_filtre,
                        )
                with col_etat:
                    with st.container(key="mathicap_series_filtre_etat_couleur"):
                        filtre_etat = st.selectbox(
                            "Avancement", options_etats, key=cle_etat,
                            on_change=reinitialiser_selection_apres_filtre,
                        )

            fiches_visibles = [
                fiche for fiche in fiches_series
                if (filtre_chapitre == "Tous les chapitres"
                    or (filtre_chapitre == "Chapitre non précisé" and not fiche["chapitres"])
                    or filtre_chapitre in fiche["chapitres"])
                and (filtre_niveau == "Tous les niveaux"
                     or (filtre_niveau == "Niveau non précisé" and not fiche["niveaux"])
                     or (filtre_niveau.startswith("Niveau ")
                         and filtre_niveau[7:].isdigit()
                         and int(filtre_niveau[7:]) in fiche["niveaux"]))
                and (filtre_etat == "Tous les avancements" or fiche["etat"] == filtre_etat)
            ]
            # Les filtres portent sur la liste complète. La pagination porte
            # uniquement sur l'affichage ; numéros et données restent inchangés.
            nombre_filtre = len(fiches_visibles)
            taille_page = st.session_state[cle_taille_page]
            nombre_pages = max(1, (nombre_filtre + taille_page - 1) // taille_page)
            if (type(st.session_state.get(cle_page)) is not int
                    or not 1 <= st.session_state[cle_page] <= nombre_pages):
                st.session_state[cle_page] = 1

            # Recalcul après les éventuels callbacks Streamlit.
            taille_page = st.session_state[cle_taille_page]
            page_actuelle = st.session_state[cle_page]
            debut_page = (page_actuelle - 1) * taille_page
            fin_page = min(debut_page + taille_page, nombre_filtre)
            fiches_visibles = fiches_visibles[debut_page:fin_page]
            ids_visibles = [fiche["serie"]["id"] for fiche in fiches_visibles]

            def cocher_toutes_series():
                etat = st.session_state[cle_tout]
                for identifiant in ids_visibles:
                    st.session_state[f"cocher_serie_{identifiant}"] = etat

            def synchroniser_selection():
                st.session_state[cle_tout] = bool(ids_visibles) and all(
                    st.session_state.get(f"cocher_serie_{identifiant}", False)
                    for identifiant in ids_visibles
                )

            st.checkbox(
                "Tout sélectionner les séries de cette page",
                key=cle_tout,
                on_change=cocher_toutes_series,
                disabled=not ids_visibles,
            )

            selection = [
                identifiant for identifiant in ids_visibles
                if st.session_state.get(f"cocher_serie_{identifiant}", False)
            ]

            # La commande destructive n'apparaît qu'après une sélection explicite.
            if selection:
                if st.button(
                    f"Supprimer la sélection ({len(selection)})",
                    key="mathicap_supprimer_series_cochees",
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
                                    st.session_state.pop("serie_id_actuel", None)
                                    st.query_params.pop("serie_id", None)
                                    st.session_state["serie_version"] = (
                                        st.session_state.get(
                                            "serie_version", 0
                                        ) + 1
                                    )

                                st.session_state.pop(
                                    "suppression_en_attente", None
                                )
                                # Une suppression confirmée invalide la copie locale.
                                st.session_state.pop(
                                    "_mathicap_series_pagination_cache", None
                                )
                                st.session_state["afficher_series"] = True
                                st.rerun()

                        except Exception:
                            st.error(
                                "Impossible de supprimer les séries. "
                                "Aucune nouvelle tentative automatique "
                                "ne sera effectuée."
                            )

            if not fiches_visibles:
                st.info("Aucune série ne correspond aux filtres choisis.", width=500)

            # Les numéros ont été calculés sur toutes les séries du chapitre.
            # Les filtres ne renumérotent jamais les séries affichées.
            for fiche in fiches_visibles:
                serie = fiche["serie"]
                numero_serie = fiche["numero"]
                titre_chapitre = fiche["titre_chapitre"]
                titres_niveaux = fiche["titres_niveaux"]
                total = fiche["total"]
                renseignes = fiche["renseignes"]
                pourcentage = fiche["pourcentage"]

                with st.container(border=True, key=f"mathicap_series_carte_{serie['id']}"):
                    colonne_selection, colonne_detail = st.columns(
                        [1, 9], gap="small", vertical_alignment="top"
                    )
                    with colonne_selection:
                        st.checkbox(
                            f"Sélectionner la série {numero_serie}",
                            key=f"cocher_serie_{serie['id']}",
                            label_visibility="collapsed",
                            on_change=synchroniser_selection,
                        )
                    with colonne_detail:
                        st.markdown(f"**Série {numero_serie}** · {titre_chapitre}")
                        st.caption(f"{titres_niveaux} · {total} exercice(s) · {fiche['etat']}")
                        st.progress(
                            pourcentage,
                            text=(f"{renseignes}/{total} exercices avec réponse "
                                  f"({pourcentage} %)")
                        )
                        with st.container(
                            horizontal=True,
                            horizontal_alignment="left",
                            gap="small",
                            key=f"mathicap_series_actions_{serie['id']}",
                        ):
                            if st.button(
                                "Ouvrir",
                                key=f"reprendre_serie_{serie['id']}",
                                type="primary",
                            ):
                                if _mathicap_retablir_serie(serie, nouvelle_version=True):
                                    st.session_state["afficher_series"] = False
                                    st.session_state["_mathicap_ouvrir_serie"] = True
                                    st.query_params["vue"] = "exercices"
                                    st.query_params["serie_id"] = str(serie["id"])
                                    st.rerun()
                                else:
                                    st.error("Cette série ne peut pas être restaurée.")

                            if st.button(
                                "Supprimer",
                                key=f"supprimer_serie_{serie['id']}",
                                type="secondary",
                            ):
                                # Réutiliser le même dialogue de confirmation
                                # et le même traitement Supabase que la sélection multiple.
                                st.session_state["suppression_en_attente"] = {
                                    "mode": "selection",
                                    "ids": [serie["id"]],
                                    "eleve_id": st.session_state["eleve_id"],
                                }
                                st.rerun()

            # Barre de navigation pleine largeur, boutons à droite et sous les fiches.
            # Aucun accès Supabase : seul l'index de la page change.
            if nombre_pages > 1:
                with st.container(
                    horizontal=True,
                    horizontal_alignment="right",
                    gap="small",
                    key="mathicap_series_pagination_bas",
                ):
                    st.button(
                        "← Précédent", key="mathicap_series_page_precedente",
                        disabled=page_actuelle <= 1,
                        on_click=naviguer_page, args=(-1,),
                    )
                    st.caption(f"Page {page_actuelle} / {nombre_pages}")
                    st.button(
                        "Suivant →", key="mathicap_series_page_suivante",
                        disabled=page_actuelle >= nombre_pages,
                        on_click=naviguer_page, args=(1,),
                    )

    except Exception:
        st.error("Impossible de récupérer tes exercices.")

# Ne jamais afficher le générateur au-dessous de la liste des séries.
if page_mathicap == "Mes séries":
    st.stop()

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
        resultat = supabase_privee.table("series_exercices").insert({
            "eleve_id": st.session_state.get("eleve_id"),
            "code_reprise": code,
            "exercices": exercices,
            "reponses": {},
            "progression": 0
        }).execute()
        donnees = resultat.data or []
        if not donnees:
            raise RuntimeError("La création de la série n'a pas été confirmée.")
        st.session_state["serie_id_actuel"] = donnees[0].get("id")
        st.session_state.setdefault("_mathicap_reponses_cache", {})[(
            st.session_state["eleve_id"], code.upper()
        )] = {}
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
    """Sauvegarder en 1 écriture lorsque la série est déjà chargée.

    Le cache local est initialisé lors de la création/ouverture de la série.
    À défaut, une lecture unique est effectuée. Le cache n'est mis à jour
    qu'après confirmation de Supabase, sans masquer les erreurs.
    """
    eleve_id = st.session_state.get("eleve_id")
    if not eleve_id or not isinstance(code, str) or not code.strip():
        return False

    code_normalise = code.strip().upper()
    cle = (eleve_id, code_normalise)
    cache = st.session_state.setdefault("_mathicap_reponses_cache", {})
    if cle not in cache:
        serie = recuperer_serie(code_normalise)
        if not serie:
            return False
        cache[cle] = dict(serie.get("reponses") or {})

    reponses = dict(cache[cle])
    reponses[str(numero)] = reponse
    resultat = (
        supabase_privee.table("series_exercices")
        .update({"reponses": reponses})
        .eq("code_reprise", code_normalise)
        .eq("eleve_id", eleve_id)
        .execute()
    )
    if not resultat.data:
        return False
    cache[cle] = reponses
    return True
    
def enregistrer_reponse_auto(numero):
    code = st.session_state.get("code_actuel")
    version = st.session_state.get("serie_version", 0)
    reponse = st.session_state.get(f"reponse_{version}_{numero}")
    st.session_state.pop(f"bilan_simple_{version}_{numero}", None)

    if code and reponse is not None:
        try:
            if not sauvegarder_reponse(code, numero, reponse):
                st.session_state["erreur_sauvegarde"] = True
        except Exception:
            st.session_state["erreur_sauvegarde"] = True
def enregistrer_reponse_texte_auto(numero):
    """Conserve les réponses rédigées, qui n'étaient pas sauvegardées avant."""
    code = st.session_state.get("code_actuel")
    cle = f"reponse_texte_{st.session_state.get('serie_version', 0)}_{numero}"
    if code and st.session_state.get("eleve_id"):
        try:
            if not sauvegarder_reponse(code, numero, st.session_state.get(cle, "")):
                st.session_state["erreur_sauvegarde"] = True
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
        confirme = sauvegarder_reponse(
            code,
            numero,
            {
                "type": "banque",
                "champs": reponses
            }
        )
        if not confirme:
            st.session_state["erreur_sauvegarde"] = True
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
            correction = _mathicap_correction_division_euclidienne(
                dividende, diviseur, quotient, reste
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

                    livres_initiaux = random.randint(70, 110)
                    livres_recus = random.randint(15, 35)
                    total = livres_initiaux + livres_recus

                    q_p, r_p = divmod(total, petite)
                    q_g, r_g = divmod(total, grande)

                    attendu1 = q_p + (1 if r_p > 0 else 0)
                    nombre_grandes = q_g + (1 if r_g > 0 else 0)
                    attendu2 = attendu1 - nombre_grandes

                    enonce = (
                        f"Une bibliothèque possède {livres_initiaux} livres "
                        f"et reçoit {livres_recus} nouveaux livres.\n\n"

                        f"Elle doit transporter tous ses livres.\n\n"

                        f"Elle peut utiliser :\n"
                        f"- des petites caisses de {petite} livres maximum ;\n"
                        f"- des grandes caisses de {grande} livres maximum.\n\n"

                        f"La bibliothèque souhaite utiliser le moins "
                        f"de caisses possible.\n\n"

                        f"1. Combien de petites caisses faut-il "
                        f"au minimum pour transporter tous les livres ?\n\n"

                        f"2. Combien de caisses économise-t-elle "
                        f"en utilisant uniquement les grandes caisses ?"
                    )

                    correction = (
                        f"**1. Nombre de petites caisses**\n\n"

                        f"Nombre total de livres :\n"
                        f"{livres_initiaux} + {livres_recus} "
                        f"= {total} livres.\n\n"

                        f"Division : {total} ÷ {petite}\n"
                        f"Quotient : {q_p}, reste : {r_p}.\n\n"

                        f"Il faut donc {attendu1} petites caisses.\n\n"

                        f"**2. Nombre de grandes caisses**\n\n"

                        f"Division : {total} ÷ {grande}\n"
                        f"Quotient : {q_g}, reste : {r_g}.\n\n"

                        f"Il faut {nombre_grandes} grandes caisses.\n\n"

                        f"**Comparaison**\n\n"

                        f"{attendu1} − {nombre_grandes} "
                        f"= {attendu2} caisses économisées.\n\n"

                        f"Lorsqu'une division laisse un reste, "
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
            if type_exercice == "Mes automatismes" and difficulte == 3:
                autre_nombre = random.randint(2, min(8, quotient))
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
                    f"On effectue d'abord la division :\n\n"
                    f"{dividende} ÷ {diviseur} = {quotient}.\n\n"
                    f"Puis : {quotient} {signe} {autre_nombre} "
                    f"= {resultat}."
                )

                reponse_attendue = resultat

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
if demande_generation:
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
                            "Des exercices alternatifs ont été générés.",
                            width=500,
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
        # Mémoriser le chapitre et le niveau pour les nouveaux suivis.
        # Les anciennes séries restent lisibles sans ces métadonnées.
        for exercice in exercices:
            if isinstance(exercice, dict):
                exercice.setdefault("mathicap_chapitre", chapitre)
                exercice.setdefault("mathicap_niveau", niveau_reel)

        st.session_state.exercices_actuels = exercices
        st.session_state["serie_ouverte_depuis_liste"] = False
        st.session_state["serie_version"] = st.session_state.get("serie_version", 0) + 1
        st.query_params["vue"] = "exercices"
        st.query_params.pop("serie_id", None)
    
        if st.session_state.get("eleve_id"):
            try:
                code = sauvegarder_serie(exercices)
                if code:
                    st.session_state.code_actuel = code
                    if st.session_state.get("serie_id_actuel") is not None:
                        st.query_params["serie_id"] = str(st.session_state["serie_id_actuel"])
                    st.toast("Exercices générés et sauvegardés !", icon="✅", duration=3)
                else:
                    st.error("Sauvegarde impossible.")
            except Exception:
                st.error("Sauvegarde impossible.")
        else:
            st.session_state.code_actuel = None
            st.info("Connecte-toi pour sauvegarder tes exercices.", width=500)
# Les saisies ne relancent plus toute l'application (en-tête, menus et statistiques).
# Le fragment garde le défilement plus stable lors de la sauvegarde automatique.
@st.fragment
def _mathicap_afficher_serie_et_reponses():
    with st.container(key="mathicap_zone_exercices_affichage"):
        if st.session_state.pop("erreur_sauvegarde", False):
            st.error("Une réponse n'a pas pu être enregistrée. Vérifie ta connexion avant de quitter cette page.")
        if st.session_state.pop("erreur_reprise_series", False):
            st.warning("Impossible de récupérer automatiquement la dernière série enregistrée.")
        if st.session_state.exercices_actuels:
            for numero, exercice in enumerate(st.session_state.exercices_actuels, start=1):
                st.subheader(f"Exercice {numero}")           
                est_distributivite = (
                    exercice["enonce"].startswith(
                        "Utilise la distributivité pour calculer :"
                    )
                    and bool(exercice.get("champs_reponse"))
                    and all(
                        c["id"].startswith("calcul_")
                        for c in exercice["champs_reponse"]
                    )
                )

                if est_distributivite:
                    lignes_calcul = exercice["enonce"].split("\n\n")[1:]
                    st.write("Utilise la distributivité pour calculer :")
                else:
                    with st.container(key=f"mathicap_enonce_{numero}"):
                        st.write(exercice["enonce"])

    
                if exercice.get("reponse_attendue") is not None:  
                    col_texte, col_saisie = st.columns(
                        [1.4, 1],
                        gap="small",
                        vertical_alignment="top",
                        wrap=False
                    )

                    with col_texte:
                        st.write("Ta réponse :")

                    with col_saisie:
                        reponse_eleve = st.number_input(
                            "Ta réponse :",
                            label_visibility="collapsed",
                            value=None,
                            step=0.01 if isinstance(
                                exercice.get("reponse_attendue"), float
                            ) else 1,
                            key=f"reponse_{st.session_state.get('serie_version', 0)}_{numero}",
                            on_change=enregistrer_reponse_auto,
                            args=(numero,)
                        )    
                    cle_bilan_simple = (
                        f"bilan_simple_{st.session_state.get('serie_version', 0)}_{numero}"
                    )
                    if st.button("Vérifier ma réponse", key=f"verifier_{numero}"):
                        if reponse_eleve is None:
                            st.warning("Saisis d'abord ta réponse.")
                        else:
                            correcte = reponse_eleve == exercice["reponse_attendue"]
                            bilan_simple = {"bonnes": int(correcte), "total": 1}
                            st.session_state[cle_bilan_simple] = bilan_simple
                            code = st.session_state.get("code_actuel")
                            if code and st.session_state.get("eleve_id"):
                                try:
                                    confirme = sauvegarder_reponse(code, numero, {
                                        "type": "simple",
                                        "valeur": reponse_eleve,
                                        "bilan": bilan_simple,
                                    })
                                    if not confirme:
                                        st.error("Le résultat n'a pas pu être enregistré.")
                                except Exception:
                                    st.error("Le résultat n'a pas pu être enregistré.")
                            if correcte:
                                st.success("Bonne réponse !", width=500)
                            else:
                                st.error("Réponse incorrecte. Essaie encore.")
                    elif isinstance(st.session_state.get(cle_bilan_simple), dict):
                        dernier = st.session_state[cle_bilan_simple]
                        st.caption(
                            "Dernière vérification : "
                            + ("Bonne réponse" if dernier.get("bonnes") else "Réponse incorrecte")
                        )
                elif exercice.get("champs_reponse"):        
                    champs = exercice["champs_reponse"]
                    division_euclidienne = (
                        len(champs) == 2
                        and all(c["type"] == "nombre" for c in champs)
                        and {
                            c["libelle"].strip().lower()
                            for c in champs
                        } == {"quotient", "reste"}
                    )

                    if division_euclidienne:
                        colonnes_division = st.columns(
                            [1.0, 1.0],
                            gap="small",
                            wrap=False
                        )

                    for index, champ in enumerate(champs):
                        etiquette = (
                            f"Question {champ['question']} — "
                            f"{champ['libelle']}"
                        )
                        cle = (
                            f"banque_{st.session_state.get('serie_version', 0)}"
                            f"_{numero}_{champ['id']}"
                        )
                    
                        if champ["type"] == "nombre":
                            if est_distributivite:
                                col_calcul, col_reponse = st.columns(
                                    [1.4, 1],
                                    gap="small",
                                    vertical_alignment="top",
                                    wrap=False
                                )

                                with col_calcul:
                                    st.write(lignes_calcul[index])

                                with col_reponse:
                                    st.text_input(
                                        etiquette,
                                        label_visibility="collapsed",
                                        placeholder="Réponse",
                                        key=cle,
                                        on_change=enregistrer_reponses_banque_auto,
                                        args=(numero,)
                                    )

                            elif division_euclidienne:

                                with colonnes_division[index]:
                                    st.text_input(
                                        champ["libelle"],
                                        placeholder="Réponse",
                                        key=cle,
                                        on_change=enregistrer_reponses_banque_auto,
                                        args=(numero,)
                                    )
                            else:
                                # Le libellé est écrit directement sur la page.
                                # Aucune colonne de hauteur fixe ne peut le tronquer.
                                with st.container(key=f"mathicap_question_{numero}_{index}"):
                                    st.write(etiquette)
                                with st.container(
                                    key=f"mathicap_champ_reponse_{numero}_{index}"
                                ):
                                    st.text_input(
                                        etiquette,
                                        label_visibility="collapsed",
                                        placeholder="Réponse",
                                        key=cle,
                                        on_change=enregistrer_reponses_banque_auto,
                                        args=(numero,)
                                    )

                        elif champ["type"] == "choix":
                            with st.container(key=f"mathicap_question_{numero}_{index}"):
                                st.write(etiquette)
                            with st.container(
                                key=f"mathicap_champ_reponse_{numero}_{index}"
                            ):
                                st.selectbox(
                                    etiquette,
                                    ["Choisir..."] + champ["options"],
                                    label_visibility="collapsed",
                                    key=cle,
                                    on_change=enregistrer_reponses_banque_auto,
                                    args=(numero,)
                                )

                        elif champ["type"] == "texte_libre":
                            with st.container(
                                key=f"mathicap_reponse_texte_{numero}_{index}"
                            ):
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
    
                            bilan_verifie = {
                                "bonnes": bonnes_reponses,
                                "total": total_reponses,
                            }
                            try:
                                confirme = sauvegarder_reponse(
                                    code,
                                    numero,
                                    {
                                        "type": "banque",
                                        "champs": reponses_banque,
                                        "bilan": bilan_verifie,
                                    }
                                )
                                if confirme:
                                    st.session_state[
                                        f"bilan_banque_{st.session_state.get('serie_version', 0)}_{numero}"
                                    ] = bilan_verifie
                                else:
                                    st.error("Le bilan n'a pas pu être enregistré.")
                            except Exception:
                                st.error("Le bilan n'a pas pu être enregistré.")
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
                    with st.container(key=f"mathicap_reponse_texte_libre_{numero}"):
                        st.text_area(
                            "Ta réponse :",
                            placeholder="Écris ici tes réponses aux questions de l'exercice.",
                            height=150,
                            key=f"reponse_texte_{st.session_state.get('serie_version', 0)}_{numero}",
                            on_change=enregistrer_reponse_texte_auto,
                            args=(numero,),
                        )
                    if st.button(
                        "Enregistrer ma réponse",
                        key=f"enregistrer_texte_{st.session_state.get('serie_version', 0)}_{numero}",
                    ):
                        code = st.session_state.get("code_actuel")
                        cle_texte = f"reponse_texte_{st.session_state.get('serie_version', 0)}_{numero}"
                        if code and st.session_state.get("eleve_id"):
                            try:
                                if sauvegarder_reponse(code, numero, st.session_state.get(cle_texte, "")):
                                    st.toast("Réponse enregistrée.", icon="✅", duration=3)
                                else:
                                    st.error("Impossible d'enregistrer cette réponse.")
                            except Exception:
                                st.error("Impossible d'enregistrer cette réponse.")
                        else:
                            st.warning("Connecte-toi pour sauvegarder ta réponse.")

                with st.expander(
                    f"Voir la correction{'​' * (st.session_state.get('serie_version', 0) + 1)}",
                    expanded=False
                ):
                    texte_correction = exercice["correction"]
                    # Rendre explicites le quotient et le reste, y compris
                    # pour les séries créées avant cette mise à jour.
                    champs_division = exercice.get("champs_reponse") or []
                    if (
                        exercice.get("enonce", "").startswith(
                            "Effectue la division euclidienne de "
                        )
                        and {champ.get("id") for champ in champs_division}
                        == {"quotient", "reste"}
                    ):
                        donnees_division = {
                            champ["id"]: champ.get("attendu")
                            for champ in champs_division
                        }
                        match_division = re.search(
                            r"division euclidienne de (\d+) par (\d+)",
                            exercice.get("enonce", ""),
                            flags=re.IGNORECASE,
                        )
                        if (
                            match_division
                            and all(
                                donnees_division.get(cle) is not None
                                for cle in ("quotient", "reste")
                            )
                        ):
                            dividende, diviseur = map(int, match_division.groups())
                            quotient = int(donnees_division["quotient"])
                            reste = int(donnees_division["reste"])
                            texte_correction = _mathicap_correction_division_euclidienne(
                                dividende, diviseur, quotient, reste
                            )
                    st.markdown(texte_correction.replace("\n", "  \n"))
            

_mathicap_afficher_serie_et_reponses()

