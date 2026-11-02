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
    page_title="MathiCap Collège",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)
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
    width: calc(var(--mc-avatar) + 2 * var(--mc-ico) + 2 * var(--mc-ico-gap)) !important;
    min-width: calc(var(--mc-avatar) + 2 * var(--mc-ico) + 2 * var(--mc-ico-gap)) !important;
}

.st-key-mathicap_zone_profil .st-key-mathicap_avatar_clic {
    position: absolute !important;
    top: 0 !important;
    right: 0 !important;
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
    grid-template-columns: minmax(0, 1fr) auto !important;
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

/* Espacement sous la rangée d'icônes (sans boutons superposés). */
.mathicap-espace-icones {
    display: block;
    height: var(--mc-ico);
    width: 100%;
    pointer-events: none;
}

/* Loupe et cloche : deux vrais boutons Streamlit, placés avant l'avatar. */
.st-key-mathicap_zone_profil .st-key-mathicap_recherche_clic,
.st-key-mathicap_zone_profil .st-key-mathicap_notifications_clic {
    position: absolute !important;
    top: 0 !important;
    width: var(--mc-ico) !important;
    min-width: var(--mc-ico) !important;
    max-width: var(--mc-ico) !important;
    height: var(--mc-ico) !important;
    min-height: var(--mc-ico) !important;
    max-height: var(--mc-ico) !important;
    z-index: 11 !important;
    margin: 0 !important;
    padding: 0 !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_recherche_clic {
    right: calc(var(--mc-avatar) + var(--mc-ico) + 2 * var(--mc-ico-gap)) !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_notifications_clic {
    right: calc(var(--mc-avatar) + var(--mc-ico-gap)) !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_recherche_clic [data-testid="stButton"],
.st-key-mathicap_zone_profil .st-key-mathicap_notifications_clic [data-testid="stButton"] {
    width: var(--mc-ico) !important;
    height: var(--mc-ico) !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_recherche_clic button,
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
.st-key-mathicap_zone_profil .st-key-mathicap_recherche_clic button:hover,
.st-key-mathicap_zone_profil .st-key-mathicap_notifications_clic button:hover {
    background: #eaf1fc !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_recherche_clic button:focus-visible,
.st-key-mathicap_zone_profil .st-key-mathicap_notifications_clic button:focus-visible {
    outline: 2px solid #2563eb !important;
    outline-offset: 2px !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_recherche_clic button p,
.st-key-mathicap_zone_profil .st-key-mathicap_notifications_clic button p {
    position: absolute !important;
    width: 1px !important;
    height: 1px !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    clip-path: inset(50%) !important;
}
.st-key-mathicap_zone_profil .st-key-mathicap_recherche_clic button::before,
.st-key-mathicap_zone_profil .st-key-mathicap_notifications_clic button::before {
    content: "";
    display: block;
    width: 68%;
    height: 68%;
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    pointer-events: none;
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
/* Bouton Déconnexion compact sur smartphone uniquement */
@media (max-width: 767px) {

    div[data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic)
    > div[data-testid="stColumn"]:last-child
    div[data-testid="stButton"] {
        width: fit-content !important;
        margin-left: auto !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic)
    > div[data-testid="stColumn"]:last-child
    div[data-testid="stButton"] button {
        width: auto !important;
        min-width: 0 !important;
        height: 24px !important;
        min-height: 24px !important;
        padding: 1px 4px !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic)
    > div[data-testid="stColumn"]:last-child
    div[data-testid="stButton"] button p {
        font-size: 10px !important;
    }
}
/* Réduire l'espace au-dessus de l'en-tête sur PC uniquement */
/* Hauteur cohérente sur PC, plein écran ou demi-écran */
@media (min-width: 768px) {
    [data-testid="stMainBlockContainer"]:has(.st-key-mathicap_logo_clic) {
        padding-top: 2.75rem !important;
    }
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

/* Les deux boutons d'icône gardent une zone de clic carrée sur mobile.
   Ces règles, plus ciblées, prennent le pas sur celles de Déconnexion. */
div[data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic)
> div[data-testid="stColumn"]:last-child
.st-key-mathicap_recherche_clic button,
div[data-testid="stHorizontalBlock"]:has(.st-key-mathicap_logo_clic)
> div[data-testid="stColumn"]:last-child
.st-key-mathicap_notifications_clic button {
    width: var(--mc-ico) !important;
    min-width: var(--mc-ico) !important;
    max-width: var(--mc-ico) !important;
    height: var(--mc-ico) !important;
    min-height: var(--mc-ico) !important;
    max-height: var(--mc-ico) !important;
    padding: 0 !important;
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
</style>
""", unsafe_allow_html=True)

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
    st.session_state["mathicap_page"] = "Accueil"
    st.session_state["afficher_series"] = False
    st.query_params["vue"] = "accueil"


def _mathicap_ouvrir_icone(vue):
    """Ouvre une rubrique sans effacer la série en cours ni la connexion."""
    st.query_params["vue"] = vue


def _mathicap_ouvrir_chapitre_recherche(chapitre):
    """Depuis la recherche, ouvre le chapitre réellement disponible."""
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


# En-tête : bloc logo/slogan à gauche, profil à droite
col_logo, col_profil = st.columns(
    [3, 1],
    vertical_alignment="top",
    gap="small",
    wrap=True,
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
        help="Revenir à l'accueil MathiCap",
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
        _svg_recherche = (
            _icone_svg_debut
            + '<circle cx="11" cy="11" r="6.5"/>'
            + '<path d="M16 16l5 5"/></svg>'
        )
        _svg_notifications = (
            _icone_svg_debut
            + '<path d="M6 16v-5a6 6 0 0 1 12 0v5l1.5 2h-15z"/>'
            + '<path d="M10 20.5a2 2 0 0 0 4 0"/></svg>'
        )
        _recherche_b64 = base64.b64encode(_svg_recherche.encode()).decode()
        _notifications_b64 = base64.b64encode(_svg_notifications.encode()).decode()
        st.html(
            f"""<style>
            .st-key-mathicap_recherche_clic button::before {{
                background-image: url("data:image/svg+xml;base64,{_recherche_b64}") !important;
            }}
            .st-key-mathicap_notifications_clic button::before {{
                background-image: url("data:image/svg+xml;base64,{_notifications_b64}") !important;
            }}
            </style>"""
        )
        # La zone d'espacement conserve la position de Connecté/Déconnexion.
        st.html('<div class="mathicap-espace-icones" aria-hidden="true"></div>')
        st.button(
            "Rechercher",
            key="mathicap_recherche_clic",
            help="Rechercher un chapitre ou une notion",
            on_click=_mathicap_ouvrir_icone,
            args=("recherche",),
        )
        st.button(
            "Notifications",
            key="mathicap_notifications_clic",
            help="Accéder aux notifications",
            on_click=_mathicap_ouvrir_icone,
            args=("notifications",),
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
        if st.button(
            "Ouvrir mon profil",
            key="mathicap_avatar_clic",
            disabled=not est_connecte,
            help="Accéder à mon profil",
        ):
            st.query_params["vue"] = "profil"
            st.rerun()
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


if est_connecte and st.query_params.get("vue") == "profil":
    st.subheader("Mon profil")
    st.markdown("### Mes informations personnelles")

    identifiant_eleve = st.session_state["eleve_id"]
    email_eleve = None
    pseudo_eleve = ""
    date_inscription = None
    profil_charge = False

    # Récupérer les informations du compte existant
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

    # Classe et date d'inscription
    classe_eleve = st.session_state.get("mathicap_classe")

    if date_inscription:
        date_affichee = date_inscription.strftime("%d/%m/%Y")
    else:
        date_affichee = "Information non disponible"

    # Affichage homogène, sans lien e-mail cliquable
    st.html(
        '<div style="line-height: 1.9;">'
        f'<div><strong>Adresse e-mail :</strong> '
        f'{escape(email_eleve or "Information non disponible")}</div>'
        f'<div><strong>Pseudo :</strong> '
        f'{escape(pseudo_eleve or "Non renseigné")}</div>'
        f'<div><strong>Ma classe :</strong> '
        f'{escape(classe_eleve or "Non définie")}</div>'
        f'<div><strong>Date d’inscription :</strong> '
        f'{escape(date_affichee)}</div>'
        '</div>'
    )

    # Personnalisation de l'avatar, propre au compte de chaque élève.
    st.markdown("### Mon avatar")
    if st.session_state.pop("mathicap_avatar_sauve", False):
        st.success("Avatar enregistré. Il sera retrouvé sur tes appareils.")

    avatar_type = st.session_state.get("mathicap_avatar_type", "defaut")
    avatar_choix = st.session_state.get("mathicap_avatar_choix", "")
    avatar_fichier = st.session_state.get("mathicap_avatar_fichier", "")
    if avatar_type == "galerie" and avatar_choix in AVATARS_MATHICAP:
        emoji_apercu, nom_apercu, fond_apercu = AVATARS_MATHICAP[avatar_choix]
        st.html(
            f'<div role="img" aria-label="Avatar {escape(nom_apercu)}" '
            'style="width:80px;height:80px;border-radius:50%;'
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
                'style="width:80px;height:80px;border-radius:50%;'
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
                'style="width:80px;height:80px;border-radius:50%;'
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
        st.info("Connecte-toi à ton profil pour personnaliser l'avatar.")

    # Confirmation après enregistrement
    if st.session_state.pop("mathicap_pseudo_sauve", False):
        st.success("Pseudo enregistré avec succès.")

    # Modifier le pseudo sans toucher aux autres informations
    if profil_charge:
        with st.expander("Modifier mon pseudo"):
            with st.form("mathicap_formulaire_pseudo"):
                nouveau_pseudo = st.text_input(
                    "Nouveau pseudo",
                    value=pseudo_eleve,
                    max_chars=30,
                    help="Facultatif. Laisse vide pour retirer ton pseudo."
                )

                enregistrer_pseudo = st.form_submit_button("Enregistrer")

            if enregistrer_pseudo:
                nouveau_pseudo = nouveau_pseudo.strip()

                if nouveau_pseudo == pseudo_eleve.strip():
                    st.info("Aucune modification à enregistrer.")

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
                        
    st.markdown("### Mes activités")
    series_profil = None

    try:
        resultat_series = (
            supabase_privee.table("series_exercices")
            .select("id, exercices, reponses")
            .eq("eleve_id", identifiant_eleve)
            .execute()
        )

        series_profil = resultat_series.data or []

        total_series = len(series_profil)
        series_avec_reponses = sum(
            1 for serie in series_profil
            if serie.get("reponses")
        )

        col_series, col_reponses, _ = st.columns([2, 2, 1], gap="small")

        with col_series:
            st.metric("Séries sauvegardées", total_series)

        with col_reponses:
            st.metric("Séries avec réponses", series_avec_reponses)

    except Exception:
        st.info("Impossible de charger les statistiques pour le moment.")

    st.caption(
        "Ces chiffres représentent les séries encore sauvegardées sur ton compte."
    )

    st.markdown("### Ma progression")
    if series_profil is None:
        st.info("La progression est momentanément indisponible.")
    else:
        statistiques = _mathicap_statistiques_progression(series_profil)
        col_exercices, col_saisies, _ = st.columns([2, 2, 1], gap="small")

        with col_exercices:
            st.metric(
                "Exercices avec réponse",
                f"{statistiques['exercices_avec_reponse']} "
                f"/ {statistiques['exercices_total']}",
            )
        with col_saisies:
            st.metric(
                "Réponses renseignées",
                statistiques["reponses_renseignees"],
            )

        st.caption(
            "Un exercice est compté dès qu'au moins une réponse est "
            "enregistrée. Cela ne signifie pas qu'il est terminé ou réussi."
        )

        if statistiques["questions_verifiees"]:
            with st.container(key="mathicap_score_corrections"):
                st.metric(
                    "Résultats des corrections enregistrées",
                    f"{statistiques['bonnes_verifiees']} bonnes réponses "
                    f"/ {statistiques['questions_verifiees']}",
                )
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

        with st.expander("Progression par chapitre et par niveau"):
            par_chapitre = statistiques["par_chapitre"]
            par_niveau = statistiques["par_niveau"]
            if not par_chapitre and not par_niveau:
                st.info(
                    "Les anciennes séries ne contiennent pas de chapitre "
                    "ni de niveau enregistrés. Ce suivi apparaîtra "
                    "avec les nouvelles séries."
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

    if st.button(
        "Voir mes séries enregistrées",
        key="mathicap_profil_mes_series"
    ):
        st.session_state["mathicap_page"] = "Mes séries"
        st.session_state["afficher_series"] = True
        st.query_params["vue"] = "accueil"
        st.rerun()
    if st.button(
        "Retour à l'accueil",
        key="mathicap_retour_accueil"
    ):
        st.session_state["mathicap_page"] = "Accueil"
        st.query_params["vue"] = "accueil"
        st.rerun()


# Avant connexion seulement : formulaire compact, sous l'en-tête.
if not est_connecte:
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
                                "pour confirmer ton compte."
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
                        enregistrer_jeton_navigateur(jeton_persistant)
                        st.session_state["vider_champs_connexion"] = True
                        time.sleep(1.5)
                        st.rerun()  
                    else:
                        st.error("Connexion impossible.")
                except Exception:
                    st.error("Une erreur est survenue lors de la connexion.")
# Rubriques accessibles depuis les icônes de l'en-tête.
# La page active est gardée dans l'URL : une actualisation y revient.
vue_icone = st.query_params.get("vue")
if vue_icone == "recherche":
    st.subheader("Recherche")
    st.caption("Chapitres et notions de 5e actuellement répertoriés dans MathiCap.")
    recherche = st.text_input(
        "Rechercher un chapitre ou une notion",
        placeholder="Ex. fractions, distributivité, triangles…",
        key="mathicap_recherche_texte",
    )
    if recherche.strip():
        terme = _mathicap_texte_recherche(recherche.strip())
        trouves = [
            (nom, [notion for notion in notions if terme in _mathicap_texte_recherche(notion)])
            for nom, notions in CHAPITRES_MATHICAP.items()
            if terme in _mathicap_texte_recherche(nom)
            or any(terme in _mathicap_texte_recherche(n) for n in notions)
        ]
        if trouves:
            st.caption(f"{len(trouves)} chapitre(s) trouvé(s).")
            for indice, (nom, notions) in enumerate(trouves):
                col_detail, col_ouvrir = st.columns([3, 1], vertical_alignment="center")
                with col_detail:
                    st.markdown(f"**{nom}**")
                    if notions:
                        st.caption("Notions correspondantes : " + ", ".join(notions))
                with col_ouvrir:
                    st.button(
                        "Ouvrir",
                        key=f"mathicap_recherche_ouvrir_{indice}",
                        on_click=_mathicap_ouvrir_chapitre_recherche,
                        args=(nom,),
                    )
        else:
            st.info("Aucun chapitre ni aucune notion ne correspond à ta recherche.")
    else:
        st.info("Entre un mot pour trouver un chapitre ou une notion.")
    st.button(
        "← Accueil",
        key="mathicap_recherche_retour",
        on_click=_mathicap_retour_accueil_logo,
    )
    st.stop()

if vue_icone == "notifications":
    st.subheader("Notifications")
    if est_connecte:
        st.info("Aucune notification pour le moment.")
        st.caption("Les notifications seront disponibles lorsqu'un service de notification sera activé dans MathiCap.")
    else:
        st.info("Connecte-toi pour accéder à tes notifications.")
    st.button(
        "← Accueil",
        key="mathicap_notifications_retour",
        on_click=_mathicap_retour_accueil_logo,
    )
    st.stop()

# Nouvelle interface MathiCap Collège
if est_connecte and st.query_params.get("vue") == "profil":
    st.stop()

# Une série ouverte depuis « Mes séries » s'affiche dans « Exercices ».
# La navigation est préparée ici, avant la création du widget de menu.
if st.session_state.pop("_mathicap_ouvrir_serie", False):
    st.session_state["mathicap_page"] = "Exercices"
    st.session_state["afficher_series"] = False

page_mathicap = afficher_interface_mathicap()

if page_mathicap == "Exercices":
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

if page_mathicap == "Mes séries" and st.session_state.get("eleve_id"):
    # La rubrique « Mes séries » ouvre directement la liste enregistrée.
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
                col_coche, col_contenu = st.columns(
                    [1.5, 8.5],
                    gap="small",
                    vertical_alignment="center"
                )

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
                     st.session_state["_mathicap_ouvrir_serie"] = True
                     st.rerun()

    except Exception:
        st.error("Impossible de récupérer tes exercices.")

# Ne jamais afficher le générateur au-dessous de la liste des séries.
if page_mathicap == "Mes séries":
    st.stop()

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
        # Mémoriser le chapitre et le niveau pour les nouveaux suivis.
        # Les anciennes séries restent lisibles sans ces métadonnées.
        for exercice in exercices:
            if isinstance(exercice, dict):
                exercice.setdefault("mathicap_chapitre", chapitre)
                exercice.setdefault("mathicap_niveau", niveau_reel)

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
                st.write(exercice["enonce"])

    
            if exercice.get("reponse_attendue") is not None:  
                col_texte, col_saisie, _ = st.columns(
                    [1.3, 1.2, 4.5],
                    gap="small",
                    vertical_alignment="center"
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
                        [1.2, 1.2, 4.6],
                        gap="small"
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
                            col_calcul, col_reponse, _ = st.columns(
                                [2.1, 1.2, 3.7],
                                gap="small",
                                vertical_alignment="center"
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
                            col_texte, col_saisie, _ = st.columns(
                                [2.4, 1.2, 3.4],
                                gap="small",
                                vertical_alignment="center"
                            )

                            with col_texte:
                                st.write(etiquette)

                            with col_saisie:
                                st.text_input(
                                    etiquette,
                                    label_visibility="collapsed",
                                    placeholder="Réponse",
                                    key=cle,
                                    on_change=enregistrer_reponses_banque_auto,
                                    args=(numero,)
                                )

                    elif champ["type"] == "choix":
                        col_texte, col_saisie, _ = st.columns(
                            [2.4, 1.2, 3.4],
                            gap="small",
                            vertical_alignment="center"
                        )

                        with col_texte:
                            st.write(etiquette)

                        with col_saisie:
                            st.selectbox(
                                etiquette,
                                ["Choisir..."] + champ["options"],
                                label_visibility="collapsed",
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
            
