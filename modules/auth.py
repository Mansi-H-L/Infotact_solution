import streamlit as st
import pandas as pd
import os

USER_DB = "user_db.csv"

def load_users():
    if os.path.exists(USER_DB):
        return pd.read_csv(USER_DB)
    else:
        return pd.DataFrame(columns=["username", "password", "role"])

def save_user(username, password, role):
    df = load_users()
    new_user = pd.DataFrame([[username, password, role]], columns=["username", "password", "role"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_DB, index=False)

def login_ui():
    st.title("User Authentication")

    option = st.radio("Choose an option", ["Login", "Sign Up"])

    if option == "Login":
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if not username or not password:
                st.warning("Please fill in all fields.")
            else:
                users = load_users()
                user = users[(users["username"] == username) & (users["password"] == password)]
                if not user.empty:
                    st.session_state['user'] = {
                        'name': username,
                        'role': user.iloc[0]['role']
                    }
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
                    if not user.empty:
                        st.session_state['user'] = {
                        'name': username,
                        'role': user.iloc[0]['role']
                }
                    st.session_state['page'] = "Task Management"  # Redirect here
                    st.rerun()


    elif option == "Sign Up":
        new_username = st.text_input("New Username", key="signup_user")
        new_password = st.text_input("New Password", type="password", key="signup_pass")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_conf")
        role = st.selectbox("Select Role", ["Employee", "Manager", "Admin"])

        if st.button("Register"):
            if not new_username or not new_password or not confirm_password:
                st.warning("Please fill in all fields.")
            elif new_password != confirm_password:
                st.warning("Passwords do not match.")
            elif new_username in load_users()['username'].values:
                st.warning("Username already exists.")
            else:
                save_user(new_username, new_password, role)
                st.success("User registered successfully!")
                st.session_state['user'] = {
                    'name': new_username,
                    'role': role
                }
                st.rerun()
