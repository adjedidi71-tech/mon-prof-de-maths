"""Tableau de diagnostic visuel MathiCap : lecture seule, version 1.

Ne confond jamais réponses sauvegardées a posteriori avec première vérification.
Les tentatives anciennes / partielles / après correction sont exclues du score.
"""

from html import escape
from mathicap_diagnostic import premier_bilan


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
        points.append({
            "chapitre": chapitre if isinstance(chapitre, str) else "",
            "niveau": niveau, "serie": fiche.get("numero", "?"),
            "numero": numero, "questions": repartition,
            "bonnes": bonnes, "total": total,
            "date": ev.get("enregistre_le") or "",
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


def _html_tableau(points):
    recents = points[:10]
    maxi = max(len(x["questions"]) for x in recents)
    titres = "".join(f"<th scope='col'>Q{i}</th>" for i in range(1, maxi + 1))
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
    points = bilan["points"]
    st.caption(f"{len(points)} exercice(s) vérifié(s) · "
               f"{bilan['bonnes']}/{bilan['total']} réponses correctes "
               f"({round(100*bilan['bonnes']/bilan['total'])} %).")
    st.html(_html_tableau(points))
    st.caption("✓ Correcte · × Incorrecte · — Question absente. "
               "Les 10 dernières vérifications sont affichées ; "
               "les statistiques portent sur toutes les vérifications sélectionnées.")
    groupe_erreurs = [
        (i, g["total"] - g["bonnes"], g["total"])
        for i, g in sorted(bilan["positions"].items())
        if g["total"] >= 5 and (g["total"] - g["bonnes"]) >= 3
        and (g["total"] - g["bonnes"]) * 2 >= g["total"]
    ]
    if groupe_erreurs:
        positions = ", ".join(f"Q{i} ({n} erreurs sur {t})"
                              for i, n, t in groupe_erreurs[:3])
        st.warning("**Points à consolider :** les erreurs se répètent sur "
                   + positions + ". Vérifie les compétences évaluées dans ces "
                   "questions et réessaie des exercices comparables. Ce constat "
                   "ne permet pas encore d'identifier la cause exacte des erreurs.")
    elif len(points) >= 5:
        st.success("Tes erreurs ne se concentrent pas fortement sur une "
                   "position de question dans cet échantillon. Continue à "
                   "t'entraîner pour confirmer tes acquis.")
    else:
        st.info("Encore quelques exercices pour distinguer une difficulté "
                "régulière d'une erreur occasionnelle.")
    if bilan["finales_total"]:
        st.caption(f"Questions finales des problèmes (niveaux 7 à 9) : "
                   f"{bilan['finales_bonnes']}/{bilan['finales_total']} correctes.")
    if bilan["exclus"]:
        st.caption("Les vérifications incomplètes, consultations préalables "
                   "de correction et résultats non détaillables sont exclus "
                   "du tableau.")
