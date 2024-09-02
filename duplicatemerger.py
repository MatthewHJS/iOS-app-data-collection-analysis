import pandas as pd

'''

duplicatemerger.py

Deletes one row if they are the same and merges their parents ID

'''

def merge_parent_ids(file_path):

    df = pd.read_csv(file_path, encoding='ISO-8859-1')

    merged_df = df.groupby(df.columns[0]).agg({df.columns[7]: lambda x: list(x)}).reset_index()

    df.drop_duplicates(subset=df.columns[0], keep='first', inplace=True)

    df = df.merge(merged_df, on=df.columns[0], suffixes=('', '_merged'))

    df[df.columns[7]] = df[df.columns[7] + '_merged']

    df.drop(columns=[df.columns[7] + '_merged'], inplace=True)

    return df

file_path = 'leaf_leaf_apps.csv'
merged_df = merge_parent_ids(file_path)
merged_df.to_csv('merged_file.csv', index=False)
