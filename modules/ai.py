import streamlit as st
import pandas as pd
from datetime import datetime
from textblob import TextBlob
import matplotlib.pyplot as plt

# 1. Sentiment Analysis
def sentiment_analysis_ui():
    st.subheader("🔍 Sentiment Analysis")
    text = st.text_area("Enter task description or comment")

    if st.button("Analyze Sentiment"):
        if text:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity

            if polarity > 0.1:
                sentiment = "Positive"
            elif polarity < -0.1:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"

            st.write(f"**Sentiment:** {sentiment}")
            st.write(f"**Polarity Score:** {polarity:.2f}")
        else:
            st.warning("Please enter some text.")

# 2. Task Optimization
def optimize_tasks(task_df):
    def urgency_score(desc):
        polarity = TextBlob(desc).sentiment.polarity
        return max(0, 1 + polarity)  # Inverse urgency (lower = more urgent)

    task_df['urgency'] = task_df['description'].apply(urgency_score)
    task_df['days_left'] = (pd.to_datetime(task_df['deadline']) - datetime.now()).dt.days
    task_df['priority_score'] = 1 / (task_df['urgency'] + task_df['days_left'] + 1)
    task_df = task_df.sort_values(by="priority_score", ascending=False)
    return task_df

def task_optimization_ui():
    st.subheader("⚙️ Task Optimization")
    uploaded = st.file_uploader("Upload CSV file with columns: title, description, deadline")

    if uploaded:
        df = pd.read_csv(uploaded)
        st.write("📋 Original Task Data")
        st.dataframe(df)

        try:
            df['deadline'] = pd.to_datetime(df['deadline'])
            optimized_df = optimize_tasks(df)
            st.success("✅ Tasks prioritized successfully!")
            st.dataframe(optimized_df)
        except Exception as e:
            st.error(f"Error processing file: {e}")

# 3. Automated Scheduling
def generate_schedule(task_df, work_hours=8):
    schedule = []
    hour = 9  # Start at 9 AM

    for _, task in task_df.iterrows():
        if hour >= 17:
            break
        task_duration = 1  # Assume 1 hour per task
        start_time = f"{hour}:00"
        end_time = f"{hour + task_duration}:00"
        schedule.append(f"{start_time} - {end_time}: {task['title']}")
        hour += task_duration

    return schedule

def run_scheduler_ui():
    st.subheader("📅 Automated Scheduling")
    uploaded = st.file_uploader("Upload CSV with columns: title, description, deadline", key="schedule")

    if uploaded:
        df = pd.read_csv(uploaded)
        try:
            df['deadline'] = pd.to_datetime(df['deadline'])
            optimized = optimize_tasks(df)
            schedule = generate_schedule(optimized)

            st.success("🗓 Suggested Schedule")
            for item in schedule:
                st.write(f"✅ {item}")
        except Exception as e:
            st.error(f"Error processing schedule: {e}")

# 4. Predictive Analytics
def predictive_analytics_ui():
    st.subheader("📈 Predictive Analytics")
    uploaded = st.file_uploader("Upload completed tasks CSV with column: completion_date", key="predictive")

    if uploaded:
        df = pd.read_csv(uploaded)
        try:
            df['completion_date'] = pd.to_datetime(df['completion_date'])
            daily = df.groupby(df['completion_date'].dt.date).size()

            st.line_chart(daily)
            avg = daily.mean()
            st.success(f"📊 Average tasks completed per day: {avg:.2f}")

            if avg < 3:
                st.warning("Consider optimizing task loads or reducing bottlenecks.")

        except Exception as e:
            st.error(f"Error analyzing completion data: {e}")
# modules/ai.py

import streamlit as st
import pandas as pd
from modules.ml_model import train_task_model

def render_ai_page():
    st.subheader("📊 Predictive Task Completion (ML Model)")

    uploaded = st.file_uploader("Upload task dataset with 'created_at', 'deadline', 'completed_at', 'description' columns")

    if uploaded:
        df = pd.read_csv(uploaded)
        
        with st.spinner("Training model..."):
            model, report = train_task_model(df)
        
        st.success("Model trained!")
        st.write("📈 Classification Report:")
        st.json(report)

# Main tab layout
def run_ai_tools():
    st.title("🤖 AI Tools")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Sentiment Analysis", 
        "Task Optimization", 
        "Automated Scheduling", 
        "Predictive Analytics"
    ])

    with tab1:
        sentiment_analysis_ui()

    with tab2:
        task_optimization_ui()

    with tab3:
        run_scheduler_ui()

    with tab4:
        predictive_analytics_ui()
