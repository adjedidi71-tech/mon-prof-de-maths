
import streamlit as st
from streamlit_local_storage import LocalStorage

def session_eleve_active():
    return bool(st.session_state.get("eleve_id"))


def deconnecter_eleve():
    st.session_state.pop("eleve_id", None)
    st.session_state.pop("session_eleve", None)
    st.session_state.pop("exercices_actuels", None)
    st.session_state.pop("code_actuel", None)



