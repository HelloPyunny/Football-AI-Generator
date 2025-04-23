# predict_position_grouped.py
import os
import sqlite3
import numpy as np
import pandas as pd
import joblib

'''
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
'''


# load data using CSV
# df = pd.read_csv('../../Data/player_data/data_updated.csv')

base_dir = os.path.dirname(__file__)
model = joblib.load(os.path.join(base_dir, "position_grouped_model.pkl"))

'''
db_file = os.path.abspath(os.path.join(base_dir, "..", "..", "Data", "players.db"))

conn = sqlite3.connect(db_file)
df = pd.read_sql_query("SELECT * FROM players", conn)
conn.close()
'''


# select the features for ML
selected_features = [ 
    'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'Acceleration', 'Sprint Speed', 'Positioning',
    'Finishing', 'Shot Power', 'Long Shots', 'Volleys', 'Penalties', 'Vision', 'Crossing',
    'Free Kick Accuracy', 'Short Passing', 'Long Passing', 'Curve', 'Dribbling', 'Agility',
    'Balance', 'Reactions', 'Ball Control', 'Composure', 'Interceptions', 'Heading Accuracy',
    'Def Awareness', 'Standing Tackle', 'Sliding Tackle', 'Jumping', 'Stamina', 'Strength',
    'Aggression', 'Skill moves', 'Weak foot', 'Height', 'GK Diving', 'GK Handling',
    'GK Kicking', 'GK Positioning', 'GK Reflexes'
]

'''
# set target
target = 'Position_Grouped'

# Set X and y
X = df[selected_features]
y = df[target]

# train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])
pipeline.fit(X_train, y_train)

print(f"Sample size of [Position_Grouped] training: {len(X_train)}")

# import statements
from sklearn.metrics import accuracy_score

y_pred = pipeline.predict(X_test)  # predict test data
accuracy = accuracy_score(y_test, y_pred)  # calculate accuracy
print(f"model accuracy: {accuracy:.4f}") 

def predict_position_grouped(new_player_stats: dict):
    name = list(new_player_stats.keys())[0]
    stats = new_player_stats[name]
    
    # change data type to integer
    stats = {key: int(value) for key, value in stats.items()}
    
    new_data = pd.DataFrame([stats])
    prediction = pipeline.predict(new_data[selected_features])[0]
    
    return name, prediction
'''

def predict_position_grouped(new_player_stats: dict):
    name = list(new_player_stats.keys())[0]
    stats = {k: float(v) for k, v in new_player_stats[name].items()}
    df = pd.DataFrame([stats])
    pred = model.predict(df[selected_features])[0]
    return name, pred

# 예시 사용
if __name__ == '__main__':
    sample_input = {
    "Kylian Mbappé": {
        "PAC": 97.0, "SHO": 90.0, "PAS": 80.0, "DRI": 92.0, "DEF": 36.0, "PHY": 78.0, 
        "Acceleration": 97.0, "Sprint Speed": 97.0, "Positioning": 93.0, "Finishing": 94.0, 
        "Shot Power": 90.0, "Long Shots": 83.0, "Volleys": 84.0, "Penalties": 84.0, 
        "Vision": 83.0, "Crossing": 78.0, "Free Kick Accuracy": 69.0, "Short Passing": 86.0, 
        "Long Passing": 71.0, "Curve": 80.0, "Dribbling": 93.0, "Agility": 93.0, 
        "Balance": 82.0, "Reactions": 93.0, "Ball Control": 92.0, "Composure": 88.0, 
        "Interceptions": 38.0, "Heading Accuracy": 73.0, "Def Awareness": 26.0, 
        "Standing Tackle": 34.0, "Sliding Tackle": 32.0, "Jumping": 88.0, "Stamina": 88.0, 
        "Strength": 77.0, "Aggression": 64.0, "Skill moves": 5.0, "Weak foot": 4.0, "Height": 182.0,
        "GK Diving": 0.0, "GK Handling": 0.0, "GK Kicking": 0.0, 
        "GK Positioning": 0.0, "GK Reflexes": 0.0
    }
    }
    name, result = predict_position_grouped(sample_input)
    print(f"선수 이름: {name}, 예측된 Position_Grouped: {result}")