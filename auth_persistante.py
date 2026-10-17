
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager


def obtenir_cookies():
    cookies = EncryptedCookieManager(
        prefix="mon_prof_maths_",
        password=st.secrets["COOKIE_PASSWORD"]
    )

    if not cookies.ready():
        st.stop()

    return cookies


def session_eleve_active():
    return bool(st.session_state.get("eleve_id"))


def deconnecter_eleve():
    st.session_state.pop("eleve_id", None)
    st.session_state.pop("session_eleve", None)
    st.session_state.pop("exercices_actuels", None)
    st.session_state.pop("code_actuel", None)


