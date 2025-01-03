import streamlit as st
from queries import find_devices
from devices import Device
from startbildschirm import check_password
from users import User
from reservations import Reservation

if check_password():
    tab1, tab2, tab3 = st.tabs(["Geräte", "Nutzer", "Reservierung"])

    if "sb_current_device" not in st.session_state:
        st.session_state.sb_current_device = ""

    # Tabs
    with tab1:
        st.title("Geräte-Verwaltung")

        devices_in_db = find_devices()

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
        else:
            st.write("No devices found.")
            st.stop()

    with tab2:
        st.title("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

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
            start_time = st.text_input("Startzeit (Format: 2021-12-31 23:59:59)")
            end_time = st.text_input("Endzeit (Format: 2021-12-31 23:59:59)")

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


else:
    st.warning("Bitte gib das Passwort ein, um fortzufahren.")