# modules/ml_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from textblob import TextBlob

def extract_features(df):
    df['description_length'] = df['description'].apply(len)
    df['sentiment'] = df['description'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['days_to_deadline'] = (pd.to_datetime(df['deadline']) - pd.to_datetime(df['created_at'])).dt.days
    df['completed_on_time'] = (pd.to_datetime(df['completed_at']) <= pd.to_datetime(df['deadline'])).astype(int)
    
    if 'assigned_to' in df.columns:
        df['assigned_to_encoded'] = LabelEncoder().fit_transform(df['assigned_to'])
    else:
        df['assigned_to_encoded'] = 0  # default value if not present

    return df[['description_length', 'sentiment', 'days_to_deadline', 'assigned_to_encoded']], df['completed_on_time']

def train_task_model(df):
    X, y = extract_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    return model, report
