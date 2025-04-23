import sqlite3
import pandas as pd

def create_and_populate_db():
    
    db_file = 'players.db'
    df = pd.read_csv('player_data/data_updated.csv')
    
    # connect to SQLite
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # create player table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS players (
        Name TEXT,
        OVR REAL,
        PAC REAL,
        SHO REAL,
        PAS REAL,
        DRI REAL,
        DEF REAL,
        PHY REAL,
        Acceleration REAL,
        "Sprint Speed" REAL,
        Positioning REAL,
        Finishing REAL,
        "Shot Power" REAL,
        "Long Shots" REAL,
        Volleys REAL,
        Penalties REAL,
        Vision REAL,
        Crossing REAL,
        "Free Kick Accuracy" REAL,
        "Short Passing" REAL,
        "Long Passing" REAL,
        Curve REAL,
        Dribbling REAL,
        Agility REAL,
        Balance REAL,
        Reactions REAL,
        "Ball Control" REAL,
        Composure REAL,
        Interceptions REAL,
        "Heading Accuracy" REAL,
        "Def Awareness" REAL,
        "Standing Tackle" REAL,
        "Sliding Tackle" REAL,
        Jumping REAL,
        Stamina REAL,
        Strength REAL,
        Aggression REAL,
        Position TEXT,
        Position_Grouped TEXT,
        "Weak foot" REAL,
        "Skill moves" REAL,
        "Preferred foot" TEXT,
        Height REAL,
        Weight REAL,
        Age INTEGER,
        Nation TEXT,
        League TEXT,
        Team TEXT,
        "play style" TEXT,
        "Alternative positions" TEXT,
        "GK Diving" REAL,
        "GK Handling" REAL,
        "GK Kicking" REAL,
        "GK Positioning" REAL,
        "GK Reflexes" REAL
    )
    '''
    cursor.execute(create_table_query)
    conn.commit()
    
    # save DataFrame's data into players table
    df.to_sql('players', conn, if_exists='append', index=False)
    
    # check connection bvy printing out the sample data
    sample_query = "SELECT * FROM players LIMIT 5;"
    sample_data = pd.read_sql_query(sample_query, conn)
    print("sample data:")
    print(sample_data)
    
    # end connection
    conn.close()

if __name__ == '__main__':
    create_and_populate_db()
