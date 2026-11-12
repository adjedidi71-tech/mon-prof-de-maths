"""Tableau de diagnostic visuel MathiCap : lecture seule, version 1.

Ne confond jamais réponses sauvegardées a posteriori avec première vérification.
Les tentatives anciennes / partielles / après correction sont exclues du score.
"""

from html import escape
from mathicap_diagnostic import premier_bilan, valeur_renseignee
from mathicap_adaptatif import (analyser_bilan, questions_pedagogiques,
                                conseil_argumente, resumer_questions)


def charger_evenements(client, eleve_id):
    """Lit uniquement les premières actions immuables de cet élève (pagination)."""
    if not eleve_id:
        return []
    sortie = []
    page_size = 400
    for i in range(100):
        lot = (client.table("mathicap_diagnostic_premiers")
               .select("code_reprise,numero_exercice,evenement,complet,bonnes,total,"
                       "reponses_evaluables,chapitre,niveau,enregistre_le")
               .eq("eleve_id", eleve_id)
               .order("enregistre_le", desc=True)
               .range(i * page_size, (i + 1) * page_size - 1)
               .execute().data)
        if not isinstance(lot, list):
            raise RuntimeError("Lecture diagnostique incomplète")
        sortie.extend(lot)
        if len(lot) < page_size:
            return sortie
    raise RuntimeError("Trop d'événements diagnostiques à lire")


def _details_verification(exercice, saisies):
    """Détaille un bilan à l'aide du correcteur PREMIER_BILAN existant.

    Pour les choix avec dépendances, soustrait les points de leurs dépendances
    au bilan du sous-ensemble, sans reproduire la formule de correction.
    """
    if not isinstance(exercice, dict) or not isinstance(saisies, dict):
        return None
    if exercice.get("reponse_attendue") is not None:
        b = premier_bilan(exercice, {"valeur": saisies.get("valeur")})
        return [bool(b["bonnes"])] if b and b["complet"] and b["total"] == 1 else None

    champs = [c for c in (exercice.get("champs_reponse") or [])
              if isinstance(c, dict) and c.get("type") != "texte_libre"]
    if not champs:
        return None
    reponses = {"champs": saisies}
    complet = premier_bilan(exercice, reponses)
    if not complet or not complet["complet"] or complet["total"] != len(champs):
        return None
    par_id = {c.get("id"): c for c in champs if c.get("id")}
    resultat = []
    for champ in champs:
        dependances = [par_id[d] for d in (champ.get("dependances") or [])
                       if d in par_id and d != champ.get("id")]
        # Le correcteur traite les choix dépendants avec leurs réponses liées.
        bloc = premier_bilan({"champs_reponse": [champ, *dependances]}, reponses)
        dep = (premier_bilan({"champs_reponse": dependances}, reponses)
               if dependances else None)
        if bloc is None:
            return None
        points = bloc["bonnes"] - (dep["bonnes"] if dep else 0)
        if points not in (0, 1):
            return None
        resultat.append(bool(points))
    if sum(resultat) != complet["bonnes"]:
        return None
    return resultat


def _etat_redaction_actuelle(exercice, reponses_sauvegardees):
    """Lecture seule : toutes les rédactions sont-elles ACTUELLEMENT renseignées ?

    L'événement immuable ne contient que les champs notables. On ne peut donc
    pas attester que la rédaction était présente lors du premier contrôle.
    None signifie : l'exercice ne comporte aucune rédaction distincte.
    """
    champs = [c for c in (exercice.get("champs_reponse") or [])
              if isinstance(c, dict) and c.get("type") == "texte_libre"]
    if not champs:
        return None
    if not isinstance(reponses_sauvegardees, dict):
        return False
    if reponses_sauvegardees.get("type") != "banque":
        return False
    saisies = reponses_sauvegardees.get("champs")
    if not isinstance(saisies, dict):
        return False
    return all(
        isinstance(saisies.get(c.get("id")), str)
        and valeur_renseignee(saisies.get(c.get("id")))
        for c in champs
    )


def calculer_bilan(series_filtrees, evenements):
    """Sépare répartition par position, chapitres et niveaux ; non évalué != erreur."""
    index = {}
    for fiche in series_filtrees:
        s = fiche.get("serie") or {}
        code = str(s.get("code_reprise") or "").upper()
        if code and isinstance(s.get("exercices"), list):
            index[code] = (s, fiche)
    points = []
    nb_exclus = 0
    for ev in evenements:
        if not isinstance(ev, dict):
            continue
        cle = str(ev.get("code_reprise") or "").upper()
        if cle not in index:
            continue
        if ev.get("evenement") != "verification" or ev.get("complet") is not True:
            nb_exclus += 1
            continue
        s, fiche = index[cle]
        numero = ev.get("numero_exercice")
        if type(numero) is not int or not 1 <= numero <= len(s["exercices"]):
            continue
        exercice = s["exercices"][numero - 1]
        if not isinstance(exercice, dict):
            continue
        bonnes, total = ev.get("bonnes"), ev.get("total")
        if (type(bonnes) is not int or type(total) is not int
                or total < 1 or not 0 <= bonnes <= total):
            continue
        repartition = _details_verification(exercice, ev.get("reponses_evaluables") or {})
        # Préserver les totaux officiels ; exclure du tableau les métadonnées
        # non cohérentes plutôt que présenter des cases trompeuses.
        if repartition is None or len(repartition) != total or sum(repartition) != bonnes:
            nb_exclus += 1
            continue
        niveau = exercice.get("mathicap_niveau")
        chapitre = exercice.get("mathicap_chapitre")
        if type(niveau) is not int or not 1 <= niveau <= 9:
            continue
        questions, texte_libre, numerotation = questions_pedagogiques(
            exercice, repartition
        )
        reponses_actuelles = s.get("reponses") or {}
        if not isinstance(reponses_actuelles, dict):
            reponses_actuelles = {}
        etat_redaction = _etat_redaction_actuelle(
            exercice, reponses_actuelles.get(str(numero))
        )
        points.append({
            "chapitre": chapitre if isinstance(chapitre, str) else "",
            "niveau": niveau, "serie": fiche.get("numero", "?"),
            "numero": numero, "questions": repartition,
            "bonnes": bonnes, "total": total,
            "date": ev.get("enregistre_le") or "",
            # Métadonnées additionnelles pour l'analyse, sans nouvelle
            # écriture Supabase et sans remplacer les scores d'origine.
            "questions_pedagogiques": questions,
            "avec_texte_libre": texte_libre,
            "redaction_actuellement_renseignee": etat_redaction,
            "numero_question_fiable": numerotation,
            "notion": exercice.get("mathicap_partie"),
            "exercice_id": exercice.get("id"),
            "code_reprise": cle, "serie_id": s.get("id"),
            "entrainement_cible": bool(
                exercice.get("mathicap_entrainement_cible_v1")
            ),
        })

    points.sort(key=lambda x: x["date"], reverse=True)
    bonnes = sum(x["bonnes"] for x in points)
    total = sum(x["total"] for x in points)
    # Positions comptées avec leur dénominateur propre : Q5 ne concerne
    # que les exercices comportant au moins cinq questions.
    positions = {}
    for p in points:
        for i, correct in enumerate(p["questions"], 1):
            g = positions.setdefault(i, {"bonnes": 0, "total": 0})
            g["bonnes"] += int(correct)
            g["total"] += 1
    syntheses = [x for x in points if x["niveau"] >= 7 and len(x["questions"]) >= 2]
    reussites_finales = sum(p["questions"][-1] for p in syntheses)
    return {
        "points": points, "bonnes": bonnes, "total": total,
        "positions": positions, "exclus": nb_exclus,
        "finales_total": len(syntheses), "finales_bonnes": reussites_finales,
    }


def _tranches_bilan(nombre, taille=10):
    """Tranches d'affichage uniquement ; les scores utilisent le bilan complet."""
    if type(nombre) is not int or nombre <= 0 or type(taille) is not int or taille <= 0:
        return []
    return [(debut, min(debut + taille, nombre))
            for debut in range(0, nombre, taille)]


def _tranche_choisie(st, eleve_id, points, *, taille=10):
    """Sélection 1–10, 11–20… ; mémorisée dans l'URL, par contexte de filtre.

    Aucune information d'élève ou de réponse n'est placée dans l'URL.
    La sélection n'affecte ni les résultats ni l'analyse pédagogique.
    """
    tranches = _tranches_bilan(len(points), taille)
    if not tranches:
        return [], (0, 0)

    cle = f"mathicap_bilan_tranche_{eleve_id}"
    cle_contexte = "_mc_bilan_tranche_contexte"
    contexte = (
        str(eleve_id),
        str(st.query_params.get("ms_chapitre", "")),
        str(st.query_params.get("ms_niveau", "")),
        str(st.query_params.get("ms_avancement", "")),
    )
    ancien_contexte = st.session_state.get(cle_contexte)
    if ancien_contexte is not None and ancien_contexte != contexte:
        # Changer de filtre ou d'élève : repartir des lignes récentes.
        st.session_state[cle] = 0
        st.query_params.pop("mb_tranche", None)
    st.session_state[cle_contexte] = contexte

    if cle not in st.session_state:
        try:
            numero_url = int(st.query_params.get("mb_tranche", "1")) - 1
        except (TypeError, ValueError):
            numero_url = 0
        st.session_state[cle] = numero_url if 0 <= numero_url < len(tranches) else 0

    if (type(st.session_state.get(cle)) is not int
            or not 0 <= st.session_state[cle] < len(tranches)):
        st.session_state[cle] = 0
        st.query_params.pop("mb_tranche", None)

    def memoriser_tranche():
        st.query_params["mb_tranche"] = str(st.session_state[cle] + 1)
        st.query_params["vue"] = "series"

    if len(tranches) > 1:
        st.selectbox(
            "Exercices affichés", list(range(len(tranches))),
            format_func=lambda i: f"{tranches[i][0] + 1} à {tranches[i][1]}",
            key=cle, on_change=memoriser_tranche,
            help="Parcourir les exercices évalués, du plus récent au plus ancien. "
                 "Le diagnostic porte toujours sur l'ensemble des exercices filtrés.",
        )
    debut, fin = tranches[st.session_state[cle]]
    return points[debut:fin], (debut, fin)


def _html_tableau(points):
    recents = points
    if not recents:
        return ""
    maxi = max(len(x["questions"]) for x in recents)
    titres = "".join(f"<th scope='col'>C{i}</th>" for i in range(1, maxi + 1))
    lignes = []
    for p in recents:
        type_ligne = "P" if p["niveau"] >= 7 else "Ex"
        titre = f"N{p['niveau']} · S{p['serie']} · {type_ligne}{p['numero']}"
        colonnes = []
        for i in range(maxi):
            if i >= len(p["questions"]):
                colonnes.append("<td class='mc-heat-none' aria-label='Question absente'>—</td>")
            elif p["questions"][i]:
                colonnes.append("<td class='mc-heat-ok' aria-label='Bonne réponse'>✓</td>")
            else:
                colonnes.append("<td class='mc-heat-ko' aria-label='Réponse incorrecte'>×</td>")
        lignes.append(f"<tr><th scope='row'>{escape(titre)}</th>{''.join(colonnes)}</tr>")
    return """
    <style>
    .mc-heat-wrap{overflow-x:auto;width:100%;max-width:100%;margin:5px 0 10px}
    .mc-heat{border-collapse:separate;border-spacing:4px;width:100%;font-size:.88rem}
    .mc-heat th,.mc-heat td{text-align:center;white-space:nowrap;padding:7px 5px;border-radius:5px}
    .mc-heat thead th{color:#47617a;font-weight:650;font-size:.8rem}
    .mc-heat tbody th{color:#253a51;font-size:.8rem;text-align:left;background:#f3f6fa}
    .mc-heat td{min-width:29px;font-size:1.02rem;font-weight:700}
    .mc-heat-ok{background:#dcf4e6;color:#136b3e}
    .mc-heat-ko{background:#fce6e5;color:#af2525}
    .mc-heat-none{background:#f1f2f4;color:#81858c}
    @media(max-width:540px){.mc-heat{border-spacing:2px;font-size:.74rem}
      .mc-heat th,.mc-heat td{padding:6px 3px}.mc-heat td{min-width:24px}}
    </style><div class='mc-heat-wrap' role='region' aria-label='Répartition des réponses par exercice'>
    <table class='mc-heat'><thead><tr><th scope='col'>Exercice</th>""" + titres + "</tr></thead><tbody>" + "".join(lignes) + "</tbody></table></div>"


def afficher_tableau_series(st, client, eleve_id, series_filtrees):
    """Affichage automatique dans Mes séries, après les filtres, avant la liste."""
    st.markdown("#### Mon bilan de compétences")
    st.caption("Mes premières réponses évaluées, sans correction préalable · niveaux 1 à 9")
    memo = st.session_state.get("_mc_heat_cache")
    import time
    if (not isinstance(memo, dict)
            or memo.get("compte") != eleve_id
            or memo.get("jeton") != st.session_state.get("jeton_persistant")
            or time.monotonic() - memo.get("lu_a", -9999) > 60):
        try:
            lignes = charger_evenements(client, eleve_id)
        except Exception:
            st.info("Le tableau des réponses est momentanément indisponible.")
            return
        st.session_state["_mc_heat_cache"] = {
            "compte": eleve_id, "jeton": st.session_state.get("jeton_persistant"),
            "lu_a": time.monotonic(), "lignes": lignes,
        }
    else:
        lignes = memo["lignes"]
    bilan = calculer_bilan(series_filtrees, lignes)
    if not bilan["points"]:
        st.info("Pas encore de vérification autonome complète pour ces filtres. "
                "Les anciennes tentatives ne sont pas reconstituées.")
        return
    # La sélection de la tranche ne change jamais le groupe diagnostiqué.
    points = bilan["points"]
    somme = resumer_questions(points)
    groupes = analyser_bilan(points)
    groupe_unique = groupes[0] if len(groupes) == 1 else None
    taux = (round(100 * somme["questions_bonnes"] / somme["questions"])
            if somme["questions"] else 0)

    # Trois indicateurs faciles à comprendre, avec leurs dénominateurs.
    col_score, col_finale, col_volume = st.columns(3, gap="small")
    with col_score:
        st.metric("Questions réussies", f"{taux} %")
        st.caption(f"{somme['questions_bonnes']}/{somme['questions']} questions notées")
    if groupe_unique and groupe_unique["niveau"] >= 7:
        etape_finale = groupe_unique["stats"]["etapes"].get("Résolution finale") or {}
        nb_finales = etape_finale.get("total", 0)
        bonnes_finales = etape_finale.get("bonnes", 0)
        with col_finale:
            st.metric("Résolutions finales", (
                f"{round(100 * bonnes_finales / nb_finales)} %"
                if nb_finales else "—"
            ))
            st.caption(f"{bonnes_finales}/{nb_finales} questions finales notées")
        with col_volume:
            st.metric("Problèmes renseignés",
                      f"{groupe_unique['stats']['problemes_entierement_renseignes']}"
                      f"/{len(groupe_unique['points'])}")
            st.caption("Toutes les cases remplies, sans garantir la réussite")
    else:
        with col_finale:
            st.metric("Questions notées", str(somme["questions"]))
            st.caption("Parties évaluables automatiquement")
        with col_volume:
            st.metric("Exercices évalués", str(len(points)))
            st.caption("Premières vérifications autonomes")

    # Le conseil doit être visible AVANT les longs tableaux explicatifs.
    if len(groupes) == 1:
        g = groupes[0]
        stats = g["stats"]
        constat, interpretation, proposition = conseil_argumente(g)
        with st.container(border=True):
            st.markdown("##### Mon conseil pour progresser")
            st.write(proposition)
            st.caption(interpretation)
    elif len(groupes) > 1:
        with st.container(border=True):
            st.markdown("##### Mon conseil pour progresser")
            st.write("Les résultats sont analysés séparément par chapitre et par niveau. "
                     "Choisis un chapitre et un niveau dans les filtres pour recevoir "
                     "un conseil personnalisé.")
        st.dataframe([
            {
                "Chapitre": grp["chapitre"],
                "Niveau": grp["niveau"],
                "Questions évaluées": grp["stats"]["questions"],
                "Réussite": (f"{round(100 * grp['taux'])} %"
                            if grp["taux"] is not None else "—"),
                "Conseil": {
                    "echantillon_insuffisant": "Continuer à s'entraîner",
                    "verification_humaine_necessaire": "Vérifier les réponses rédigées",
                    "progression_sous_reserve_redaction": "Passage envisageable, rédaction à vérifier",
                    "a_consolider": "Consolider",
                    "analyse_incomplete": "Données à compléter",
                    "encourageant": "Résultats encourageants",
                    "progression_envisageable": "Passage envisageable",
                }.get(grp["statut"], "À suivre"),
            } for grp in groupes
        ], hide_index=True, width="stretch")

    # Pagination visuelle, indépendante du calcul précédent.
    gauche, droite = st.columns([4, 1.5], gap="small")
    with gauche:
        st.markdown("##### Répartition de mes réponses")
        st.caption(f"{len(points)} exercices évalués, du plus récent au plus ancien")
    with droite:
        selection, (debut, fin) = _tranche_choisie(st, eleve_id, points)
    st.html(_html_tableau(selection))
    st.caption(
        f"Lignes {debut + 1} à {fin} sur {len(points)} · "
        "✓ correcte · × incorrecte · — champ absent. "
        "C1, C2… désignent les champs de réponse, pas nécessairement des questions distinctes."
    )
    with st.expander("Comment sont calculés mes résultats ?", expanded=False):
        st.write(
            "Le pourcentage principal compte les **questions pédagogiques** : "
            "une question à plusieurs champs n'est réussie que si tous "
            "ses champs évaluables sont corrects."
        )
        st.caption(
            f"Questions : {somme['questions_bonnes']}/{somme['questions']} correctes "
            f"({taux} %). Champs de réponse : {bilan['bonnes']}/{bilan['total']} "
            f"corrects ({round(100 * bilan['bonnes']/bilan['total'])} %). "
            "Ces résultats portent sur tous les exercices des filtres, "
            "quelle que soit la tranche affichée."
        )
        st.caption("Seules les premières vérifications complètes, sans correction "
                   "consultée auparavant, entrent dans ce bilan.")
        if bilan["exclus"]:
            st.caption("Certaines tentatives incomplètes, réalisées après "
                       "correction ou non détaillables ne sont pas comptées.")

    if len(groupes) != 1:
        return None
    # Conserver les tableaux de diagnostic détaillés et les actions existantes.
    st.markdown("##### Mes points forts et difficultés")
    if stats["competences"]:
        st.markdown("**Types de tâches mathématiques**")
        st.dataframe([
            {"Type de tâche": nom,
             "Partie notée correcte": f"{v['bonnes']}/{v['total']}",
             "Erreurs": v["total"] - v["bonnes"]}
            for nom, v in sorted(stats["competences"].items())
        ], hide_index=True, width="stretch")
        st.caption("Ce tableau indique où apparaissent les erreurs ; "
                   "il ne permet pas, à lui seul, d'en connaître la cause.")
    if g["niveau"] >= 7 and stats["etapes"]:
        st.markdown("**Réussite selon l'étape du problème**")
        ordre = ("Début du problème", "Étapes intermédiaires", "Résolution finale")
        st.dataframe([
            {"Étape": label,
             "Partie notée correcte": f"{stats['etapes'][label]['bonnes']}/{stats['etapes'][label]['total']}",
             "Erreurs": stats["etapes"][label]["total"] - stats["etapes"][label]["bonnes"]}
            for label in ordre if label in stats["etapes"]
        ], hide_index=True, width="stretch")
    elif stats["notions"]:
        st.markdown("**Réussite selon la notion travaillée**")
        st.dataframe([
            {"Notion": nom, "Partie notée correcte": f"{v['bonnes']}/{v['total']}",
             "Erreurs": v["total"] - v["bonnes"]}
            for nom, v in sorted(stats["notions"].items())
        ], hide_index=True, width="stretch")

    if g["niveau"] >= 7:
        st.caption(
            f"Repères pour progresser : au moins 6 problèmes entièrement "
            f"renseignés (actuellement {stats['problemes_entierement_renseignes']}), "
            f"20 questions notées (actuellement {stats['questions']}), "
            "80 % de réussite et pas de difficulté répétée importante."
        )
    if stats["problemes_redaction_manquante"]:
        st.caption(
            f"Rédactions : {stats['problemes_redaction_manquante']} problème(s) "
            "ont encore une rédaction vide dans les réponses enregistrées. "
            "Elles ne sont pas évaluées automatiquement et ne retirent aucun point."
        )
    if stats["problemes_avec_texte_libre"]:
        with st.expander("Détail des réponses rédigées", expanded=False):
            st.caption(
                f"Parmi les exercices évalués : {stats['problemes_sans_redaction']} "
                "sans rédaction, "
                f"{stats['problemes_redaction_renseignee']} avec rédaction "
                "actuellement renseignée et "
                f"{stats['problemes_redaction_manquante']} avec rédaction "
                "non renseignée dans les sauvegardes. "
                "Une rédaction complétée n'est jamais comptée automatiquement "
                "comme correcte et son état au premier contrôle est inconnu."
            )
    if stats["sans_numerotation"] and g["niveau"] >= 7:
        st.caption("Certaines séries ne précisent pas la numérotation des "
                   "questions : aucune compétence finale n'est inférée pour elles.")
    if g["apres"]["questions"]:
        avant, apres = g["avant"], g["apres"]
        st.caption("Comparaison indicative : exercices habituels / entraînement "
                   "ciblé du même niveau (échantillons et modèles potentiellement différents).")
        st.dataframe([
            {"Période": "Hors entraînement ciblé",
             "Questions": avant["questions"],
             "Réussite": (f"{round(100 * avant['questions_bonnes']/avant['questions'])} %"
                         if avant["questions"] else "—")},
            {"Période": "Entraînement ciblé",
             "Questions": apres["questions"],
             "Réussite": (f"{round(100 * apres['questions_bonnes']/apres['questions'])} %"
                         if apres["questions"] else "—")},
        ], hide_index=True, width="stretch")
    cible = g["cible"]
    if (cible and g["statut"] in ("a_consolider", "echantillon_insuffisant")
            and cible["chapitre"] == "1. Opérations"):
        st.caption("Exercices ciblés : même modèle et même niveau que le problème "
                   "où cette difficulté a été observée. Ils permettront une "
                   "nouvelle première vérification autonome.")
        if st.button("Générer 3 exercices pour m'améliorer",
                     key=f"mathicap_entrainement_adaptatif_{g['niveau']}",
                     type="primary"):
            return cible
    elif g["difficultes"]:
        st.caption("Un entraînement automatique pour cette notion n'est pas "
                   "encore disponible. Tu peux créer une nouvelle série au même niveau.")
    return None
