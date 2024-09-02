import pandas as pd
import ast
import csv

'''
collectionfinder.py 


Constructs collections for the third task of the project. 

I have decided to construct two types of collections 
1. Direct relationships 
2. n = 5, similar recommendations 


'''


# Read the CSV file
df1 = pd.read_csv('leaf_apps.csv')
df2 = pd.read_csv('leaf_leaf_apps.csv')

# Extract columns
app_id = df1.iloc[:, 0]
rec_id1 = df1.iloc[:, 6]
parents_id = df1.iloc[:, 7]
rec_id2 = df2.iloc[:, 6]

collections = []

# Combine app_id, rec_id, and parents_id into collections
for i in range(len(app_id)):
    curr_collection = [app_id[i]]
    curr_collection.extend(ast.literal_eval(rec_id1[i]))
    curr_collection.extend(ast.literal_eval(parents_id[i]))
    collections.append(curr_collection)

# Combine all rec_id1 and rec_id2 into rec_all
rec_all = []
for i in range(len(rec_id1)):
    rec_all.append(ast.literal_eval(rec_id1[i]))
for i in range(len(rec_id2)):
    rec_all.append(ast.literal_eval(rec_id2[i]))

#Using set to find duplicates
def count_similarities(list1, list2):
    return (len(set(list1) & set(list2)))

def merge_lists(list1, list2):
    return list(set(list1) | set(list2))

def merge_similar_lists(lists, n):
    merged = []
    while lists:
        base_list = lists.pop(0)
        to_merge = []
        for lst in lists:
            if count_similarities(base_list, lst) >= n:
                to_merge.append(lst)
        
        for lst in to_merge:
            lists.remove(lst)
            base_list = merge_lists(base_list, lst)
        
        merged.append(base_list)
    return merged

n = 5
collSim = merge_similar_lists(rec_all, n)

#avg length for each list in both collections. 
collSimcount = 0
collectioncount = 0

for i in collSim:
    collSimcount += len(i)

for i in collections:
    collectioncount += len(i)





