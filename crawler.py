import requests
from bs4 import BeautifulSoup
import csv

def get_app_basic_info(app_id):
    app_url = f'https://apps.apple.com/us/app/{app_id}'
    response = requests.get(app_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        app_name = soup.find('h1', {'class': 'app-header__title'}).text.strip()
        info_items = soup.find_all('div', {'class': 'information-list__item'})
    
        app_category = app_languages = app_size = app_age = ''
        
        for item in info_items:
            term = item.find('dt', {'class': 'information-list__item__term'}).text.strip()
            if term == "Category":
                app_category = item.find('a').text.strip()
            elif term == "Languages":
                app_languages = item.find('p').text.strip()
            elif term == "Size":
                app_size = item.find('dd').text.strip()
            elif term == "Age Rating":
                app_age = item.find('dd').text.strip().split('\n')[0]

        reccomended_url = f'https://apps.apple.com/us/app/{app_id}?see-all=customers-also-bought-apps'
        response = requests.get(reccomended_url)


        a_tags = soup.find_all('a')
        reccomended_ID = []
        # Gets all links on the page and filters them to see which has the data-metrics-click value
        for a in a_tags:
            
            if a.get('data-metrics-click') != None:
                # Getting only the targetId value
                data_metrics_click = a.get('data-metrics-click')
                start_index = data_metrics_click.find("targetId\":\"") + len("targetId\":\"")
                end_index = data_metrics_click.find("\"", start_index)
                app_id = data_metrics_click[start_index:end_index]
                try:
                    reccomended_ID.append(int(app_id))
                except Exception as e:
                    print(f"Error: {e}")

    except Exception as e:
        print(f'Error: {e}')
        return [None, None, None, None, None, None]
 
   
    return [app_name, app_size, app_languages, app_category, app_age, reccomended_ID]


app_ids = [] 


with open('collectedapps.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    
    next(csv_reader)
    
    for row in csv_reader:
        app_ids.append(row[1])

all_apps_details = []
for app_id in app_ids:
    app_details = get_app_basic_info(app_id)
    all_apps_details.append(app_details)

with open('root_apps.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    rows = list(reader)

with open('root_apps.csv', mode='w', newline='', encoding='utf-8') as file:
   writer = csv.writer(file)
   writer.writerow(["App ID", "App Name", "App Size", "App Languages", "App Category", "App Age Rating", "Recommended IDs"])
   for app_details in all_apps_details:
        writer.writerow(app_details)
