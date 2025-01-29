import json
import streamlit as st
from queries import find_devices
from devices import Device
from startbildschirm import check_password
from users import User
from reservations import Reservation
from maintenance import Maintenance
from datetime import datetime

if check_password():
    tab1, tab2, tab3, tab4 = st.tabs(["Geräte", "Nutzer", "Reservierungssystem", "Wartungs-Management"])

    if "sb_current_device" not in st.session_state:
        st.session_state.sb_current_device = ""

    # Tabs
    with tab1:
        st.title("Geräte-Verwaltung")

        devices_in_db = find_devices()
        st.subheader("Gerät ändern")
        if devices_in_db:
            current_device_name = st.selectbox(
                'Gerät auswählen',
                options=devices_in_db, key="sbDevice")

            if current_device_name in devices_in_db:
                loaded_device = Device.find_by_attribute("device_name", current_device_name)
                if loaded_device:
                    st.write(f"Loaded Device: {loaded_device}")
                else:
                    st.error("Device not found in the database.")

                with st.form("Device"):
                    st.write(loaded_device.device_name)

                    text_input_val = st.text_input("Geräte-Verantwortlicher", value=loaded_device.managed_by_user_id)
                    loaded_device.set_managed_by_user_id(text_input_val)

                    # Every form must have a submit button.
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        loaded_device.store_data()
                        st.write("Data stored.")
                        st.rerun()
            else:
                st.error("Selected device is not in the database.")


            st.subheader("Gerät hinzufügen")        
            with st.form("add_device"):
            
                new_device_name = st.text_input("Gerätename")
                new_managed_by_user_id = st.text_input("Verantwortlicher")
                new_device = Device(new_device_name, new_managed_by_user_id)

                submit_device = st.form_submit_button("Gerät hinzufügen")
                if submit_device:
                    st.write("Gerät hinzugefügt.")
                    new_device.store_data()
                    st.rerun()

            st.subheader("Gerät entfernen")
            remove_device_name = current_device_name
            device_to_remove = Device.find_by_attribute("device_name", remove_device_name)
            if st.button("Gerät entfernen"):
                try:
                    device_to_remove.delete()
                    st.success(f"Gerät {remove_device_name} entfernt.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Fehler beim Entfernen des Geräts: {e}")

        else:
            st.write("No devices found.")
            st.stop()

    with tab2:
        
        
        print("Tab2")
        st.header("Personnel managment")
        
        option = st.selectbox( 'Choose an option:', ('Create a user', 'Remove a user', 'Show all users') )

        if option == "Create a user":
            
            firstname = st.text_input("Enter the first name: ")
            surname = st.text_input("Enter the surname: ")
            name = firstname + " " + surname 
            email = firstname + "." + surname + "@mci.edu"
            
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
            surname = st.text_input("Add surname: ")
            name = firstname + " " + surname
            
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
        st.title("Reservierungs-Verwaltung")

        if st.button("Reservierungen anzeigen"):
            st.subheader("Reservierungen")
            reservations = Reservation.get_all_reservations()
            if reservations:
                import pandas as pd
                df = pd.DataFrame(reservations)
                st.dataframe(df)
            else:
                st.write("Keine Reservierung gefunden.")

        st.write("---")

        st.subheader("Neue Reservierung hinzufügen")
        with st.form("add_reservation"):
            device_id = st.text_input("Geräte-ID")
            user_id = st.text_input("Nutzer-ID")
            start_time_date = st.date_input("Startzeit Datum", min_value=None, max_value=None)
            start_zeit = st.time_input("Startzeit Uhrzeit")
            start_time = datetime.combine(start_time_date, start_zeit).strftime("%Y-%m-%d %H:%M:%S")
            end_time_date = st.date_input("Endzeit Datum", min_value=None, max_value=None)
            end_zeit = st.time_input("Endzeit Uhrzeit")
            end_time = datetime.combine(end_time_date, end_zeit).strftime("%Y-%m-%d %H:%M:%S")

            submitted = st.form_submit_button("Reservierung hinzufügen")
            if submitted:
                Reservation.add_reservation(device_id, user_id, start_time, end_time)
                st.write("Reservierung hinzugefügt.")
                st.rerun()
            else:
                st.write("Bitte fülle alle Felder aus.")

        st.write("---")

        st.subheader("Reservierung entfernen")
        remove_id = st.number_input("Reservierungs-ID", min_value=1, max_value=len(Reservation.get_all_reservations()), step=1)
        if st.button("Reservierung entfernen"):
            try:
                Reservation.delete_reservation(remove_id)
                st.success(f"Reservierung {remove_id} entfernt.")
            except Exception as e:
                st.error(f"Fehler beim Entfernen der Reservierung: {e}")

    with tab4:
        st.title("Wartungs-Management")
        if st.button("Wartungen anzeigen"):
            st.subheader("Wartungen")
            device_maintenance = Maintenance.show_maintenance()
            if device_maintenance:
                import pandas as pd
                df2 = pd.DataFrame(device_maintenance)
                st.dataframe(df2)
            else:
                st.write("Keine Wartung gefunden.")

        new_device_id = st.number_input("Geräte-ID", min_value=1, max_value=len(Maintenance.show_maintenance()), step=1)
        if st.button("Nächste Wartung anzeigen"):
            next_maintenance = Maintenance.maintenances[new_device_id-1]["start_time"]
            if next_maintenance:
                st.write(f"Nächste Wartung: {next_maintenance}")
            else:
                st.write("Keine Wartung gefunden.")

        if st.button("Kosten anzeigen"):
            cost = Maintenance.maintenances[new_device_id-1]["cost"]
            if cost:
                st.write(f"Kosten: {cost}€")

        if st.button("Intervall zur nächsten Wartung anzeigen"):
            intervall_next_maintenance = Maintenance.calculate_interval_until_maintenance(new_device_id)
            if intervall_next_maintenance:
                st.write(f"Nächste Wartung in {intervall_next_maintenance} Tagen.")
            else:
                st.write("Keine Wartung gefunden.")

        st.write("---")

        st.subheader("Wartung bearbeiten")
        with st.form("configure_maintenance"):
            new_device_id = st.number_input("Geräte-ID", min_value=1, max_value=len(Maintenance.show_maintenance()), step=1)
            new_start_date = st.date_input("Startzeit Datum", min_value=None, max_value=None)
            new_start_zeit = st.time_input("Startzeit Uhrzeit")
            new_start_time = datetime.combine(new_start_date, new_start_zeit).strftime("%Y-%m-%d %H:%M:%S")
            new_end_date = st.date_input("Endzeit Datum", min_value=None, max_value=None)
            new_end_zeit = st.time_input("Endzeit Uhrzeit")
            new_end_time = datetime.combine(new_end_date, new_end_zeit).strftime("%Y-%m-%d %H:%M:%S")
            new_cost = st.number_input("Kosten", step=0.50  )

            submit_configuration = st.form_submit_button("Wartung bearbeiten")
            if submit_configuration:
                try:
                    Maintenance.configure_maintenance(new_device_id, new_start_time, new_end_time, new_cost)
                    st.write("Wartung konfiguriert.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Fehler beim Konfigurieren der Wartung: {e}")

            

        st.write("---")

        if st.button("Quartalskosten anzeigen"):
            st.subheader("Quartalskosten")
            quarterly_costs = Maintenance.calculate_quarterly_costs()
            if quarterly_costs:
                st.write(f"Q1: {quarterly_costs:.2f}€")
            
            else:
                st.write("Keine Wartungskosten verfügbar.")



else:
    st.warning("Bitte gib das Passwort ein, um fortzufahren.")

