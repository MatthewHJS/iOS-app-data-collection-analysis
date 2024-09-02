import pandas as pd


'''
Merges all apps together 

'''

df1 = pd.read_csv('root_apps.csv')
df2 = pd.read_csv('leaf_apps.csv')
df3 = pd.read_csv('leaf_leaf_apps.csv')

df1 = df1.iloc[:, :6]
df2 = df2.iloc[:, :6]
df3 = df3.iloc[:, :6]

merged_df = pd.concat([df1, df2, df3], ignore_index=True)

merged_df.drop_duplicates(subset=merged_df.columns[0], keep='first', inplace=True)

merged_df.to_csv('all_apps.csv', index=False)

