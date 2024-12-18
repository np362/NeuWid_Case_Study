import streamlit as st
from queries import find_devices
from devices import Device
from users import User

tab1, tab2, tab3 = st.tabs(["Geräte", "Nutzer", "Reservierung"])

if "sb_current_device" not in st.session_state:
    st.session_state.sb_current_device = ""

    st.write("# Test")


# Tabs
with tab1:
   st.header("Geräteauswahl")

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
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)