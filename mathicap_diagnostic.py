"""MathiCap - projet 2, lot 1 : premier événement pédagogique immuable.

Aucun impact sur les scores visibles et les variantes du projet 1.
La base PostgreSQL fait respecter l'unicité atomique.
"""

MARQUEUR = "__mc_diag_actif_v1"


def valeur_renseignee(v):
    return v is not None and str(v).strip() not in ("", "Choisir...", "Choisir…")


def premier_bilan(exercice, reponses):
    """Score du 1er clic, selon la règle actuelle de l'exercice principal.

    Une vérification partielle est enregistrée, mais n'est PAS autonome.
    Les textes libres n'entrent jamais dans le dénominateur.
    """
    if not isinstance(exercice, dict):
        return None
    attendu_simple = exercice.get("reponse_attendue")
    if attendu_simple is not None:
        valeur = reponses.get("valeur") if isinstance(reponses, dict) else None
        if not valeur_renseignee(valeur):
            return {"bonnes": 0, "total": 1, "complet": False, "reponses": {}}
        return {
            "bonnes": int(valeur == attendu_simple), "total": 1, "complet": True,
            "reponses": {"valeur": valeur},
        }
    champs = [c for c in (exercice.get("champs_reponse") or [])
              if isinstance(c, dict) and c.get("type") != "texte_libre"]
    if not champs:
        return None
    saisies = reponses.get("champs", {}) if isinstance(reponses, dict) else {}
    if not isinstance(saisies, dict):
        saisies = {}
    copies = {c.get("id"): saisies.get(c.get("id")) for c in champs if c.get("id")}
    complet = all(valeur_renseignee(copies.get(c.get("id"))) for c in champs)
    bonnes = 0
    for c in champs:
        valeur = copies.get(c.get("id"))
        if not valeur_renseignee(valeur):
            continue
        if c.get("type") == "nombre":
            try:
                # Identique au calcul du bouton principal (égalité stricte).
                correcte = float(str(valeur).replace(",", ".")) == float(c.get("attendu"))
            except (TypeError, ValueError):
                correcte = False
        elif c.get("type") == "choix":
            correcte = valeur == c.get("attendu")
            if correcte:
                for dependance in c.get("dependances", []):
                    autre = next((a for a in champs if a.get("id") == dependance), None)
                    if autre and autre.get("type") == "nombre":
                        try:
                            correcte = (float(str(copies.get(dependance)).replace(",", "."))
                                        == float(autre.get("attendu")))
                        except (TypeError, ValueError):
                            correcte = False
                    if not correcte:
                        break
        else:
            correcte = valeur == c.get("attendu")
        bonnes += int(correcte)
    return {"bonnes": bonnes, "total": len(champs),
            "complet": complet, "reponses": copies}


def enregistrer_premier_evenement(client, eleve_id, code_reprise, numero,
                                evenement, exercice, reponses=None):
    """PostgREST RPC à INSERT ... ON CONFLICT DO NOTHING, première action unique.

    L'application appelle ceci AVANT de donner une aide ou un retour correctif.
    Si la RPC échoue, lever : on ne doit pas exposer le corrigé sans trace.
    """
    if evenement not in ("correction", "verification"):
        raise ValueError("Type d'événement pédagogique inconnu")
    bilan = premier_bilan(exercice, reponses or {}) if evenement == "verification" else None
    if evenement == "verification" and bilan is None:
        return None  # Exercice purement rédigé, non noté automatiquement.
    data = client.rpc("mc_diagnostic_premiere_action_v1", {
        "p_eleve_id": eleve_id,
        "p_code_reprise": code_reprise,
        "p_numero_exercice": int(numero),
        "p_evenement": evenement,
        "p_complet": bool(bilan["complet"]) if bilan else False,
        "p_bonnes": int(bilan["bonnes"]) if bilan else None,
        "p_total": int(bilan["total"]) if bilan else None,
        "p_reponses": bilan["reponses"] if bilan else {},
    }).execute().data
    if not isinstance(data, dict) or data.get("statut") not in ("verification", "correction"):
        raise RuntimeError("Enregistrement du diagnostic non confirmé")
    return data
