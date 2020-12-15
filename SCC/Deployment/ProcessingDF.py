import pandas as pd
df = pd.read_csv('./final.csv', encoding ='utf-8')

df_vodafone = df.query('named_entities.str.contains("vodafone")', engine='python')

#print(df.query('named_entities.str.contains("etisalat")', engine='python')
#print(df.query('named_entities.str.contains("orange")', engine='python'))