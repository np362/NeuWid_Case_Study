import streamlit as st
from users import User

tab1, tab2, tab3 = st.tabs(["Geräte", "Nutzer", "Reservierung"])
print("Hello from test branch")

if "sb_current_device" not in st.session_state:
    st.session_state.sb_current_device = ""

    st.write("# Test")


# Tabs
with tab1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

   # Eine Überschrift der ersten Ebene
   st.write("# Gerätemanagement")

    # Eine Überschrift der zweiten Ebene
   st.write("## Geräteauswahl")

    # Eine Auswahlbox mit hard-gecoded Optionen, das Ergebnis

   st.session_state.sb_current_device = st.selectbox(label='Gerät auswählen',
            options = ["Gerät_A", "Gerät_B"])

   st.write(F"Das ausgewählte Gerät ist {st.session_state.sb_current_device}")

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


