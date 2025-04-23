# Best Formation Generator with Player Position Prediction

This project generates the best formation for the selected 11 players.

Also this project predicts a player's **Position Group** (e.g., FW, MF, DF, GK), detailed **Position** (e.g., ST, CB), and **Overall Rating (OVR)** based on the player's stats. The workflow is divided into multiple scripts, each serving a distinct purpose.

## Scripts Overview

- **predict_position_grouped.py**  
  Trains a classification model (e.g., RandomForestClassifier) to classify a player into a Position Group (FW, MF, DF, GK).

- **predict_position.py**  
  Trains a classification model to predict a player’s detailed Position (ST, CB, etc.).

- **predict_ovr.py**  
  Trains multiple regression models (one per Position) to predict a player’s OVR based on their stats when placed in a specific Position.

- **main.py**  
  Combines the above modules to:

  - Predict a new player's Position Group.
  - Predict the detailed Position.
  - Compute the OVR for the predicted (or user-overridden) Position.

  The script also continuously prompts the user to view OVR predictions for alternative positions until the user chooses to exit.

Start server with FasAPI:
uvicorn main:app --reload
Start client: npm start
