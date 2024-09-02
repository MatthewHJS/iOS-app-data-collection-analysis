import csv

'''
Initializes root_apps.csv 
'''

app_ids = []
with open('collectedapps.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader) 
    for row in reader:
        app_ids.append(row[1])  

with open('root_apps.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['App ID', 'App Name', 'APK Size', 'Supported Languages', 'Category', 'Recommended User Age', 'Recommended Apps'])

    for app_id in app_ids:
        writer.writerow([app_id, '', '', '', '', '', '', ''])
