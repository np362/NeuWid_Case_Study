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
   
   #Lösung, falls zwei gleiche Namen
   #Personen alphabetisch sortieren
   
   print("Tab2")
   st.header("Personenverwaltung")
   
   option = st.selectbox( 'Wähle eine Option aus:', ('Create a user', 'Remove a user', 'Show all users') )

   if option == "Create a user":
      
      firstname = st.text_input("Geben Sie hier den Vorname ein: ")
      lastname = st.text_input("Geben Sie hier den Nachnamen ein: ")
      name = firstname + " " + lastname 
      email = firstname + "." + lastname + "@mci.edu"
      
      newdata = {name : email}
      
      try:

         # Open existing json and adds data
         with open('user.json', 'r+', encoding='utf-8') as file:
            data = json.load(file)
            if name != "":
               st.write("New user: " + name + " : " + email)

            if st.button("Add"):
               # add new data
               data['Users'][name] = email
               
               # set datapoint to the start and overwrites current data with new data
               file.seek(0)
               json.dump(data, file, ensure_ascii=False, indent=4)
               file.truncate()

      except FileNotFoundError:
         print("File not found")
      
      

   if option == "Remove a user":

      firstname = st.text_input("Add first name: ")
      lastname = st.text_input("Add surname: ")
      name = firstname + " " + lastname
      
      try:
         with open('user.json', 'r+', encoding='utf-8') as file:
            data = json.load(file)
 
            if st.button("Remove"):
               if name in data["Users"]:
                  del data["Users"][name]
                  st.write("The user has been deleted")
               else:
                  st.write("The user does not exist")

               file.seek(0)
               json.dump(data, file, ensure_ascii=False, indent=4)
               file.truncate()
      except FileNotFoundError:
         print("File not found")


   if option == "Show all users":

      #unicode transformation format 8 bit ist ein Zeichencodierungssystem zum Übertragen von Zeichen in verschiedenen Schriftsystemen
      try:
         with open('user.json', 'r', encoding='utf-8') as file:
            userdict = {}
            data = json.load(file)
            userdict = data['Users']
            sortedusers = {k : userdict[k] for k in sorted(userdict)}
         #st.write(data)
         for i in sortedusers:
            st.write(i + " : " + sortedusers[i])
            print(sortedusers)
      except FileNotFoundError:
         print("File not found")

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


