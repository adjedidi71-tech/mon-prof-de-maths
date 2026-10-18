
import streamlit as st
from streamlit_local_storage import LocalStorage
def tester_stockage():
    stockage = LocalStorage()
    return stockage

def session_eleve_active():
    return bool(st.session_state.get("eleve_id"))


def deconnecter_eleve():
    st.session_state.pop("eleve_id", None)
    st.session_state.pop("session_eleve", None)
    st.session_state.pop("exercices_actuels", None)
    st.session_state.pop("code_actuel", None)

import secrets
import hashlib
from datetime import datetime, timedelta, timezone


def creer_jeton():
    return secrets.token_urlsafe(32)


def empreinte_jeton(jeton):
    return hashlib.sha256(jeton.encode("utf-8")).hexdigest()


def expiration_session():
    return (
        datetime.now(timezone.utc) + timedelta(days=30)
    ).isoformat()



