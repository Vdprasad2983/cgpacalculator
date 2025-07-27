# main.py

import streamlit as st
from streamlit_option_menu import option_menu
import datetime

import pandas as pd
import random
import ast

from utils.s3_utils import read_user_csv_from_s3, write_user_csv_to_s3, create_user_csv_in_s3
from utils.email_utils import send_email
from utils.cgpa_utils import calculate_cgpa, calculate_percentage

# Initialize session state
for key in ["otp", "otp_verified", "otp_entered", "auth", "username","college"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "auth" else 0

def generate_otp():
    st.session_state.otp = ''.join(str(random.randint(0, 9)) for _ in range(6))

def register():
    st.title("🎓 CGPA Calculator - Registration")
    existing_details = read_user_csv_from_s3("details")
    existing_users = existing_details["username"] if existing_details is not None else []

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    password1 = st.text_input("Re-enter Password", type="password")
    rollnumber=st.text_input("Enter your roll number")
    email = st.text_input("Email")
    check_aditya=st.radio("confirm your college",["Yes, I am from aditya college of engineering and technology","No, I am from another college"])
    if check_aditya=="No, I am from another college":
        college=st.text_input("enter your college name")
    else:
        college="Aditya College of Engineering and Technology"
    mobile=st.text_input("Enter your mobile number")
    dob = st.date_input("Date of Birth", min_value=datetime.date(1900, 1, 1))
    date = datetime.datetime.now()

    if st.button("Register"):
        if not username or not password or not email:
            st.warning("Fill all required fields.")
            return
        if password != password1:
            st.warning("Passwords do not match.")
            return
        if username in existing_users:
            st.warning("Username already exists.")
            return

        generate_otp()
        send_email("OTP Verification", email, f"Your OTP: {st.session_state.otp}")
        st.success("OTP sent to your email.")
        create_user_csv_in_s3(username)

        
        st.session_state.username = username
        st.session_state.auth = 0
        st.session_state.otp_verified = False

    if st.session_state.otp and not st.session_state.otp_verified:
        st.session_state.otp_entered = st.text_input("Enter OTP", max_chars=6)
        if st.button("Verify OTP"):
            if st.session_state.otp_entered == st.session_state.otp:
                
                new_data = {
                    "username": st.session_state.username,
                    "rollnumber":rollnumber,
                    "password": password,
                    "dob": dob,
                    "email": email,
                    "college name":college,
                    "mobile":mobile,
                    "date":date
                }
                df_new = pd.DataFrame([new_data])
                df_existing = existing_details if existing_details is not None else pd.DataFrame()
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                write_user_csv_to_s3("details", df_combined)
                st.session_state.otp_verified = True
                send_email("Registration Successful", email, f"Welcome {username}!")
                st.success("Registration complete!")
            else:
                st.error("Incorrect OTP")

def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    details = read_user_csv_from_s3("details")
    if st.button("Login"):
        user_row = details[details["username"] == username]
        if user_row.empty:
            st.warning("User not found.")
        elif user_row["password"].iloc[0] != password:
            st.warning("Incorrect password.")
        else:
            st.session_state.auth = 1
            st.session_state.username = username
            st.session_state.college=user_row["college name"].iloc[0]
            st.success("Login successful!")
            st.rerun()
            st.balloons()


def dashboard():
    from add_modify_see import add_data, modify_data, see_data

    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("Logout"):
        for key in ["auth", "username", "otp", "otp_verified", "otp_entered","college"]:
            st.session_state[key] = None if key != "auth" else 0
        st.rerun()

    choice = option_menu(None, ["Add Data", "Modify Data", "See Results"], orientation="horizontal")
    if choice == "Add Data":
        add_data(st.session_state.username)
    elif choice == "Modify Data":
        modify_data(st.session_state.username)
    elif choice == "See Results":
        see_data(st.session_state.username)

# Main App Logic
st.set_page_config(page_title="CGPA Calculator",page_icon="🧮")

if st.session_state.auth == 0:
    page = option_menu(None, ["Register", "Login"], orientation="horizontal")
    if page == "Register":
        register()
    else:
        login()
else:
    dashboard()
