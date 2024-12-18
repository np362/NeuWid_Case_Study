import streamlit as st

# Definiere das Passwort
PASSWORD = "meinpasswort"

# Funktion zur Passwortprüfung
def check_password():
    # Falls das Passwort bereits korrekt eingegeben wurde
    if "password_correct" in st.session_state and st.session_state.password_correct:
        return True

    # Zeige das Passwort-Eingabefeld
    st.text_input("Passwort eingeben:", type="password", key="password")

    if st.button("Bestätigen"):
        if st.session_state.password == PASSWORD:
            st.session_state.password_correct = True
            st.success("Zugriff gewährt!")
            return True
        else:
            st.session_state.password_correct = False
            st.error("Falsches Passwort.")

    return False


