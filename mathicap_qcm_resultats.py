"""Sauvegarde et consultation des scores QCM de MathiCap.

Les données sont séparées des séries d'exercices. Les accès Supabase
sont côté serveur avec vérification du jeton de session de l'élève.
Aucune clé administrative n'est transmise au navigateur.
"""
from __future__ import annotations

import uuid
import streamlit as st
from supabase import create_client
from auth_persistante import verifier_session

TABLE = "mathicap_qcm_resultats"
LABELS = {
    "decimaux": "Calculs décimaux",
    "euclidienne": "Division euclidienne",
    "division_decimale": "Division décimale",
    "priorites": "Priorités opératoires",
    "distributivite": "Distributivité",
    "melange": "Chapitre 1 — Mélange",
}


def _client_prive():
    """Client privilégié réservé au serveur ; jamais dans les composants HTML/JS."""
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_SECRET_KEY"])


def _compte_valide(client):
    """Ne jamais faire confiance au seul identifiant dans session_state."""
    user_id = st.session_state.get("eleve_id")
    jeton = st.session_state.get("jeton_persistant")
    if not isinstance(user_id, str) or not isinstance(jeton, str) or not jeton:
        return None
    try:
        if verifier_session(client, jeton) == user_id:
            return user_id
    except Exception:
        pass
    return None


def enregistrer_resultat(partie):
    """Enregistre le score une seule fois par élève et partie.

    Retourne (ok, message). Le résultat n'inclut pas de données sensibles.
    """
    notion = partie.get("notion")
    questions = partie.get("questions")
    reponses = partie.get("reponses")
    partie_id = partie.get("id")
    if (notion not in LABELS or not isinstance(questions, list)
            or len(questions) != 10 or not isinstance(reponses, dict)
            or not isinstance(partie_id, str) or not (8 <= len(partie_id) <= 64)):
        return False, "Cette partie QCM n'est pas complète."
    if any(not isinstance(q, dict) or q.get("id") not in reponses
           for q in questions):
        return False, "Il reste des questions sans réponse."
    bonnes = sum(reponses.get(q["id"]) == q.get("answer") for q in questions)
    try:
        client = _client_prive()
        eleve_id = _compte_valide(client)
        if not eleve_id:
            return False, "Connecte-toi pour enregistrer tes résultats."
        id_resultat = str(uuid.uuid5(uuid.NAMESPACE_URL,
                                    f"mathicap:qcm:{eleve_id}:{partie_id}"))
        client.table(TABLE).upsert({
            "id": id_resultat,
            "eleve_id": eleve_id,
            "partie_id": partie_id,
            "notion": notion,
            "bonnes": bonnes,
            "total": 10,
        }, on_conflict="id").execute()
        # Une réponse d'écriture sans erreur ne suffit pas à prouver que la
        # ligne est visible. Vérifier avec le même compte avant de confirmer.
        controle = (client.table(TABLE)
                    .select("bonnes,total")
                    .eq("eleve_id", eleve_id)
                    .eq("partie_id", partie_id)
                    .limit(1)
                    .execute())
        lignes = controle.data or []
        if (not lignes or int(lignes[0].get("bonnes", -1)) != bonnes
                or int(lignes[0].get("total", -1)) != 10):
            return False, ("Le score est affiché, mais sa sauvegarde n'est pas "
                           "encore confirmée. Réessaie l'enregistrement.")
        return True, "Score enregistré et vérifié dans ton compte."
    except Exception as erreur:
        # Code d'erreur PostgREST : ne pas afficher au navigateur les détails
        # techniques, requêtes, clés ou identifiants de comptes.
        code = str(getattr(erreur, "code", "") or "")
        if code in ("PGRST205", "42P01"):
            return False, "Table des scores introuvable : vérifie le script SQL dans Supabase."
        if code == "42501":
            return False, "Le serveur n'a pas les droits nécessaires pour enregistrer le score."
        return False, ("Enregistrement indisponible pour le moment. "
                       "Le score reste visible ; tu peux réessayer sans refaire le QCM.")


def charger_resultats(limite=50):
    """Renvoie les résultats récents du seul compte actuellement vérifié."""
    try:
        client = _client_prive()
        eleve_id = _compte_valide(client)
        if not eleve_id:
            return None, "Connecte-toi pour consulter tes résultats."
        resultat = (client.table(TABLE)
                    .select("notion,bonnes,total,termine_le")
                    .eq("eleve_id", eleve_id)
                    .order("termine_le", desc=True)
                    .limit(max(1, min(int(limite), 100)))
                    .execute())
        return (resultat.data or []), None
    except Exception:
        return None, "Historique indisponible. Vérifie que la table Supabase a été créée."


def afficher_progression_qcm():
    """Petit tableau du profil ; n'altère aucun indicateur des exercices."""
    st.markdown("### Mes résultats QCM")
    resultats, erreur = charger_resultats(50)
    if erreur:
        st.caption(erreur)
        return
    if not resultats:
        st.caption("Aucun QCM terminé et enregistré pour le moment.")
        return
    essais = len(resultats)
    moyenne = round(sum(int(x["bonnes"]) for x in resultats) / essais, 1)
    derniere = int(resultats[0]["bonnes"])
    c1, c2 = st.columns(2, gap="small")
    with c1:
        st.metric("QCM récents enregistrés", essais)
    with c2:
        st.metric("Dernier score", f"{derniere} / 10")
    st.caption(f"Moyenne sur les {essais} derniers QCM : {moyenne:.1f}/10. "
               "Cette moyenne ne remplace pas une évaluation scolaire.")
    with st.expander("Voir mes QCM par notion", width=500):
        groupes = {}
        for row in resultats:
            notion = row["notion"]
            groupes.setdefault(notion, []).append(int(row["bonnes"]))
        for nom, scores in groupes.items():
            st.markdown(f"**{LABELS.get(nom, nom)}** — "
                        f"{len(scores)} QCM · dernier {scores[0]}/10 · "
                        f"meilleur {max(scores)}/10")
    st.caption("Affichage limité aux 50 derniers QCM enregistrés.")
