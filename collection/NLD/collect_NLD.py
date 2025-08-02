import json
from datetime import date, datetime
from pathlib import Path
import pandas as pd
import argparse
from dotenv import load_dotenv
import os
from ollama import Client

import requests


def src2raw_NLD(dir_data):
    """
    Download the travel advices from the Netherlands at a certain point in time
    """

    url_api = "https://opendata.nederlandwereldwijd.nl/v2/sources/nederlandwereldwijd/infotypes/"
    headers = {
        "User-Agent": "https://github.com/sybrendeuzeman/worldwide-travel-advices"
    }

    # Get list with travel advices
    rows = 200
    offset = 0

    path_dir_raw_data = Path(dir_data) / "raw" / "NLD"
    path_dir_raw_data.mkdir(parents=True, exist_ok=True)

    data_total = []

    while True:
        url = f"{url_api}traveladvice?output=json&rows={rows}&offset={offset}"

        r = requests.get(url, headers=headers)
        r.raise_for_status()

        data = r.json()
        if len(data) == 0:
            break
        
        path_file_list = path_dir_raw_data / date.today().isoformat() / f"list_advices_{offset}.json"
        path_file_list.parent.mkdir(parents=True, exist_ok=True)

        with open(
            path_file_list,
            "wb",
        ) as f:
            f.write(r.content)

        offset += rows
        data_total.extend(data)

    # Get advices not yet downloaded
    for short_advice in data_total:
        timestamp = datetime.strptime(
            short_advice["lastmodified"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%Y-%m-%d")

        path_file = (
            path_dir_raw_data
            / f"traveladvice/advice_{timestamp}_{short_advice['id']}.json"
        )

        path_file.parent.mkdir(parents=True, exist_ok=True)

        if path_file.exists():
            continue

        url = f"{url_api}countries/{short_advice['id']}/traveladvice?output=json"

        r = requests.get(url, headers=headers)
        r.raise_for_status()

        with open(path_file, "wb") as f:
            f.write(r.content)

def transform_NLD(path_file_in, country_codes, client, query_label):   
    with open(path_file_in, "r", encoding='utf-8') as f:
        data = json.loads(f.read())

    dict_label = {
        "advise_from" : "NLD",
        "advise_on" : country_codes[data['location']],
        "advise_on_name" : data['location'],
        "text_label" : data['introduction']
    }
    
    # Use genAI to find the label from the text
    no_answer = True
    attempts = 0
    while attempts < 10:
        attempts += 1
        try:
            query = f"{query_label} {data['location']}:\n{data['introduction']}"
            response = client.chat(model='gemma3:4b', messages=[
            {
                'role': 'user',
                'content': query,
            },
            ])

            dict_label['label'] = json.loads(response.message.content)

            if any(value not in ['groen', 'geel', 'oranje', 'rood'] for value in dict_label['label'].values()):
                print("Not in 'groen', 'geel', 'oranje', 'rood'")
                continue

            break
        except json.JSONDecodeError:
            print("JSONDecodeErrors; AI answered with", response.message.content)

        except:
            print("Another error")
    return dict_label

def raw2collect_NLD(dir_data, client):
    
    path_countrycodes = Path(__file__).parent / "countrycodes.json" 
    with open(path_countrycodes, 'r') as f:
        country_codes = json.load(f)

    path_query = Path(__file__).parent / "query_label.txt" 
    with open(path_query, 'r') as f:
        query_label = f.read()

    path_dir_raw_data = Path(dir_data) / "raw" / "NLD" / "traveladvice"
    paths_raw = path_dir_raw_data.glob("*")

    values = []
    for path in paths_raw:
        print(path.name)
        dict_label = transform_NLD(path, country_codes, client, query_label)
        values.append(dict_label)

    dict_values = {
        "values" : values,
        "last_file" : path.name
    }

    path_dir_data_collect = Path(dir_data) / "collect" / "NLD" / f"advice_{date.today().isoformat()}.json"
    path_dir_data_collect.parent.mkdir(parents=True, exist_ok=True)
    with open(path_dir_data_collect, 'w') as f:
        json.dump(dict_values, f)

def main():
    load_dotenv()
    print(__file__)

    # Get label via an AI model
    client = Client(
       host='http://localhost:11434',
       headers = {"timeout" : "10"}
    )
    dir_data = os.getenv('DIR_DATA')
    src2raw_NLD(dir_data)
    raw2collect_NLD(dir_data, client)

if __name__ == "__main__":
    main()