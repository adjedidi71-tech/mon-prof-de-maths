"""MathiCap - analyse pédagogique prudente des premières réponses autonomes.

Lecture seule. Ne modifie ni note, ni série, ni historique Supabase.
Les champs d'une même question sont regroupés : une question est correcte
lorsque tous ses champs évaluables sont corrects. Les textes libres ne sont
jamais notés automatiquement et bloquent toute conclusion de maîtrise complète.
"""

from collections import defaultdict
from mathicap_competences import competences_par_question


def questions_pedagogiques(exercice, resultats_champs):
    """Retourne (questions, presence_libre, fiable_numero).

    Ne déduit jamais une compétence de l'intitulé ou de l'ordre des réponses.
    Les anciens exercices sans champ `question` restent affichables, mais
    ne participent pas aux recommandations sur les étapes d'un problème.
    """
    if not isinstance(exercice, dict) or not isinstance(resultats_champs, list):
        return [], False, False
    if exercice.get("reponse_attendue") is not None:
        if len(resultats_champs) != 1:
            return [], False, False
        return [{"numero": 1, "bonne": bool(resultats_champs[0]),
                 "competences": [], "explicite": False}], False, False

    champs = [c for c in exercice.get("champs_reponse", []) if isinstance(c, dict)]
    evaluables = [c for c in champs if c.get("type") != "texte_libre"]
    if len(evaluables) != len(resultats_champs):
        return [], False, False
    numero_fiable = bool(evaluables) and all(
        type(c.get("question")) is int and 1 <= c["question"] <= 50
        for c in evaluables
    )
    # Ne pas présenter l'avant-dernière question comme la résolution finale
    # lorsqu'une dernière question entièrement rédigée n'est pas évaluée.
    champs_libres = [c for c in champs if c.get("type") == "texte_libre"]
    if numero_fiable and champs_libres:
        if (any(type(c.get("question")) is not int for c in champs_libres)
                or max(c["question"] for c in champs_libres)
                > max(c["question"] for c in evaluables)):
            numero_fiable = False
    # Le mélange de numéros renseignés et absents ne doit pas fusionner
    # arbitrairement des champs dans une même question.
    groupes = {}
    for i, (champ, statut) in enumerate(zip(evaluables, resultats_champs), 1):
        numero = champ["question"] if numero_fiable else i
        g = groupes.setdefault(numero, {"numero": numero,
                                       "bonnes_champs": [], "competences": set(),
                                       "explicite": numero_fiable})
        g["bonnes_champs"].append(bool(statut))
        competence = champ.get("mathicap_competence")
        if isinstance(competence, str) and competence.strip():
            g["competences"].add(competence.strip()[:100])
    # Les métadonnées pédagogiques explicites sont prioritaires.
    # Le répertoire contrôlé prend le relais pour 31 modèles déterministes
    # du chapitre Opérations ; pas de déduction depuis une position seule.
    etiquettes = competences_par_question(exercice) if numero_fiable else {}
    questions = [
        {"numero": numero, "bonne": all(g["bonnes_champs"]),
         "competences": (sorted(g["competences"])
                         if g["competences"] else etiquettes.get(numero, [])),
         "explicite": numero_fiable}
        for numero, g in sorted(groupes.items())
    ]
    libre = any(c.get("type") == "texte_libre" for c in champs)
    return questions, libre, numero_fiable


def _etape(question, questions, niveau):
    """Niveaux 7-9 uniquement : positions dans un problème, pas compétences."""
    if niveau < 7 or len(questions) < 2 or not all(q["explicite"] for q in questions):
        return None
    if question["numero"] == questions[0]["numero"]:
        return "Début du problème"
    if question["numero"] == questions[-1]["numero"]:
        return "Résolution finale"
    return "Étapes intermédiaires"


def resumer_questions(points):
    """Agrège les premiers résultats notables et l'état ACTUEL des rédactions.

    L'achèvement de la saisie n'est pas une preuve de réussite autonome :
    seules les parties automatiquement vérifiables entrent dans le score.
    """
    q_total = q_bonnes = total_champs = bonnes_champs = 0
    entierement_saisis = 0
    sans_redaction = 0
    redactions_renseignees = 0
    redactions_manquantes = 0
    libres = 0
    sans_numerotation = 0
    positions = defaultdict(lambda: {"total": 0, "bonnes": 0})
    etapes = defaultdict(lambda: {"total": 0, "bonnes": 0})
    competences = defaultdict(lambda: {"total": 0, "bonnes": 0})
    notions = defaultdict(lambda: {"total": 0, "bonnes": 0})

    for p in points:
        qs = p.get("questions_pedagogiques", [])
        if not qs:
            continue
        total_champs += p["total"]
        bonnes_champs += p["bonnes"]
        q_total += len(qs)
        q_bonnes += sum(q["bonne"] for q in qs)
        if p.get("avec_texte_libre"):
            libres += 1
            if p.get("redaction_actuellement_renseignee") is True:
                redactions_renseignees += 1
                entierement_saisis += 1
            else:
                # Inconnu/non sauvegardé : on ne présume pas la saisie complète.
                redactions_manquantes += 1
        else:
            sans_redaction += 1
            entierement_saisis += 1
        if not p.get("numero_question_fiable"):
            sans_numerotation += 1
        niveau = p["niveau"]
        for q in qs:
            if q["explicite"]:
                position = positions[q["numero"]]
                position["total"] += 1
                position["bonnes"] += int(q["bonne"])
            etape = _etape(q, qs, niveau)
            if etape:
                g = etapes[etape]
                g["total"] += 1
                g["bonnes"] += int(q["bonne"])
            for tag in q["competences"]:
                g = competences[tag]
                g["total"] += 1
                g["bonnes"] += int(q["bonne"])
        partie = p.get("notion")
        if isinstance(partie, str) and partie.strip():
            g = notions[partie.strip()]
            g["total"] += len(qs)
            g["bonnes"] += sum(q["bonne"] for q in qs)

    return {"questions": q_total, "questions_bonnes": q_bonnes,
            "champs": total_champs, "champs_bons": bonnes_champs,
            # Au premier clic valide, tous les champs NOTABLES étaient remplis.
            # Les rédactions proviennent de la sauvegarde ACTUELLE ; elles peuvent
            # avoir été écrites ou modifiées après la première vérification.
            "problemes_entierement_renseignes": entierement_saisis,
            "problemes_sans_redaction": sans_redaction,
            "problemes_redaction_renseignee": redactions_renseignees,
            "problemes_redaction_manquante": redactions_manquantes,
            # Ancienne clé conservée pour compatibilité interne, à ne pas
            # présenter comme « nombre total de problèmes terminés ».
            "problemes_termines_evaluables": sans_redaction,
            "problemes_avec_texte_libre": libres,
            "sans_numerotation": sans_numerotation,
            "positions": dict(positions), "etapes": dict(etapes),
            "competences": dict(competences), "notions": dict(notions)}


def _difficultes_significatives(agregat, minimum=5, nature="etape"):
    """Repère des difficultés répétées, jamais une erreur isolée."""
    return sorted(
        [{"label": label, "total": g["total"],
          "erreurs": g["total"] - g["bonnes"], "nature": nature}
         for label, g in agregat.items()
         if g["total"] >= minimum and g["total"] - g["bonnes"] >= 3
         and 2 * (g["total"] - g["bonnes"]) >= g["total"]],
        key=lambda x: (x["erreurs"] / x["total"], x["erreurs"]), reverse=True,
    )


def _cible_entrainement(points, difficultes):
    """Exercice d'origine réellement raté sur une étape ciblée.

    Les possibilités de génération seront revalidées dans app.py (et côté
    serveur sur la série appartenant à l'élève) AVANT création de la série.
    """
    if not difficultes:
        return None
    difficulte = difficultes[0]
    label = difficulte["label"]
    nature = difficulte.get("nature")
    # Choisir un exercice portant réellement sur la même famille de tâches,
    # pas simplement un exercice où la dernière réponse est incorrecte.
    for p in points:
        qs = p.get("questions_pedagogiques", [])
        if nature == "famille":
            erreurs = [q for q in qs if not q["bonne"] and label in q["competences"]]
        elif nature == "etape":
            erreurs = [q for q in qs if not q["bonne"]
                       and _etape(q, qs, p["niveau"]) == label]
        else:
            erreurs = [q for q in qs if not q["bonne"] and (
                label in q["competences"] or label == f"Notion : {p.get('notion', '')}"
            )]
        if erreurs:
            return {"code_reprise": p.get("code_reprise"),
                    "numero_exercice": p.get("numero"),
                    "serie_id": p.get("serie_id"),
                    "chapitre": p["chapitre"], "niveau": p["niveau"],
                    "etape": label, "exercice_id": p.get("exercice_id")}
    return None


def analyser_bilan(points):
    """Retourne une synthèse par chapitre ET niveau, jamais de mélange des niveaux.

    Les statistiques portent sur les premières vérifications valides déjà
    filtrées par l'appelant. La tendance récente est évaluée sur 12 problèmes.
    """
    groupes = defaultdict(list)
    for point in points:
        if (isinstance(point, dict) and isinstance(point.get("chapitre"), str)
                and point["chapitre"] and type(point.get("niveau")) is int):
            groupes[(point["chapitre"], point["niveau"])].append(point)

    sorties = []
    for (chapitre, niveau), lignes in sorted(groupes.items(), key=lambda item: (item[0][0], item[0][1])):
        # Trier même si des données arrivent hors ordre.
        lignes = sorted(lignes, key=lambda p: p.get("date") or "", reverse=True)
        stats = resumer_questions(lignes)
        recents = resumer_questions(lignes[:12])
        # Une famille de tâches et une étape sont deux lectures distinctes :
        # conserver les DEUX permet de repérer une dernière question souvent
        # ratée, même lorsqu'elle couvre des familles mathématiques variées.
        familles = _difficultes_significatives(
            recents["competences"], nature="famille")
        if niveau >= 7:
            etapes = _difficultes_significatives(
                recents["etapes"], nature="etape")
            difficultes = familles + etapes
        else:
            notions = {f"Notion : {nom}": v
                       for nom, v in recents["notions"].items()}
            difficultes = familles + _difficultes_significatives(
                notions, nature="notion")
        apres = [p for p in lignes if p.get("entrainement_cible")]
        avant = [p for p in lignes if not p.get("entrainement_cible")]
        avant_stats = resumer_questions(avant)
        apres_stats = resumer_questions(apres)
        taux = (stats["questions_bonnes"] / stats["questions"]
                if stats["questions"] else None)
        eligible = None
        if niveau >= 7:
            if stats["problemes_entierement_renseignes"] < 6 or stats["questions"] < 20:
                eligible = "echantillon_insuffisant"
            elif taux is None or taux < .8 or difficultes:
                eligible = "a_consolider"
            elif recents["sans_numerotation"] > 0:
                eligible = "analyse_incomplete"
            elif stats["problemes_avec_texte_libre"]:
                # Les résultats numériques seuls ne certifient pas une
                # rédaction, mais ne doivent pas non plus effacer les progrès.
                eligible = "progression_sous_reserve_redaction"
            else:
                eligible = "progression_envisageable"
        else:
            if stats["questions"] < 10:
                eligible = "echantillon_insuffisant"
            elif taux is not None and taux >= .8 and not difficultes:
                eligible = "encourageant"
            else:
                eligible = "a_consolider"
        sorties.append({
            "chapitre": chapitre, "niveau": niveau,
            "points": lignes, "stats": stats, "recents": recents,
            "difficultes": difficultes,
            "cible": _cible_entrainement(lignes, difficultes),
            "statut": eligible, "taux": taux,
            "avant": avant_stats, "apres": apres_stats,
        })
    return sorties


def _fragilite_resolution_finale(g):
    """Conseil de vigilance, distinct d'une difficulté répétée bloquante.

    Un écart modéré sur la synthèse ne doit pas être ignoré quand la moyenne
    dépasse 80 %, ni transformer des réponses rédigées en erreurs.
    """
    if g.get("niveau", 0) < 7:
        return None
    etapes = g.get("stats", {}).get("etapes", {})
    finale = etapes.get("Résolution finale") or {}
    total = finale.get("total", 0)
    bonnes = finale.get("bonnes", 0)
    # Échantillon minimal : éviter un message pour 1 ou 2 réponses.
    if total < 6 or not 0 <= bonnes <= total:
        return None
    if bonnes / total >= 0.75:
        return None
    # Cette information est un signal d'attention, pas un diagnostic causal.
    return (f"Sur les questions de résolution finale automatiquement évaluables, "
            f"tu as réussi {bonnes} réponses sur {total} "
            f"({round(100 * bonnes / total)} %). "
            "Cette étape mérite encore un entraînement, sans que cela "
            "constitue à lui seul un blocage de progression.")


def conseil_argumente(g):
    """Conseil actionnable : réussite, fragilités, réserve et prochaine étape."""
    s = g["stats"]
    n = g["niveau"]
    nb = s["questions"]
    taux = round(100 * s["questions_bonnes"] / nb) if nb else 0
    constat = (f"Niveau {n} : {s['questions_bonnes']}/{nb} questions "
               f"automatiquement évaluables réussies ({taux} %) "
               f"sur {len(g['points'])} exercice(s) suivi(s).")
    fragilite = _fragilite_resolution_finale(g)
    if g["difficultes"]:
        d = g["difficultes"][0]
        sujet = ("les tâches de type" if d.get("nature") == "famille"
                 else "l'étape" if d.get("nature") == "etape"
                 else "la notion")
        interpretation = (
            f"Sur les 12 derniers exercices au maximum, les erreurs se répètent "
            f"sur {sujet} « {d['label']} » : "
            f"{d['erreurs']} erreurs sur {d['total']} questions évaluées. "
            "Ce constat ne suffit pas à identifier la cause des erreurs."
        )
    elif fragilite:
        interpretation = fragilite
    elif n >= 7 and g["recents"]["sans_numerotation"]:
        interpretation = (
            "Certaines questions ne possèdent pas de numéro pédagogique fiable ; "
            "l'analyse des étapes peut être incomplète."
        )
    else:
        interpretation = (
            "Aucune difficulté répétée importante n'a été détectée "
            "sur les réponses automatiquement évaluables."
        )
    statut = g["statut"]
    if statut == "echantillon_insuffisant":
        if n >= 7:
            proposition = (
                f"Continue au niveau {n} : "
                f"{s['problemes_entierement_renseignes']}/6 problèmes "
                f"entièrement renseignés et {s['questions']}/20 questions "
                "automatiquement évaluables. Il faut davantage de résultats "
                "pour donner un conseil de passage fiable."
            )
        else:
            proposition = (
                "Continue à t'entraîner au même niveau : il faut davantage "
                "de réponses pour établir une tendance."
            )
    elif statut == "progression_sous_reserve_redaction":
        ouverture = (f"Tu peux envisager le niveau {n + 1} "
                     if n < 9 else "Tu as atteint les critères du niveau 9")
        proposition = (
            ouverture + ": les critères quantitatifs "
            "et le taux de réussite sur les questions automatiquement notées "
            "sont atteints, sans difficulté répétée importante détectée. "
        )
        if fragilite:
            proposition += (
                f"Avant de commencer, consolide la résolution finale avec "
                f"quelques problèmes complets du niveau {n}. "
            )
        proposition += (
            "Les réponses rédigées ne sont pas notées automatiquement : "
            "leur vérification reste nécessaire pour confirmer la maîtrise "
            "complète du niveau."
        )
    elif statut == "progression_envisageable":
        ouverture = (f"Tu peux envisager le niveau {n + 1}" if n < 9
                     else "Tu as atteint les critères du niveau 9")
        proposition = ouverture + " : les critères prévus sont atteints."
        if fragilite:
            proposition += (
                f" Pour renforcer tes acquis, travaille encore quelques "
                f"résolutions finales sur des problèmes du niveau {n}."
            )
    elif statut in ("a_consolider", "analyse_incomplete"):
        proposition = (
            f"Poursuis pour le moment au niveau {n}. "
            "Refais des problèmes complets en ciblant les difficultés observées, "
            "puis compare tes nouvelles réponses."
        )
    else:
        proposition = (
            "Tes résultats sont encourageants. Tu peux envisager le niveau "
            "suivant, tout en continuant à consolider tes acquis."
        )
    return constat, interpretation, proposition
