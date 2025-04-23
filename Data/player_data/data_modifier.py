# data_modifier.py : file to modify csv files if there is something to change

import pandas as pd

# load csv
df = pd.read_csv('data_updated.csv')

# modification
df['Position_Grouped'] = df['Position_Grouped'].replace('ATT', 'FW')

# save the modified data
try:
    df.to_csv('data_updated.csv', index=False)
    print("Success")
except Exception as e:
    print(f"Error: {e}")