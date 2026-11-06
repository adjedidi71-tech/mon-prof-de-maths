
import streamlit as st
# Le composant externe streamlit-local-storage (v1) ne se charge plus
# de façon fiable sur Streamlit Community Cloud.
# Composant natif Streamlit v2 : aucun script externe, aucune iframe dédiée.

_STORAGE_JS = r"""
const publications = new WeakMap();

export default function(component) {
    const { parentElement, data, setStateValue } = component;
    const requete = data || {};
    const nom = 'jeton_persistant_maths'; // Nom historique : garde les sessions déjà présentes.
    let valeur = '';
    let disponible = true;

    try {
        if (requete.action === 'write' && typeof requete.value === 'string') {
            window.localStorage.setItem(nom, requete.value);
        } else if (requete.action === 'delete') {
            window.localStorage.removeItem(nom);
        }
        valeur = window.localStorage.getItem(nom) || '';
    } catch (_err) {
        // Navigateur bloquant le stockage (mode privé/restrictions).
        disponible = false;
    }

    // Ne publier que les changements ; sinon boucle de reruns Streamlit.
    const rapport = JSON.stringify({
        version: requete.version || 'initiale',
        disponible: disponible,
        valeur: valeur
    });
    if (publications.get(parentElement) !== rapport) {
        publications.set(parentElement, rapport);
        setStateValue('rapport', JSON.parse(rapport));
    }
}
"""

_COMPOSANT_STOCKAGE = st.components.v2.component(
    'mathicap_stockage_navigateur_v2', js=_STORAGE_JS
)


def _stockage_modifie():
    """Rerun automatique de Streamlit après lecture/écriture du navigateur."""
    pass


def _programmer_stockage(action, valeur=''):
    """L'écriture est exécutée par le navigateur au prochain rerun."""
    from uuid import uuid4
    st.session_state['_mathicap_stockage_commande'] = {
        'action': action,
        'value': valeur if action == 'write' else '',
        'version': uuid4().hex,
    }


def tester_stockage():
    return lire_jeton_navigateur() is not None


def obtenir_stockage():
    """Compatibilité avec les anciens imports : pas de composant v1."""
    return _COMPOSANT_STOCKAGE

def session_eleve_active():
    return bool(st.session_state.get("eleve_id"))


def deconnecter_eleve():
    # Une déconnexion ne doit jamais conserver l’autorisation QCM locale.
    _vider_cache_verification_session()
    st.session_state.pop("eleve_id", None)
    st.session_state.pop("session_eleve", None)
    st.session_state.pop("exercices_actuels", None)
    st.session_state.pop("code_actuel", None)

import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from time import monotonic


def creer_jeton():
    return secrets.token_urlsafe(32)


def empreinte_jeton(jeton):
    return hashlib.sha256(jeton.encode("utf-8")).hexdigest()


def expiration_session():
    return (
        datetime.now(timezone.utc) + timedelta(days=30)
    ).isoformat()

def enregistrer_session(supabase_privee, eleve_id):
    jeton = creer_jeton()

    supabase_privee.table(
        "sessions_persistantes"
    ).insert({
        "eleve_id": eleve_id,
        "jeton_hash": empreinte_jeton(jeton),
        "expire_le": expiration_session()
    }).execute()

    return jeton

# Cache strictement local à une session Streamlit, jamais partagé entre élèves.
# Un appel ordinaire reste systématiquement vérifié dans Supabase.
_CACHE_SESSION_KEY = '_mathicap_session_verifiee_qcm'


def _vider_cache_verification_session():
    st.session_state.pop(_CACHE_SESSION_KEY, None)


def verifier_session(supabase_privee, jeton, *, cache_seconds=0):
    """Vérifie un jeton côté serveur et renouvelle son expiration de 30 jours.

    Par défaut, aucune réponse mise en cache n'est acceptée (app.py et autres
    fonctions d'authentification restent inchangés dans leur comportement).
    Seules les opérations QCM peuvent demander de réutiliser une vérification
    récente, durant 30 secondes au plus, dans CETTE session Streamlit.
    Après cette période, un nouvel appel Supabase est impératif. Les jetons
    expirés/supprimés ne sont jamais recréés.
    """
    if not isinstance(jeton, str) or not jeton:
        _vider_cache_verification_session()
        return None

    empreinte = empreinte_jeton(jeton)
    maintenant_monotone = monotonic()
    # Même si un appelant demande davantage, ne jamais dépasser 30 secondes.
    delai_cache = max(0.0, min(float(cache_seconds), 30.0))
    souvenir = st.session_state.get(_CACHE_SESSION_KEY)
    eleve_courant = st.session_state.get('eleve_id')

    if (delai_cache > 0 and isinstance(souvenir, dict)
            and souvenir.get('empreinte') == empreinte
            and isinstance(souvenir.get('eleve_id'), str)
            and (eleve_courant is None or eleve_courant == souvenir['eleve_id'])
            and isinstance(souvenir.get('verifie_le'), (float, int))
            and 0 <= maintenant_monotone - souvenir['verifie_le'] < delai_cache):
        return souvenir['eleve_id']

    maintenant = datetime.now(timezone.utc).isoformat()
    try:
        resultat = (
            supabase_privee
            .table('sessions_persistantes')
            .update({'expire_le': expiration_session()})
            .eq('jeton_hash', empreinte)
            .gt('expire_le', maintenant)
            .select('eleve_id')
            .execute()
        )
    except Exception:
        # Ne jamais utiliser une ancienne validation si Supabase a échoué.
        _vider_cache_verification_session()
        raise

    lignes = resultat.data or []
    if not lignes or not isinstance(lignes[0].get('eleve_id'), str):
        _vider_cache_verification_session()
        return None

    eleve_id = lignes[0]['eleve_id']
    st.session_state[_CACHE_SESSION_KEY] = {
        'empreinte': empreinte,
        'eleve_id': eleve_id,
        'verifie_le': monotonic(),
    }
    return eleve_id


def supprimer_session(supabase_privee, jeton):
    # Révocation locale immédiate, même si l'appel à Supabase échoue.
    _vider_cache_verification_session()
    if not jeton:
        return

    supabase_privee.table(
        "sessions_persistantes"
    ).delete().eq(
        "jeton_hash",
        empreinte_jeton(jeton)
    ).execute()

def enregistrer_jeton_navigateur(jeton):
    """Programme l'enregistrement durable du jeton dans le navigateur."""
    if isinstance(jeton, str) and jeton:
        _programmer_stockage('write', jeton)


def effacer_jeton_navigateur():
    """Programme la suppression du jeton à la déconnexion."""
    _programmer_stockage('delete')


def lire_jeton_navigateur():
    """Monte UNE fois par rerun le pont intégré Streamlit / navigateur.

    Avant que le JavaScript renvoie sa valeur, retourne None.
    La réponse JavaScript déclenche alors un rerun et la restauration peut
    s'effectuer. Le composant reste monté même une fois connecté.
    """
    commande = st.session_state.get('_mathicap_stockage_commande')
    version = st.session_state.get('_mathicap_stockage_derniere_version', 'initiale')
    requete = commande or {'action': 'read', 'version': version}

    resultat = _COMPOSANT_STOCKAGE(
        key='mathicap_stockage_navigateur',
        data=requete,
        height=0,
        on_rapport_change=_stockage_modifie,
    )
    rapport = getattr(resultat, 'rapport', None)
    if not isinstance(rapport, dict):
        return None

    if commande is not None:
        if rapport.get('version') != commande['version']:
            # Éviter d'utiliser l'ancienne réponse tant que l'ordre est en cours.
            return None
        st.session_state['_mathicap_stockage_derniere_version'] = commande['version']
        st.session_state.pop('_mathicap_stockage_commande', None)

    if not rapport.get('disponible', False):
        return None
    valeur = rapport.get('valeur')
    return valeur if isinstance(valeur, str) and valeur else None
