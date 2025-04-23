import os
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

# 기본 설정
base_dir = os.path.dirname(__file__)
db_file = os.path.abspath(os.path.join(base_dir, "..", "..", "Data", "players.db"))
conn = sqlite3.connect(db_file)
df = pd.read_sql_query("SELECT * FROM players", conn)
conn.close()

selected_features = [ 
    'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'Acceleration', 'Sprint Speed', 'Positioning',
    'Finishing', 'Shot Power', 'Long Shots', 'Volleys', 'Penalties', 'Vision', 'Crossing',
    'Free Kick Accuracy', 'Short Passing', 'Long Passing', 'Curve', 'Dribbling', 'Agility',
    'Balance', 'Reactions', 'Ball Control', 'Composure', 'Interceptions', 'Heading Accuracy',
    'Def Awareness', 'Standing Tackle', 'Sliding Tackle', 'Jumping', 'Stamina', 'Strength',
    'Aggression', 'Skill moves', 'Weak foot', 'Height', 'GK Diving', 'GK Handling',
    'GK Kicking', 'GK Positioning', 'GK Reflexes'
]

X = df[selected_features]

# ========== 1. Position_Grouped ==========
y_pg = df["Position_Grouped"]
X_train, _, y_train, _ = train_test_split(X, y_pg, test_size=0.2, random_state=42)
pg_model = Pipeline([("scaler", StandardScaler()), ("clf", RandomForestClassifier(n_estimators=100, random_state=42))])
pg_model.fit(X_train, y_train)
joblib.dump(pg_model, os.path.join(base_dir, "position_grouped_model.pkl"))
print("✅ Position_Grouped model saved")

# ========== 2. Position ==========
y_pos = df["Position"]
X_train, _, y_train, _ = train_test_split(X, y_pos, test_size=0.2, random_state=42)
pos_model = Pipeline([("scaler", StandardScaler()), ("clf", RandomForestClassifier(n_estimators=100, random_state=42))])
pos_model.fit(X_train, y_train)
joblib.dump(pos_model, os.path.join(base_dir, "position_model.pkl"))
print("✅ Position model saved")

# ========== 3. OVR per Position ==========
os.makedirs(os.path.join(base_dir, "ovr_models"), exist_ok=True)
target = "OVR"
positions = df["Position"].unique()

for pos in positions:
    pos_data = df[df["Position"] == pos]
    if len(pos_data) < 30:
        continue
    X = pos_data[selected_features]
    y = pos_data[target]
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    model_path = os.path.join(base_dir, "ovr_models", f"{pos}.pkl")
    joblib.dump(model, model_path)
    print(f"✅ OVR model saved: {pos}")
