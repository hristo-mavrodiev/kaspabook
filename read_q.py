import pandas as pd
t = pd.read_json("t.json")
import json
# load data using Python JSON module
with open('t.json','r') as f:
    data = json.loads(f.read())# Flatten data
df_nested_list = pd.json_normalize(data, record_path =['data'])
print(df_nested_list)