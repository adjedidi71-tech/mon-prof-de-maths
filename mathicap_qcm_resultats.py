"""MathiCap : séries QCM et résultats conservés dans Supabase.

Le jeton de l'élève est vérifié côté serveur avant chaque lecture/écriture.
Aucune donnée d'un autre compte n'est retournée et aucune clé secrète ne
passe dans les composants de la page.
"""
from __future__ import annotations

from datetime import datetime, timezone
from time import perf_counter
import uuid
import streamlit as st
from supabase import create_client
from auth_persistante import verifier_session

TABLE = 'mathicap_qcm_resultats'
LABELS = {
    'decimaux': 'Calculs décimaux',
    'euclidienne': 'Division euclidienne',
    'division_decimale': 'Division décimale',
    'priorites': 'Priorités opératoires',
    'distributivite': 'Distributivité',
    'melange': 'Chapitre 1 — Mélange',
}


def _client_prive():
    """Un client privé par session Streamlit, jamais partagé entre élèves."""
    cle = '_mathicap_qcm_client_prive'
    client = st.session_state.get(cle)
    if client is None:
        client = create_client(
            st.secrets['SUPABASE_URL'], st.secrets['SUPABASE_SECRET_KEY']
        )
        st.session_state[cle] = client
    return client


def _compte_valide(client):
    utilisateur = st.session_state.get('eleve_id')
    jeton = st.session_state.get('jeton_persistant')
    if not isinstance(utilisateur, str) or not isinstance(jeton, str) or not jeton:
        return None
    try:
        return utilisateur if verifier_session(client, jeton, cache_seconds=30) == utilisateur else None
    except Exception:
        return None


def _numero_ligne(eleve_id, partie_id):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f'mathicap:qcm:{eleve_id}:{partie_id}'))


def _verifier_partie(partie):
    if not isinstance(partie, dict):
        return 'Partie QCM incorrecte.'
    if (partie.get('notion') not in LABELS or not isinstance(partie.get('id'), str)
            or not (8 <= len(partie['id']) <= 64)):
        return 'Identifiant de QCM invalide.'
    questions = partie.get('questions')
    reponses = partie.get('reponses')
    if not isinstance(questions, list) or len(questions) != 10 or not isinstance(reponses, dict):
        return 'La partie QCM doit comporter dix questions.'
    ids = [q.get('id') for q in questions if isinstance(q, dict)]
    if (len(ids) != 10 or len(set(ids)) != 10 or any(not isinstance(i, str) for i in ids)):
        return 'Questions du QCM invalides.'
    for q in questions:
        opts = q.get('options')
        rep = q.get('answer')
        if (not isinstance(q.get('question'), str) or not isinstance(opts, list)
                or len(opts) != 4 or not isinstance(rep, int) or rep not in range(4)
                or not isinstance(q.get('explain'), str)):
            return 'Format d’une question invalide.'
    for ident, indice in reponses.items():
        if ident not in ids or not isinstance(indice, int) or indice not in range(4):
            return 'Réponse QCM invalide.'
    return None


def _donnees(partie, utilisateur, terminee):
    questions = partie['questions']
    reponses = partie['reponses']
    points = sum(reponses.get(q['id']) == q['answer'] for q in questions) if terminee else 0
    index = max(0, min(int(partie.get('index', 0)), 10))
    maintenant = datetime.now(timezone.utc).isoformat()
    retour = {
        'id': _numero_ligne(utilisateur, partie['id']),
        'eleve_id': utilisateur,
        'partie_id': partie['id'],
        'notion': partie['notion'],
        'bonnes': points,
        'total': 10,
        'questions': None if terminee else questions,
        'reponses': {} if terminee else reponses,
        'statut': 'termine' if terminee else 'en_cours',
        'index_courant': index,
        'modifie_le': maintenant,
    }
    if terminee:
        retour['termine_le'] = maintenant
    return retour


def _message_erreur(exc):
    code = str(getattr(exc, 'code', '') or '')
    if code in ('PGRST205', '42P01', '42703', 'PGRST204'):
        return ('Lecture QCM impossible (code ' + code + '). Vérifie que les colonnes '
                'questions, reponses, statut, index_courant et modifie_le existent '
                'dans le projet Supabase utilisé par MathiCap.')
    if code == '42501':
        return 'Accès au stockage refusé. Vérifie les droits de la table QCM.'
    return 'Sauvegarde indisponible. Tes réponses restent affichées sur cette page.'


def enregistrer_partie(partie):
    """Sauvegarde immédiate ; petites mises à jour une fois les questions créées.

    Chaque action garde la vérification serveur de la session et la condition
    « statut = en_cours ». Les dix questions ne sont envoyées qu'à la création.
    """
    erreur = _verifier_partie(partie)
    if erreur:
        return False, erreur
    if partie.get('terminee'):
        return enregistrer_resultat(partie)

    debut = perf_counter()
    apres_session = None

    def rapport(action):
        """Uniquement des durées : aucune donnée d'élève ou secret dans l'UI."""
        fin = perf_counter()
        st.session_state['mc_qcm_temps'] = {
            'action': action,
            'session_ms': round(1000 * ((apres_session or fin) - debut)),
            'base_ms': round(1000 * (fin - (apres_session or fin))),
            'total_ms': round(1000 * (fin - debut)),
        }

    try:
        client = _client_prive()
        eleve = _compte_valide(client)
        apres_session = perf_counter()
        if not eleve:
            rapport('session invalide')
            return False, 'Connecte-toi pour conserver tes séries QCM.'

        identifiant = _numero_ligne(eleve, partie['id'])
        if not partie.get('_qcm_ligne_confirmee'):
            # Première création : conserver en base les dix questions et leur ordre.
            ancien = (client.table(TABLE).select('statut')
                      .eq('eleve_id', eleve).eq('partie_id', partie['id'])
                      .limit(1).execute())
            lignes = ancien.data or []
            if lignes and lignes[0].get('statut') == 'termine':
                rapport('lecture statut')
                return False, 'Ce QCM est déjà terminé, impossible de le modifier.'
            if not lignes:
                client.table(TABLE).insert(_donnees(partie, eleve, False)).execute()
                partie['_qcm_ligne_confirmee'] = True
                rapport('création QCM')
                return True, 'Série QCM sauvegardée.'

        # Mises à jour suivantes : réponses + position seulement.
        # Ne pas transmettre à répétition questions/options/corrections déjà stockées.
        modification = {
            'reponses': dict(partie['reponses']),
            'index_courant': max(0, min(int(partie.get('index', 0)), 10)),
            'modifie_le': datetime.now(timezone.utc).isoformat(),
        }
        mise_a_jour = (client.table(TABLE).update(modification)
                       .eq('id', identifiant).eq('eleve_id', eleve)
                       .eq('statut', 'en_cours').select('id').execute())
        rapport('mise à jour QCM')
        if not (mise_a_jour.data or []):
            return False, 'Le QCM est introuvable ou déjà terminé : sauvegarde refusée.'
        partie['_qcm_ligne_confirmee'] = True
        return True, 'Série QCM sauvegardée.'
    except Exception as exc:
        rapport('échec sauvegarde')
        return False, _message_erreur(exc)


def enregistrer_resultat(partie):
    """Conserve uniquement le score, la notion et la date du QCM terminé."""
    erreur = _verifier_partie(partie)
    if erreur:
        return False, erreur
    if any(q['id'] not in partie['reponses'] for q in partie['questions']):
        return False, 'Réponds aux dix questions pour terminer le QCM.'
    try:
        client = _client_prive()
        eleve = _compte_valide(client)
        if not eleve:
            return False, 'Connecte-toi pour sauvegarder les résultats.'
        donnees = _donnees(partie, eleve, True)
        client.table(TABLE).upsert(donnees, on_conflict='id').execute()
        controle = (client.table(TABLE).select('bonnes,total,statut,questions,reponses')
                    .eq('eleve_id', eleve).eq('partie_id', partie['id'])
                    .limit(1).execute())
        lignes = controle.data or []
        if not lignes:
            return False, 'Enregistrement non confirmé. Réessaie sans refaire le QCM.'
        ligne = lignes[0]
        if (int(ligne.get('bonnes', -1)) != donnees['bonnes']
                or ligne.get('statut') != 'termine'
                or ligne.get('questions') not in (None, [])
                or (ligne.get('reponses') or {}) != {}):
            return False, 'Le score n’a pas été confirmé correctement. Réessaie.'
        return True, 'Score enregistré et vérifié dans ton compte.'
    except Exception as exc:
        return False, _message_erreur(exc)


def charger_parties(limite=30):
    """Historique privé de l'élève (parties terminées ou non)."""
    try:
        client = _client_prive()
        eleve = _compte_valide(client)
        if not eleve:
            return None, 'Connecte-toi pour retrouver tes séries QCM.'
        resultat = (client.table(TABLE)
                    .select('partie_id,notion,statut,bonnes,total,index_courant,reponses,modifie_le')
                    .eq('eleve_id', eleve).eq('statut', 'en_cours').order('modifie_le', desc=True)
                    .limit(max(1, min(int(limite), 100))).execute())
        donnees = resultat.data or []
        for r in donnees:
            r['notion_label'] = LABELS.get(r.get('notion'), r.get('notion', 'QCM'))
            r['nombre_reponses'] = len(r.get('reponses') or {})
        return donnees, None
    except Exception as exc:
        return None, _message_erreur(exc)


def charger_partie(partie_id):
    """Recharge les choix réels et l'ordre exact des dix questions."""
    if not isinstance(partie_id, str) or not (8 <= len(partie_id) <= 64):
        return None, 'Identifiant de série invalide.'
    try:
        client = _client_prive()
        eleve = _compte_valide(client)
        if not eleve:
            return None, 'Connecte-toi pour retrouver ta série.'
        resultat = (client.table(TABLE)
                    .select('partie_id,notion,statut,questions,reponses,index_courant')
                    .eq('eleve_id', eleve).eq('partie_id', partie_id).eq('statut', 'en_cours')
                    .limit(1).execute())
        lignes = resultat.data or []
        if not lignes:
            return None, 'Aucun QCM en cours à reprendre avec cet identifiant.'
        ligne = lignes[0]
        questions = ligne.get('questions')
        if not isinstance(questions, list) or len(questions) != 10:
            return None, ('Cette ancienne série ne conserve que le score. '
                          'Les dix questions ne peuvent pas être récupérées rétroactivement.')
        termine = ligne.get('statut') == 'termine'
        partie = {
            'id': ligne['partie_id'],
            'notion': ligne['notion'],
            'questions': questions,
            'reponses': ligne.get('reponses') or {},
            'index': 10 if termine else max(0, min(int(ligne.get('index_courant') or 0), 9)),
            'terminee': termine,
            'revoir': False,
            'sauvegarde_tentee': termine,
            'sauvegarde_confirmee': termine,
            '_qcm_ligne_confirmee': True,
        }
        erreur = _verifier_partie(partie)
        if erreur:
            return None, 'Les questions sauvegardées ne sont pas exploitables.'
        return partie, None
    except Exception as exc:
        return None, _message_erreur(exc)


def questions_deja_vues(limite=12):
    """Favorise les questions jamais rencontrées dans les QCM récents."""
    try:
        client = _client_prive()
        eleve = _compte_valide(client)
        if not eleve:
            return set()
        resultat = (client.table(TABLE).select('questions')
                    .eq('eleve_id', eleve).eq('statut', 'en_cours').order('modifie_le', desc=True)
                    .limit(max(1, min(int(limite), 30))).execute())
        return {q.get('id') for ligne in (resultat.data or [])
                for q in (ligne.get('questions') or []) if isinstance(q, dict) and q.get('id')}
    except Exception:
        return set()


def charger_resultats(limite=50):
    """Renvoie seulement les QCM terminés ; les parties en cours ne comptent pas."""
    try:
        client = _client_prive()
        eleve = _compte_valide(client)
        if not eleve:
            return None, 'Connecte-toi pour consulter tes résultats.'
        resultat = (client.table(TABLE).select('notion,bonnes,total,termine_le,partie_id')
                    .eq('eleve_id', eleve).eq('statut', 'termine')
                    .order('termine_le', desc=True)
                    .limit(max(1, min(int(limite), 100))).execute())
        return (resultat.data or []), None
    except Exception as exc:
        return None, _message_erreur(exc)


def _ouvrir_depuis_profil(partie_id):
    partie, erreur = charger_partie(partie_id)
    if not partie:
        st.session_state['mc_qcm_erreur_ouverture'] = erreur
        return
    st.session_state['mathicap_qcm_partie'] = partie
    st.session_state['mathicap_qcm_notion'] = partie['notion']
    st.session_state['mathicap_page'] = 'QCM'
    try:
        st.query_params['vue'] = 'accueil'
    except Exception:
        pass


def afficher_progression_qcm():
    """Profil : notes et éventuel QCM inachevé à reprendre."""
    st.html('<div class="mc-profile-qcm-heading">Mes résultats QCM</div>')
    resultats, erreur = charger_resultats(50)
    if erreur:
        st.caption(erreur)
        return
    if not resultats:
        st.caption('Aucun QCM terminé et enregistré pour le moment.')
    else:
        nombre = len(resultats)
        moyenne = round(sum(int(x['bonnes']) for x in resultats) / nombre, 1)
        dernier = int(resultats[0]['bonnes'])
        g, d = st.columns(2, gap='small')
        with g:
            st.metric('QCM récents enregistrés', nombre)
        with d:
            st.metric('Dernier score', f'{dernier} / 10')
        st.caption(f'Moyenne sur les {nombre} derniers QCM : {moyenne:.1f}/10. '
                   'Cette moyenne ne remplace pas une évaluation scolaire.')
        with st.expander('Voir mes QCM par notion', width=500):
            groupes = {}
            for ligne in resultats:
                groupes.setdefault(ligne['notion'], []).append(int(ligne['bonnes']))
            for nom, valeurs in groupes.items():
                st.markdown(f'**{LABELS.get(nom, nom)}** — {len(valeurs)} QCM · '
                            f'dernier {valeurs[0]}/10 · meilleur {max(valeurs)}/10')
    # Chargement a la demande : un panneau FERME ne declenche plus la seconde
    # lecture Supabase. L'ouverture du panneau declenche un rerun Streamlit,
    # puis une lecture authentifiee des QCM inacheves.
    cle_panneau = 'mc_profile_qcm_inacheve_v7'
    with st.expander('Mon QCM inachevé à reprendre', width=500,
                     key=cle_panneau, on_change='rerun'):
        if st.session_state.get(cle_panneau, False):
            parties, erreur_parties = charger_parties(30)
            if parties:
                for row in parties:
                    st.button('▶ Reprendre — ' + row['notion_label']
                              + ' · ' + str(row.get('nombre_reponses', 0)) + '/10 réponses',
                              key='profil_mc_qcm_' + row['partie_id'],
                              on_click=_ouvrir_depuis_profil, args=(row['partie_id'],))
            elif erreur_parties:
                st.caption(erreur_parties)
            else:
                st.caption('Aucun QCM en cours à reprendre.')
    st.caption('Affichage limité aux 50 derniers QCM terminés enregistrés.')