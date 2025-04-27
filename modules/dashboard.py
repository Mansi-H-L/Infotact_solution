import streamlit as st
import pandas as pd
from db import tasks_collection

def show_dashboard():
    st.title("📊 Dashboard")

    tasks = list(tasks_collection.find({"user": st.session_state['user']['name']}))

    if not tasks:
        st.info("No tasks available to show on the dashboard.")
        return

    df = pd.DataFrame(tasks)
    df['deadline'] = pd.to_datetime(df['deadline'])

    col1, col2 = st.columns(2)

    with col1:
        status_counts = df['status'].value_counts()
        st.subheader("Task Status Overview")
        st.bar_chart(status_counts)

    with col2:
        priority_counts = df['priority'].value_counts()
        st.subheader("Task Priority Distribution")
        st.bar_chart(priority_counts)

    st.subheader("📅 Deadlines Overview")
    deadline_counts = df.groupby(df['deadline'].dt.date).size()
    st.line_chart(deadline_counts)
# modules/dashboard.py

import streamlit as st
import pandas as pd
from db import tasks_collection
from datetime import datetime


def render_dashboard_page(current_user):
    st.title("📊 Task Dashboard")

    tasks = list(tasks_collection.find({}))
    if not tasks:
        st.info("No tasks available.")
        return

    df = pd.DataFrame(tasks)

    # Convert string dates to datetime
    for col in ['created_at', 'deadline', 'completed_at']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    st.subheader("📌 All Tasks")
    st.dataframe(df[['title', 'assigned_to', 'status', 'priority', 'deadline']])

    # Performance metrics for individuals
    st.subheader("📈 Team Member Performance")
    performance_df = df[df['status'] == 'Completed'].groupby('assigned_to').size().reset_index(name='Completed Tasks')
    st.bar_chart(performance_df.set_index('assigned_to'))

    # Task bottleneck identification
    st.subheader("🚨 Bottlenecks & Trends")
    if 'status' in df.columns:
        bottleneck_df = df.groupby('status').size().reset_index(name='Count')
        st.bar_chart(bottleneck_df.set_index('status'))

    # Task overdue analysis
    st.subheader("⏰ Overdue Tasks")
    now = datetime.now()
    if 'deadline' in df.columns and 'status' in df.columns:
        overdue_df = df[(df['deadline'] < now) & (df['status'] != 'Completed')]
        st.write(overdue_df[['title', 'assigned_to', 'deadline', 'status']])
