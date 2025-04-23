# Football AI Genraltor

This project generates the best formation for the selected 11 players based on their provided stats. It also allows users to generate their own FC25 stats. The project includes backend scripts for machine learning models and a frontend for user interaction.

---

## Features

- Predicts the best formation for a team of 11 players.
- Classifies players into position groups (FW, MF, DF, GK) and detailed positions (ST, CB, etc.).
- Predicts player OVR (Overall Rating) based on their stats and position.
- Provides a user-friendly interface for interacting with the system.

---

## Project Structure

### Backend Scripts

#### Prediction model

- **`predict_position_grouped.py`**  
  Trains a classification model (e.g., `RandomForestClassifier`) to classify a player into a Position Group (FW, MF, DF, GK).

- **`predict_position.py`**  
  Trains a classification model to predict a player’s detailed Position (e.g., ST, CB, etc.).

- **`predict_ovr.py`**  
  Trains multiple regression models (one per Position) to predict a player’s OVR based on their stats when placed in a specific Position.

- **`train_models.py`**  
  Combine and runs all the prediction files above and save it to a Pickle file.

---

### Formation Algorithm

- **`formation.py`**
  Saved 10 popular position into nodes and used it when needed

---

- **`optimal_team_formation.py`**
  This module recommends the best football formation by maximizing total OVR based on each player's predicted performance across positions.

  Features

  - Predicts per-position OVR for each player

  - Evaluates all predefined formations

  - Uses Hungarian algorithm to assign optimal positions

  Returns:

  - Best formation

  - Total team OVR

  - Player-position assignments

  - Ranked list of all formations

---

- **`main.py`**  
  A FastAPI backend for:

  - Predicting player position, position group, and OVR from input stats

  - Recommending the optimal formation for a given list of 11 players

## How to Start

_Install requirements_ \
pip3 install -r requirements.txt

_Set up Database_ \
cd Data python3 db_setup.py

_Train models and save it as .pkl_ \
cd Backend/prediction_model python3 train_models.py

_Run Backend and Server_ \
cd Backend uvicorn main:app --reload \
cd client npm start
