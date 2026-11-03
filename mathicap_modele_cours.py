"""Prototype autonome MathiCap — modèle de page de cours (5e).

Aucune connexion à Supabase, aucune modification de app.py,
aucune donnée élève enregistrée. À tester sur une branche GitHub dédiée.
"""

from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Prototype — Cours MathiCap",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1080px;
        padding-top: clamp(1rem, 3vw, 2rem);
        padding-bottom: 3rem;
    }
    .mc-hero {
        padding: clamp(1.1rem, 3vw, 2rem);
        border: 1px solid #dbe6f4;
        border-radius: 18px;
        background: linear-gradient(110deg, #eaf4ff 0%, #f8fbff 65%, #fff5e6 100%);
        margin: 0 0 1rem 0;
    }
    .mc-eyebrow {color: #20589b; font-size: .85rem; font-weight: 700; letter-spacing: .03em;}
    .mc-hero h1 {font-size: clamp(1.7rem, 4vw, 2.5rem); line-height: 1.2; color: #0e3266; margin: .45rem 0;}
    .mc-hero p {color: #395576; margin: .3rem 0 0; font-size: 1rem;}
    .mc-step {
        border-left: 4px solid #2683d7; background: #f1f8ff;
        padding: .85rem 1.1rem; border-radius: 0 12px 12px 0;
        margin: .5rem 0;
    }
    .mc-step strong {color: #174d8d;}
    .mc-note {
        padding: .9rem 1rem; background: #fff9e9;
        border: 1px solid #f3dca9; border-radius: 12px;
    }
    .mc-muted {color: #60758d; font-size: .92rem;}
    @media (max-width: 620px) {
        .block-container {padding-left: 1rem; padding-right: 1rem;}
        .mc-hero {border-radius: 14px;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)

logo = Path(__file__).with_name("mathicap_logo.png")
if logo.is_file():
    st.image(str(logo), width=170)
else:
    st.markdown("**MathiCap Collège**")

st.markdown(
    """
    <section class="mc-hero">
        <div class="mc-eyebrow">MATHÉMATIQUES · 5e · CHAPITRE 1</div>
        <h1>La distributivité simple</h1>
        <p>Un mini-cours clair, des exemples pas à pas et un exercice pour comprendre.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.caption("Prototype visuel indépendant · aucune sauvegarde de réponses ou de compte")

cours, exemple, pratique = st.tabs(["📖 Je comprends", "🧩 Exemple guidé", "✏️ Je m'entraîne"])

with cours:
    st.subheader("La règle à retenir")
    st.write("Multiplier une somme, c'est multiplier chaque terme de la somme, puis additionner les résultats.")
    st.latex(r"a\times(b+c)=a\times b+a\times c")
    st.markdown(
        '<div class="mc-note"><strong>Astuce :</strong> dessine deux flèches partant du facteur devant la parenthèse, une vers chaque terme.</div>',
        unsafe_allow_html=True,
    )
    st.write("")
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        with st.container(border=True):
            st.markdown("**Addition dans les parenthèses**")
            st.latex(r"4(5+3) = 4\times 5 + 4\times 3")
    with col2:
        with st.container(border=True):
            st.markdown("**Soustraction dans les parenthèses**")
            st.latex(r"4(5-3) = 4\times 5 - 4\times 3")

with exemple:
    st.subheader("Exemple : calculer 3 × (7 + 2)")
    st.markdown('<div class="mc-step"><strong>Étape 1 :</strong> on distribue le facteur 3.</div>', unsafe_allow_html=True)
    st.latex(r"3\times(7+2)=3\times7+3\times2")
    st.markdown('<div class="mc-step"><strong>Étape 2 :</strong> on calcule les deux produits.</div>', unsafe_allow_html=True)
    st.latex(r"=21+6")
    st.markdown('<div class="mc-step"><strong>Étape 3 :</strong> on additionne.</div>', unsafe_allow_html=True)
    st.latex(r"=27")
    st.success("Résultat : 27")

with pratique:
    st.subheader("À toi de jouer")
    st.write("Calcule en utilisant la distributivité :")
    st.latex(r"5\times(4+6)")
    with st.form("mathicap_demo_reponse", clear_on_submit=False):
        rep = st.text_input("Ta réponse", placeholder="Écris le résultat", max_chars=15)
        verifier = st.form_submit_button("Vérifier ma réponse")
    if verifier:
        propre = rep.strip().replace(" ", "").replace(",", ".")
        if not propre:
            st.warning("Saisis une réponse avant de vérifier.")
        elif propre in {"50", "50.0"}:
            st.success("Bonne réponse : 5 × 4 + 5 × 6 = 20 + 30 = 50.")
        else:
            st.info("Reprends le calcul : 5 × 4 + 5 × 6 = 20 + 30.")
    with st.expander("Voir la correction détaillée"):
        st.latex(r"5\times(4+6) = 5\times4 + 5\times6 = 20+30 = 50")

st.divider()
st.markdown(
    '<p class="mc-muted">Ce fichier sert uniquement à évaluer le modèle de page. '
    'Les cours existants, les séries, les bilans et Supabase ne sont pas modifiés.</p>',
    unsafe_allow_html=True,
)
