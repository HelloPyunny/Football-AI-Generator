# select_eleven.py

import os
import sqlite3

# 필요한 feature들
selected_features = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'Acceleration',
    'Sprint Speed', 'Positioning', 'Finishing', 'Shot Power', 'Long Shots',
    'Volleys', 'Penalties', 'Vision', 'Crossing', 'Free Kick Accuracy',
    'Short Passing', 'Long Passing', 'Curve', 'Dribbling', 'Agility',
    'Balance', 'Reactions', 'Ball Control', 'Composure', 'Interceptions',
    'Heading Accuracy', 'Def Awareness', 'Standing Tackle', 'Sliding Tackle',
    'Jumping', 'Stamina', 'Strength', 'Aggression', 'Skill moves',
    'Weak foot', 'Height']

# name, position도 같이 가져오기
all_needed_columns = ['name', 'Position'] + selected_features

base_dir = os.path.dirname(__file__)
db_file = os.path.abspath(os.path.join(base_dir, "..", "..", "Data", "players.db"))

def select_eleven_players(selected_player_names):
    if len(selected_player_names) != 11:
        raise ValueError("You must select exactly 11 players.")
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    quoted_columns = [f'"{col}"' for col in all_needed_columns]  # 모든 열 이름을 따옴표로 감싸기
    query = f"""
        SELECT {','.join(quoted_columns)}
        FROM players
        WHERE name IN ({','.join('?' * len(selected_player_names))})
        """

    cursor.execute(query, selected_player_names)
    selected_players = cursor.fetchall()

    # GK가 적어도 한 명은 있어야 함
    goalkeepers = [player for player in selected_players if player[1] == 'GK']
    if not goalkeepers:
        raise ValueError("At least one goalkeeper must be selected.")
    
    conn.close()
    return selected_players


# Example usage
if __name__ == "__main__":
    # Example selected player names (to be replaced with actual user input)
    selected_player_names = [
        "Julia Magerl", "Aoife Mannion", "Laura Martínez", "Amanda Mbadi", "Paula Monteagudo",
        "Juliette Mossard", "Marjolen Nekesa Wafula", "Nina Ngueleu", 
        "Bárbara Olivieri", "Cristina Roque", "Mar Segarra"
    ]

    try:
        selected_players = select_eleven_players(selected_player_names)
        print("Selected 11 players:")
        for player in selected_players:
            print(player)
    except ValueError as e:
        print(f"Error: {e}")