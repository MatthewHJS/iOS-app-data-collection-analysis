import csv
import ast

'''
Initializes the leaf_leaf_apps.csv

'''

app_ids = []
rec_ids = []
with open('leaf_apps.csv', 'r', newline='', encoding='Windows-1252') as file:
    reader = csv.reader(file)
    next(reader) 
    for row in reader:
        app_ids.append(row[0])  
        rec_ids.append(ast.literal_eval(row[6]))



with open('leaf_leaf_apps.csv', 'w', newline='', encoding='Windows-1252') as file:
    writer = csv.writer(file)
    writer.writerow(['App ID', 'App Name', 'APK Size', 'Supported Languages', 'Category', 'Recommended User Age', 'Recommended Apps', 'Parent ID'])

    for i in range(0, len(app_ids)):
        for id in rec_ids[i]:
            writer.writerow([id, '', '', '', '', '', '', app_ids[i]])





