"""Interface MathiCap Collège — étape 1.

Cette interface ne modifie ni les générateurs d'exercices ni Supabase.
Intégration : appeler afficher_interface_mathicap() dans app.py,
APRÈS le bloc de connexion et AVANT les sélecteurs de chapitre.
"""

from pathlib import Path

import streamlit as st


CLASSES = ("6e", "5e", "4e", "3e")
PAGES = (
    "Accueil",
    "Parcours conseillé",
    "Cours",
    "QCM",
    "Exercices",
    "Fiches de révision",
    "Évaluations",
    "Mon Prof IA",
    "Mes séries",
    "Mon espace",
)

LOGO = Path(__file__).with_name("mathicap_logo.png")


def _aller_vers(page: str) -> None:
    """Callback exécuté avant le prochain rendu des widgets Streamlit."""
    st.session_state["mathicap_page"] = page
    if page == "Mes séries":
        st.session_state["afficher_series"] = True
    elif page == "Exercices":
        st.session_state["afficher_series"] = False


def _styles() -> None:
    st.markdown(
        """
        <style>
        .mathicap-hero {
            background: linear-gradient(112deg, #eaf4ff 0%, #f3f9ff 67%, #fff6e9 100%);
            border: 1px solid #dceafe;
            border-radius: 18px;
            padding: 26px 26px 17px;
            margin: 10px 0 12px;
        }
        .mathicap-hero h1 {
            color: #092c63;
            font-size: clamp(1.5rem, 3.6vw, 2.6rem);
            line-height: 1.15;
            margin: 0 0 10px;
        }
        .mathicap-hero p {
            color: #42638c;
            font-size: 1.05rem;
            margin: 0 0 8px;
        }
        .mathicap-section-heading {
            color: #092c63;
            font-size: 1.13rem;
            font-weight: 750;
            margin: 15px 0 10px;
        }
        .mathicap-note {
            color: #48627f;
            font-size: 0.92rem;
        }
                .mathicap-slogan {
            font-size: 1.28rem;
            font-weight: 700;
            line-height: 1.35;
            margin: 12px 0 4px 0;
            background: linear-gradient(90deg, #0b3d91 0%, #1f7ae0 55%, #f3a11a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 0.3px;
        }

        .mathicap-slogan span {
            -webkit-text-fill-color: initial;
            color: #f3a11a;
            font-weight: 800;
            padding: 0 4px;
        }

        @media (max-width: 640px) {
            .mathicap-slogan {
                font-size: 0.82rem;
                margin: 10px 0 2px 0;
            }
        }
        /* Grille des six activités */
        .st-key-mathicap_cartes [data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
            gap: 12px !important;
        }

        .st-key-mathicap_cartes [data-testid="stColumn"] {
            width: 100% !important;
            min-width: 0 !important;
            flex: initial !important;
        }

        .mathicap-card-icon {
            font-size: 1.5rem;
            margin-bottom: 6px;
        }

        .mathicap-card-title {
            font-weight: 700;
            font-size: 0.95rem;
            line-height: 1.25;
            min-height: 2.4em;
        }

        .mathicap-card-desc {
            font-size: 0.82rem;
            color: #64748b;
            line-height: 1.35;
            min-height: 2.7em;
            margin: 7px 0;
        }

        @media (max-width: 640px) {
            .st-key-mathicap_cartes [data-testid="stHorizontalBlock"] {
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                gap: 8px !important;
            }

            .mathicap-card-title {
                font-size: 0.85rem;
            }

            .mathicap-card-desc {
                font-size: 0.75rem;
            }
        }
        /* Chaque carte est un bouton entier */
        .st-key-mathicap_cartes button {
            width: 100%;
            min-height: 155px;
            padding: 16px;
            border: 1px solid #dbe3ef;
            border-radius: 14px;
            background: #ffffff;
            color: #092c63;
            text-align: left;
            align-items: flex-start;
            justify-content: flex-start;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03);
            transition: background 0.2s, border-color 0.2s;
        }

        .st-key-mathicap_cartes button p {
            white-space: pre-line;
            line-height: 1.5;
            font-size: 0.92rem;
        }

        .st-key-mathicap_cartes button:hover {
            background: #edf5ff;
            border-color: #3182ed;
        }

        .st-key-mathicap_cartes button:focus-visible {
            outline: 3px solid #3182ed;
            outline-offset: 2px;
        }

        @media (max-width: 640px) {
            .st-key-mathicap_cartes button {
                min-height: 165px;
                padding: 12px;
            }

            .st-key-mathicap_cartes button p {
                font-size: 0.82rem;
            }
        }
        /* Logo et slogan rapprochés sur smartphone */
        @media (max-width: 640px) {

            .st-key-mathicap_logo_principal [data-testid="stImage"],
            .st-key-mathicap_logo_principal img {
                width: 120px !important;
                max-width: 120px !important;
                height: auto !important;
            }

            .mathicap-slogan {
                font-size: 0.82rem;
                margin: 0 0 6px !important;
            }
        }
        
        </style>
        """,
        unsafe_allow_html=True,
    )

def _accueil() -> None:
    st.markdown(
        """
        <div class="mathicap-hero">
          <h1>Bienvenue sur MathiCap Collège !</h1>
          <p>Apprends les mathématiques clairement et progresse pas à pas, à ton rythme.</p>
          <span class="mathicap-note">Cours · QCM · Exercices · Révisions · Évaluations</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    a, b = st.columns(2)
    with a:
        st.button(
            "Commencer les exercices →",
            key="mathicap_commencer",
            type="primary",
            use_container_width=True,
            on_click=_aller_vers,
            args=("Exercices",),
        )
    with b:
        st.button(
            "Reprendre ma progression",
            key="mathicap_reprendre",
            use_container_width=True,
            disabled=not bool(st.session_state.get("eleve_id")),
            on_click=_aller_vers,
            args=("Exercices",),
            help="Ouvre la zone d'exercices et la dernière série récupérable.",
        )

    with st.container(border=True):
        col1, col2 = st.columns([3, 1], vertical_alignment="center")
        with col1:
            st.markdown("**🎯 Parcours conseillé — chapitre 1 : Opérations**")
            st.write(
                "Commence par le cours, vérifie ta compréhension puis "
                "entraîne-toi avec les neuf niveaux progressifs."
            )
            st.caption(
                "Parcours initial proposé à tous ; la personnalisation selon "
                "les résultats sera ajoutée dans une prochaine étape."
            )
        with col2:
            st.button(
                "Voir le parcours →",
                key="mathicap_voir_parcours",
                use_container_width=True,
                on_click=_aller_vers,
                args=("Parcours conseillé",),
            )

    st.markdown('<div class="mathicap-section-heading">Je choisis mon activité</div>', unsafe_allow_html=True)

    activites = (
        ("📖", "Cours & points à retenir", "Découvrir les méthodes et les exemples.", "Cours"),
        ("✅", "QCM rapides", "Vérifier la compréhension du cours.", "QCM"),
        ("✏️", "Exercices progressifs", "S'entraîner du niveau 1 au niveau 9.", "Exercices"),
        ("⏱️", "Évaluations", "Se préparer aux contrôles.", "Évaluations"),
        ("📄", "Fiches de révision", "Retenir l'essentiel du chapitre.", "Fiches de révision"),
        ("💡", "Mon Prof IA", "Obtenir une explication ou un indice.", "Mon Prof IA"),
    )
    
    # Six cartes : 3 par ligne sur PC, 2 sur smartphone
        # Six cartes entièrement cliquables
    with st.container(key="mathicap_cartes"):
        colonnes = st.columns(6, gap="small")

        for colonne, (icone, titre, description, page) in zip(
            colonnes, activites
        ):
            with colonne:
                st.button(
                    f"{icone}  **{titre}**  \n{description}",
                    key=f"mathicap_activite_{page}",
                    width="stretch",
                    wrap=True,
                    on_click=_aller_vers,
                    args=(page,),
                )

    # Mes progrès : conserver cette partie

    with st.container(border=True):
        st.markdown("**📊 Mes progrès**")
        st.caption(
            "Le suivi par compétence sera affiché ici dès que les résultats "
            "des QCM et des exercices auront été reliés au tableau de bord."
        )
        if st.session_state.get("eleve_id"):
            st.button(
                "Retrouver mes séries sauvegardées →",
                key="mathicap_mes_series_accueil",
                on_click=_aller_vers,
                args=("Mes séries",),
            )
        else:
            st.info("Connecte-toi pour enregistrer et reprendre tes séries d'exercices.")


def _page_en_preparation(page: str) -> None:
    st.title(page)
    if page == "Parcours conseillé":
        st.subheader("Première proposition : chapitre 1 — Opérations")
        st.markdown(
            "1. Lire le cours et ses points à retenir.\n"
            "2. Répondre à un QCM de compréhension.\n"
            "3. Faire quelques exercices progressifs.\n"
            "4. Consulter la fiche de révision.\n"
            "5. Passer une évaluation lorsque tu es prêt."
        )
        st.caption("Les étapes non encore développées seront disponibles progressivement.")
        st.button(
            "Commencer avec les exercices existants",
            on_click=_aller_vers,
            args=("Exercices",),
        )
    elif page == "Mon Prof IA":
        st.info("L'assistant IA n'est pas encore connecté. Cette rubrique sera développée et testée séparément.")
    else:
        st.info(f"La rubrique « {page} » est en préparation. Les exercices existants restent accessibles.")
    st.button("Retour à l'accueil", on_click=_aller_vers, args=("Accueil",))


def afficher_interface_mathicap() -> str:
    """Affiche la navigation et retourne 'Exercices' ou 'Mes séries'.

    Pour toute autre page, le contenu est affiché puis st.stop() empêche
    l'ancien générateur d'exercices de se lancer en arrière-plan.
    """
    _styles()
    if "mathicap_page" not in st.session_state:
        st.session_state["mathicap_page"] = "Accueil"
    if "mathicap_classe" not in st.session_state:
        st.session_state["mathicap_classe"] = "5e"

    with st.sidebar:
        if LOGO.is_file():
            st.image(str(LOGO), width=120)
        else:
            st.title("MathiCap Collège")
        st.divider()
        page = st.radio("Navigation", PAGES, key="mathicap_page")
        st.divider()
        st.caption("MathiCap Collège · Programme en développement")

    
    ancienne_page = st.session_state.get("_mathicap_page_precedente")

    if ancienne_page != page:
        if page == "Exercices":
            st.session_state["afficher_series"] = False
        elif page == "Mes séries":
            st.session_state["afficher_series"] = True

        st.session_state["_mathicap_page_precedente"] = page

    # Bandeau des classes
    st.markdown("**Ma classe**")

    couleurs = {
        "6e": ("#DCEBFF", "#1458B8", "#2678EF"),
        "5e": ("#DDF6E8", "#116A42", "#21A46A"),
        "4e": ("#FFF0D8", "#985300", "#F0981B"),
        "3e": ("#EFE2FF", "#6733A8", "#8752D6"),
    }

    def choisir_classe(nouvelle_classe):
        st.session_state["mathicap_classe"] = nouvelle_classe

    classe_active = st.session_state["mathicap_classe"]

    # Construire les styles une seule fois
    regles_css = []

    for nom, (fond, texte, accent) in couleurs.items():
        selectionnee = nom == classe_active

        fond_bouton = accent if selectionnee else fond
        texte_bouton = "#FFFFFF" if selectionnee else texte
        epaisseur = "3px" if selectionnee else "1px"

        regles_css.append(
            f"""
            .st-key-mathicap_bouton_{nom} button {{
                background-color: {fond_bouton} !important;
                color: {texte_bouton} !important;
                border: {epaisseur} solid {accent} !important;
                border-radius: 10px !important;
                min-height: 56px !important;
                font-weight: 700 !important;
                font-size: 1.05rem !important;
            }}
            """
        )

    # Adaptation mobile : quatre boutons sur une ligne
    regles_css.append(
        """
        @media (max-width: 640px) {
            .st-key-mathicap_ligne_classes
            [data-testid="stHorizontalBlock"] {
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                gap: 6px !important;
            }

            .st-key-mathicap_ligne_classes
            [data-testid="stColumn"] {
                min-width: 0 !important;
                width: 25% !important;
                flex: 1 1 0% !important;
            }

            .st-key-mathicap_ligne_classes button {
                min-height: 48px !important;
                padding: 6px 4px !important;
            }
        }
        """
    )

    # Injecter le CSS une seule fois, sans bloc visible
    st.html("<style>" + "\n".join(regles_css) + "</style>")

    with st.container(key="mathicap_ligne_classes"):
        colonnes_classes = st.columns(4, gap="small")

        for colonne, nom in zip(colonnes_classes, couleurs):
            with colonne:
                st.button(
                    nom,
                    key=f"mathicap_bouton_{nom}",
                    width="stretch",
                    on_click=choisir_classe,
                    args=(nom,),
                )

    classe = st.session_state["mathicap_classe"]

    if classe != "5e":
        st.title(f"MathiCap Collège — {classe}")
        st.info(
            f"Le programme de {classe} sera développé progressivement. "
            "Le chapitre 1 actuellement opérationnel appartient à la classe de 5e."
        )
        st.stop()

    if page == "Accueil":
        _accueil()
        st.stop()

    if page not in ("Exercices", "Mes séries"):
        _page_en_preparation(page)
        st.stop()

    if page == "Mes séries":
        st.session_state["afficher_series"] = True
        st.header("Mes séries d'exercices")
        if not st.session_state.get("eleve_id"):
            st.info("Connecte-toi pour accéder aux séries enregistrées.")
            st.stop()
    else:
        st.header("Exercices de mathématiques")

    return page
