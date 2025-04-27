import streamlit as st
from datetime import datetime
import pandas as pd
from db import tasks_collection
#from modules.db import tasks_collection



def task_ui():
    st.title("📝 Task Manager")

    with st.form("task_form"):
        title = st.text_input("Task Title", max_chars=100)
        description = st.text_area("Task Description")
        deadline = st.date_input("Deadline")
        status = st.selectbox("Status", ["To-Do", "In Progress", "Completed", "On-Hold"])
        priority = st.selectbox("Priority", ["Urgent", "High", "Medium", "Low"])
        submitted = st.form_submit_button("Add Task")

        if submitted:
            if not title or not description:
                st.warning("Please fill in all fields.")
            else:
                task = {
                    "title": title,
                    "description": description,
                    "deadline": deadline.strftime("%Y-%m-%d"),
                    "status": status,
                    "priority": priority,
                    "user": st.session_state['user']['name'],
                    "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                tasks_collection.insert_one(task)
                st.success("✅ Task added successfully!")

    # Show tasks for current user
    tasks = list(tasks_collection.find({"user": st.session_state['user']['name']}))
    if tasks:
        df = pd.DataFrame(tasks)
        df = df.drop(columns=["_id"])
        st.write("📋 Your Tasks")
        st.dataframe(df)
    else:
        st.info("No tasks found.")
