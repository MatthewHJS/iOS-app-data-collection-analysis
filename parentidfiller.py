
import pandas as pd

df1 = pd.read_csv('leaf_leaf_apps.csv')
df2 = pd.read_csv('leaf_leaf_apps1.csv')

last_column_name = df1.columns[-1]

df2[last_column_name] = df1[last_column_name]

df2.to_csv('file2_updated.csv', index=False)
