import streamlit as st

from config import Config


def init_user_profile_management(user_profile_management, update_user_profile_callback=None):
    user_profile_management.write(""" In order to have better personalised experience, please fill in your profile.""")
    col1, col2 = user_profile_management.columns(2)
    with user_profile_management.form("my_form"):
        first_name = col1.text_input("First Name", key="first_name")
        last_name = col2.text_input("Last Name", key="last_name")
        email = col1.text_input("Email", key="email")
        mobile_phone = col2.text_input("Mobile Phone", key="mobile")
        submitted = st.form_submit_button("Update")
        if submitted:
            Config.get_instance().set_config("user_profile", {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "mobile_phone": mobile_phone
            })

            if update_user_profile_callback:
                update_user_profile_callback()
