
import streamlit as st
from streamlit_local_storage import LocalStorage
def tester_stockage():
    stockage = LocalStorage()
    return stockage

def obtenir_stockage():
    if "stockage_navigateur" not in st.session_state:
        st.session_state["stockage_navigateur"] = LocalStorage()

    return st.session_state["stockage_navigateur"]

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

def verifier_session(supabase_privee, jeton):
    if not jeton:
        return None

    resultat = (
        supabase_privee
        .table("sessions_persistantes")
        .select("eleve_id, expire_le")
        .eq("jeton_hash", empreinte_jeton(jeton))
        .gt("expire_le", datetime.now(timezone.utc).isoformat())
        .limit(1)
        .execute()
    )

    if resultat.data:
        return resultat.data[0]["eleve_id"]

    return None



