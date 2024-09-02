import requests
from bs4 import BeautifulSoup
import csv
import concurrent.futures
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_app_basic_info(app_id, retries=3):
    original_app_id = app_id
    app_url = f'https://apps.apple.com/us/app/{app_id}'
    try:
        response = requests.get(app_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    
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

        recommended_url = f'https://apps.apple.com/us/app/{app_id}?see-all=customers-also-bought-apps'
        response = requests.get(recommended_url, timeout=10)
        
        a_tags = soup.find_all('a')
        recommended_ID = []
        for a in a_tags:
            if a.get('data-metrics-click') is not None:
                data_metrics_click = a.get('data-metrics-click')
                start_index = data_metrics_click.find("targetId\":\"") + len("targetId\":\"")
                end_index = data_metrics_click.find("\"", start_index)
                app_id = data_metrics_click[start_index:end_index]
                try:
                    recommended_ID.append(int(app_id))
                except Exception as e:
                    logging.error(f"Error parsing recommended ID for app {app_id}: {e}")

    except requests.RequestException as e:
        if retries > 0:
            logging.warning(f"Retrying for app {app_id} due to error: {e}")
            time.sleep(1)  # Brief pause before retrying
            return get_app_basic_info(app_id, retries - 1)
        else:
            logging.error(f"Failed to fetch data for app {app_id} after retries: {e}")
            return [app_id, None, None, None, None, None, None]
    except Exception as e:
        logging.error(f"Unexpected error for app {app_id}: {e}")
        return [app_id, None, None, None, None, None, None]

    return [original_app_id, app_name, app_size, app_languages, app_category, app_age, recommended_ID]

def fetch_app_details(app_ids):
    all_apps_details = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_app_id = {executor.submit(get_app_basic_info, app_id): app_id for app_id in app_ids}
        for future in concurrent.futures.as_completed(future_to_app_id):
            app_id = future_to_app_id[future]
            try:
                app_details = future.result()
                all_apps_details.append(app_details)
                logging.info(f"Fetched details for app {app_id}")
            except Exception as exc:
                logging.error(f"App {app_id} generated an exception: {exc}")
    return all_apps_details

app_ids = [] 

with open('leaf_apps.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        app_ids.append(row[0])

all_apps_details = fetch_app_details(app_ids)

with open('leaf_apps.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["App ID", "App Name", "App Size", "App Languages", "App Category", "App Age Rating", "Recommended IDs","Parent ID"])
    for app_details in all_apps_details:
        writer.writerow(app_details)
