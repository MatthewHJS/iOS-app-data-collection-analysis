import pandas as pd
import ast

df = pd.read_csv('root_apps.csv', header=None)

most_parents = [1608789604, 6479435323, 6446139013, 1643294506, 1643294506, 1643294506, 1600367795, 1608789604, 1605388852, 
                1543581137, 1611978184, 1370599950, 1172501360, 1611978184, 1597279982, 1605388852, 1546598842, 1608789604, 
                1611978184, 1643294506, 1643294506, 1172501360, 1608789604, 1611978184, 1611978184, 1643294506, 1643294506, 
                1608789604, 1611978184, 1605388852, 1643294506, 1643294506, 1608789604, 1608789604, 1605388852, 1643294506, 
                1643294506, 1608789604, 1611978184, 1611978184, 1643294506, 1605388852, 1370599950, 1611978184, 1643294506, 
                1605388852, 1605388852, 1608789604, 1611978184, 1643294506, 1605388852, 1172501360, 1608789604, 1611978184, 
                1605388852, 1643294506, 1643294506, 1608789604, 1611978184, 1643294506, 1605388852, 1605388852, 1608789604, 
                1611978184, 1643294506, 1605388852, 1605388852, 1608789604, 1611978184, 1605388852, 1643294506, 1172501360, 
                1370599950, 1611978184, 1611978184, 1605388852, 1643294506, 1608789604, 1600367795, 1611978184, 1172501360, 
                1629904853, 1608789604, 1611978184, 1643294506, 1643294506, 1605757785, 1608789604, 1611978184, 1643294506, 
                1605388852, 1629371699, 1608789604, 1611978184, 1605388852, 1643294506, 1644160969, 1608789604, 1611978184, 
                1643294506, 1605388852, 1575419096, 1608789604, 1611978184, 1605388852, 1643294506, 1606868055, 1608789604, 
                1643294506, 1611978184, 1605388852, 1636100189, 1608789604, 1611978184, 1643294506, 1568434949, 1172501360, 
                1550483828, 1611978184, 1611978184, 1643294506, 1172501360, 1608789604, 1611978184, 1643294506, 1643294506, 
                1172501360, 1370599950, 1611978184, 1643294506, 1605388852, 1370599950, 1608789604, 1608789604, 1643294506, 
                1605388852, 1608789604, 1608789604, 1611978184, 1643294506, 1605388852]

root_ids = []
#Getting all root apps from the most_parent analysis
for index, row in df.iloc[1:].iterrows():
    parent_ids = ast.literal_eval(row[6])  
    if any(parent_id in most_parents for parent_id in parent_ids):
        root_ids.append(row[0])


print(len(root_ids))

recommendations_list = []

for index, row in df.iloc[1:].iterrows():
    if row[0] in root_ids:
        recommended_ids = ast.literal_eval(row[6]) 
        if isinstance(recommended_ids, int):
            recommended_ids = {recommended_ids}
        else:
            recommended_ids = set(recommended_ids)
        recommendations_list.append(recommended_ids)
    

# Find apps that are present in every recommendation
if recommendations_list:
    common_apps = set.intersection(*recommendations_list)
else:
    common_apps = set()

# Print the number of common recommended apps
print(len(common_apps))