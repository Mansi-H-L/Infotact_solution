import streamlit as st
from modules import auth, task, dashboard, ai

st.set_page_config(page_title="AI Task Manager", layout="wide")

# Initialize session state
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = "Login"
from modules.ai import render_ai_page

if 'page' == "AI Features":
    render_ai_page()

# Redirect after login/signup
if st.session_state['user']:
    st.sidebar.title(f"Welcome, {st.session_state['user']['name']}")
    nav = st.sidebar.radio("Navigation", ["Task Management", "Dashboard", "AI Tools", "Logout"])

    if nav == "Logout":
        st.session_state['user'] = None
        st.session_state['page'] = "Login"
        st.rerun()

    elif nav == "Task Management":
        st.session_state['page'] = "Task Management"
        task.task_ui()

    elif nav == "Dashboard":
        st.session_state['page'] = "Dashboard"
        dashboard.show_dashboard()

    elif nav == "AI Tools":
        st.session_state['page'] = "AI Tools"
        ai.run_ai_tools()

else:
    auth.login_ui()
