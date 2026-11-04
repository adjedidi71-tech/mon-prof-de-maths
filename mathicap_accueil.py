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
            .mathicap-marque {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 6px;
        }

        .mathicap-marque img {
            display: block;
            width: 260px;
            max-width: 100%;
            height: auto;
        }

        .mathicap-marque .mathicap-slogan {
            margin: 0 !important;
        }

        @media (max-width: 640px) {
            .mathicap-marque img {
                width: 120px;
            }
        }
        /* Espacement de l'accueil sur smartphone */
        @media (max-width: 640px) {

            /* Réduire l'espace blanc en haut de page */
            .stMainBlockContainer {
                padding-top: 2.75rem !important;
            }

            /* Séparer le slogan du compte élève */
            .mathicap-marque {
                padding-bottom: 14px !important;
            }
        }
        /* Statut de connexion compact */
        .mathicap-statut {
            color: #16834A;
            font-weight: 700;
            font-size: 0.92rem;
            white-space: nowrap;
            margin-bottom: 8px;
        }

        /* Positionner le profil à droite */
        div[data-testid="stColumn"]:has(.mathicap-statut) {
            text-align: right;
        }

        div[data-testid="stColumn"]:has(.mathicap-statut)
        div[data-testid="stButton"] {
            display: flex;
            justify-content: flex-end;
        }

        @media (max-width: 640px) {

            .mathicap-statut {
                font-size: 0.78rem;
            }

            div[data-testid="stColumn"]:has(.mathicap-statut)
            button {
                font-size: 0.72rem !important;
                padding: 6px 8px !important;
            }

            .mathicap-marque .mathicap-slogan {
                font-size: 0.82rem;
                white-space: nowrap;
            }
        }


        /* ===== Tableau de bord MathiCap : couleurs et animations douces ===== */
        .mathicap-hero {
            position: relative;
            isolation: isolate;
            overflow: hidden;
            background: linear-gradient(118deg, #dceeff 0%, #eef7ff 48%, #fff0d5 100%) !important;
            border: 1px solid #bddcf6 !important;
            border-radius: 24px !important;
            padding: clamp(20px, 3.3vw, 36px) !important;
            box-shadow: 0 8px 24px rgba(13, 66, 124, .06);
        }
        .mathicap-hero::before {
            content: "";
            position: absolute;
            z-index: -1;
            width: 300px;
            height: 300px;
            top: -175px;
            right: -55px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255,188,65,.27), rgba(255,188,65,0) 72%);
            pointer-events: none;
        }
        .mathicap-hero h1 { max-width: 85%; font-weight: 800; }
        .mathicap-hero p { max-width: 70ch; }
        .mathicap-hero .mathicap-hero-motifs {
            position: absolute;
            top: 20px;
            right: 22px;
            color: #1f64ac;
            opacity: .57;
            font-weight: 900;
            letter-spacing: .35rem;
            font-size: clamp(1.15rem, 2.8vw, 2.3rem);
            transform: rotate(-9deg);
            pointer-events: none;
            animation: mathicap-flotte 6s ease-in-out infinite;
        }
        .mathicap-mini-label {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            border-radius: 50px;
            color: #16457d;
            background: rgba(255,255,255,.72);
            font-weight: 700;
            font-size: .82rem;
            margin-bottom: 10px;
        }
        .mathicap-dashboard { margin: 12px 0 22px; max-width: 1000px; }
        .mathicap-dashboard-grille {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
            margin: 12px 0;
        }
        .mathicap-stat-carte {
            border: 1px solid #d4e3f4;
            border-radius: 18px;
            padding: 16px 18px;
            background: #f0f7ff;
            color: #143e70;
        }
        .mathicap-stat-carte:nth-child(2) {
            background: #f1fbf4;
            border-color: #cce9d6;
            color: #145d40;
        }
        .mathicap-stat-nombre {
            display: block;
            font-size: clamp(1.6rem, 3vw, 2rem);
            font-weight: 850;
            line-height: 1.25;
        }
        .mathicap-stat-intitule { display: block; font-weight: 650; font-size: .9rem; }
        .mathicap-stat-info { display: block; font-size: .75rem; color: #45647c; margin-top: 5px; }
        .mathicap-progression {
            border: 1px solid #e5dcf9;
            border-radius: 17px;
            padding: 14px 18px;
            background: #faf7ff;
            color: #4c3483;
        }
        .mathicap-progression-entete { display: flex; justify-content: space-between; gap: 12px; align-items: center; font-size: .91rem; font-weight: 750; }
        .mathicap-progression-piste {
            width: 100%;
            height: 12px;
            border-radius: 20px;
            overflow: hidden;
            margin: 10px 0 8px;
            background: #e9e1f5;
        }
        .mathicap-progression-remplissage {
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg, #7850d3 0%, #2b8ee8 100%);
            transition: width .7s ease-out;
        }
        .mathicap-progression-note { font-size: .79rem; color: #6c5a89; }
        .st-key-mathicap_cartes [data-testid="stColumn"] button {
            position: relative;
            transition: transform .18s ease, background .18s ease, box-shadow .18s ease !important;
            border-radius: 18px !important;
            font-weight: 600 !important;
            min-height: 165px !important;
        }
        .st-key-mathicap_cartes [data-testid="stColumn"]:nth-child(1) button { background: #eaf4ff !important; border-color: #a9d0fb !important; }
        .st-key-mathicap_cartes [data-testid="stColumn"]:nth-child(2) button { background: #ebfaef !important; border-color: #b7e5c7 !important; }
        .st-key-mathicap_cartes [data-testid="stColumn"]:nth-child(3) button { background: #fff4e3 !important; border-color: #ffd69c !important; }
        .st-key-mathicap_cartes [data-testid="stColumn"]:nth-child(4) button { background: #f1eafa !important; border-color: #d5c0f8 !important; }
        .st-key-mathicap_cartes [data-testid="stColumn"]:nth-child(5) button { background: #e7faf9 !important; border-color: #b5e7e4 !important; }
        .st-key-mathicap_cartes [data-testid="stColumn"]:nth-child(6) button { background: #fff0f1 !important; border-color: #f5cad0 !important; }
        .st-key-mathicap_cartes [data-testid="stColumn"] button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 18px rgba(28,59,106,.12) !important;
        }
        .st-key-mathicap_cartes [data-testid="stColumn"] button:focus-visible {
            outline: 3px solid #1a66c9 !important;
            outline-offset: 2px;
        }
        @keyframes mathicap-flotte { 0%,100% {transform: translateY(0) rotate(-9deg)} 50% {transform: translateY(7px) rotate(-5deg)} }
        @media (max-width: 640px) {
            .mathicap-hero h1 { max-width: 100%; padding-right: 20px; }
            .mathicap-hero .mathicap-hero-motifs { right: 9px; top: 7px; font-size: 1.05rem; letter-spacing: .14rem; opacity: .42; }
            .mathicap-hero { padding: 17px !important; }
            .mathicap-stat-carte { padding: 13px 10px; }
            .mathicap-stat-intitule { font-size: .78rem; }
            .mathicap-stat-info { font-size: .7rem; }
            .mathicap-progression { padding: 12px; }
            .st-key-mathicap_cartes [data-testid="stColumn"] button { min-height: 154px !important; }
        }
        @media (prefers-reduced-motion: reduce) {
            .mathicap-hero .mathicap-hero-motifs,
            .st-key-mathicap_cartes [data-testid="stColumn"] button,
            .mathicap-progression-remplissage {
                animation: none !important;
                transition: none !important;
                transform: none !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _accueil() -> None:
    """Accueil visuel ; les données de progression proviennent uniquement des séries enregistrées."""
    from html import escape

    connecte = bool(st.session_state.get("eleve_id"))
    pseudo = st.session_state.get("mathicap_avatar_pseudo", "")
    pseudo = pseudo.strip() if isinstance(pseudo, str) else ""
    salutation = f"Bonjour, {escape(pseudo[:30])} !" if connecte and pseudo else "Bienvenue sur MathiCap !"
    st.markdown(
        f"""
        <section class="mathicap-hero" aria-label="Bienvenue sur MathiCap">
          <span class="mathicap-mini-label">✦ Ton espace de maths</span>
          <div class="mathicap-hero-motifs" aria-hidden="true">π × +</div>
          <h1>{salutation}</h1>
          <p>Explore, essaie, progresse ! Chaque petit pas compte.</p>
          <span class="mathicap-note">Cours · Défis · Exercices · Révisions</span>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if connecte:
        donnees = st.session_state.get("_mathicap_dashboard_donnees")
        if isinstance(donnees, dict) and donnees.get("disponible"):
            nb_series = max(0, int(donnees.get("nb_series", 0)))
            bonnes = max(0, int(donnees.get("bonnes", 0)))
            questions_verifiees = max(0, int(donnees.get("questions_verifiees", 0)))
            repondus = max(0, int(donnees.get("exercices_repondus", 0)))
            total = max(0, int(donnees.get("exercices_total", 0)))
            pourcentage = round(100 * repondus / total) if total else 0
            st.markdown(
                f"""
                <section class="mathicap-dashboard" aria-label="Ton tableau de bord">
                  <div class="mathicap-dashboard-grille">
                    <div class="mathicap-stat-carte">
                      <span class="mathicap-stat-nombre">📚 {nb_series}</span>
                      <span class="mathicap-stat-intitule">Séries enregistrées</span>
                      <span class="mathicap-stat-info">Retrouve ton travail quand tu veux</span>
                    </div>
                    <div class="mathicap-stat-carte">
                      <span class="mathicap-stat-nombre">⭐ {bonnes}</span>
                      <span class="mathicap-stat-intitule">Bonnes réponses vérifiées</span>
                      <span class="mathicap-stat-info">Sur {questions_verifiees} questions vérifiées</span>
                    </div>
                  </div>
                  <div class="mathicap-progression">
                    <div class="mathicap-progression-entete"><span>🎯 Exercices avec réponse</span><span>{repondus} / {total}</span></div>
                    <div class="mathicap-progression-piste" role="progressbar" aria-label="Exercices avec une réponse" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{pourcentage}">
                      <div class="mathicap-progression-remplissage" style="width:{pourcentage}%"></div>
                    </div>
                    <div class="mathicap-progression-note">{pourcentage} % des exercices enregistrés ont au moins une réponse. Ce n'est pas une note de maîtrise.</div>
                  </div>
                </section>
                """, unsafe_allow_html=True,
            )
        else:
            st.caption("Ton tableau de bord sera disponible lorsque tes séries auront été chargées.")
    else:
        st.caption("Connecte-toi pour retrouver tes séries et suivre ta progression.")

    a, b = st.columns(2, gap="small")
    with a:
        st.button(
            "✏️ Commencer mes exercices",
            key="mathicap_commencer",
            width="stretch",
            on_click=_aller_vers,
            args=("Exercices",),
        )
    with b:
        st.button(
            "▶️ Reprendre mes séries",
            key="mathicap_reprendre",
            width="stretch",
            disabled=not connecte,
            on_click=_aller_vers,
            args=("Mes séries",),
            help="Accède aux séries enregistrées sur ton compte.",
        )

    st.markdown('<div class="mathicap-section-heading">🧭 Mon parcours</div>', unsafe_allow_html=True)
    with st.container(border=False):
        st.markdown("**🎯 Parcours conseillé — chapitre 1 : Opérations**")
        st.write("Découvre la méthode, entraîne-toi, puis vérifie tes acquis à ton rythme.")
        st.button(
            "Voir le parcours →", key="mathicap_voir_parcours",
            on_click=_aller_vers, args=("Parcours conseillé",),
        )

    st.markdown('<div class="mathicap-section-heading">✨ Je choisis mon activité</div>', unsafe_allow_html=True)

    activites = (
        ("📖", "Cours & points à retenir", "Comprendre avec des exemples.", "Cours"),
        ("✅", "QCM rapides", "Tester ce que j'ai compris.", "QCM"),
        ("✏️", "Exercices progressifs", "Du niveau 1 au niveau 9.", "Exercices"),
        ("⏱️", "Évaluations", "Me préparer aux contrôles.", "Évaluations"),
        ("📄", "Fiches de révision", "Retrouver l'essentiel.", "Fiches de révision"),
        ("💡", "Mon Prof IA", "Une explication, un indice.", "Mon Prof IA"),
    )
    with st.container(key="mathicap_cartes"):
        colonnes = st.columns(6, gap="small")
        for colonne, (icone, titre, description, page) in zip(colonnes, activites):
            with colonne:
                st.button(
                    f"{icone}  **{titre}**  \n{description}",
                    key=f"mathicap_activite_{page}",
                    width="stretch",
                    wrap=True,
                    on_click=_aller_vers,
                    args=(page,),
                )
    if connecte:
        st.button(
            "📚 Voir toutes mes séries sauvegardées →",
            key="mathicap_mes_series_accueil", on_click=_aller_vers,
            args=("Mes séries",),
        )

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

    if page != "Mes séries":
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
        # Navigation compacte et adaptable au smartphone
        with st.container(horizontal=True, horizontal_alignment="left", gap="small"):
            if st.button(
                "← Mon profil",
                key="mathicap_series_retour_profil",
                disabled=not bool(st.session_state.get("eleve_id"))
            ):
                st.query_params["vue"] = "profil"
                st.rerun()

            st.button(
                "← Accueil",
                key="mathicap_series_retour_accueil",
                on_click=_aller_vers,
                args=("Accueil",)
            )
    
        st.session_state["afficher_series"] = True
        st.header("Mes séries d'exercices")
        if not st.session_state.get("eleve_id"):
            st.info("Connecte-toi pour accéder aux séries enregistrées.")
            st.stop()
    else:
        st.header("Exercices de mathématiques")

    return page
