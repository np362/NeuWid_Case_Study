import json
import streamlit as st
from queries import find_devices
from devices import Device
import startbildschirm

from users import User
correctpassword = startbildschirm.check_password()

if correctpassword == True:
    st.title("Geheime Inhalte")
    st.write("Hier siehst du die Inhalte, die nur für autorisierte Benutzer zugänglich sind.")


tab1, tab2, tab3 = st.tabs(["Geräte", "Nutzer", "Reservierung"])

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

   #st.write(F"Das ausgewählte Gerät ist {st.session_state.sb_current_device}")

with tab2:
   """In this module are all the functions for managing the users
   A user has a name and an ID (E-mail)

   -creating a user
   -removing a user
   -showing all users

   The data of users is stored in the user.json file
   """
   print("Tab2")
   st.header("Personenverwaltung")
   
   option = st.selectbox( 'Wähle eine Option aus:', ('Create a user', 'Remove a user', 'Show all users') )

   if option == "Create a user":
      print("Option 1 wurde gewählt")
      
      vorname = st.text_input("Geben Sie hier den Vorname ein: ")
      nachname = st.text_input("Geben Sie hier den Nachnamen ein: ")
      name = vorname + " " + nachname 
      email = vorname + "." + nachname + "@mci.edu"
      
      neueDaten = {name : email}
      
      try:

         # Öffne die bestehende JSON-Datei und lade die Daten
         with open('user.json', 'r+', encoding='utf-8') as file:
            daten = json.load(file)
            if name != "":
               st.write("Neuer Nutzer: " + name + " : " + email)

            if st.button("Hinzufügen"):
               # Füge die neuen Daten hinzu
               daten['Users'][name] = email
               
               # Setze den Dateizeiger an den Anfang und überschreibe die Datei mit den aktualisierten Daten
               file.seek(0)
               json.dump(daten, file, ensure_ascii=False, indent=4)
               file.truncate()

      except FileNotFoundError:
         print("File nicht gefunden")
      
      

   if option == "Remove a user":

      vorname = st.text_input("Geben Sie hier den Vorname ein: ")
      nachname = st.text_input("Geben Sie hier den Nachnamen ein: ")
      name = vorname + " " + nachname
      # Öffne die bestehende JSON-Datei und lade die Daten
      try:
         with open('user.json', 'r+', encoding='utf-8') as file:
            daten = json.load(file)

            # Entferne das Element mit dem Schlüssel "Paul Neuner"
            
            if st.button("Entfernen"):
               if name in daten["Users"]:
                  del daten["Users"][name]
                  st.write("Der Benutzer wurde gelöscht")
               else:
                  st.write("Der Benutzer wurde nicht gefunden")

               # Setze den Dateizeiger an den Anfang und überschreibe die Datei mit den aktualisierten Daten
               file.seek(0)
               json.dump(daten, file, ensure_ascii=False, indent=4)
               file.truncate()
      except FileNotFoundError:
         print("File nicht gefunden")


   if option == "Show all users":
      #unicode transformation format 8 bit ist ein Zeichencodierungssystem zum Übertragen von Zeichen in verschiedenen Schriftsystemen
      print("Option 3 wurde gewählt")
      try:
         with open('user.json', 'r', encoding='utf-8') as file:
            mydict = {}
            data = json.load(file)
            mydict = data['Users']
           
         #st.write(data)
         for i in mydict:
            st.write(i + " : " + mydict[i])
      except FileNotFoundError:
         print("File nicht gefunden")

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


