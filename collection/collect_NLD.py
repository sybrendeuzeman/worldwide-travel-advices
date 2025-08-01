import json
from datetime import date, datetime
from pathlib import Path
import StringIO
import pandas as pd

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

        with open(
            path_dir_raw_data
            / date.today().isoformat()
            / f"list_advices_{offset}.json",
            "wb",
        ) as f:
            f.write(r.content)

        offset += rows
        data_total.extend(data)

    # Get advices not yet downloaded
    for short_advice in data_total:
        timestamp = datetime.strptime(
            short_advice["lastmodified"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%Y-%m-%dT%H_%M_%S_%f")

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


def raw2collect_NLD(dir_data):
    path_dir_raw_data = Path(dir_data) / "raw" / "NLD" / "traveladvice"
    path_dir_collect_data = Path(dir_data) / "collect" / "NLD" / "traveladvice"

    l_raw_files = sorted([p.name for p in path_dir_raw_data.glob("*")], reverse=True)

    l_collect_files = sorted(
        [p.name for p in path_dir_collect_data.glob("*")], reverse=True
    )

    if len(l_collect_files) > 0:
        check_file = l_collect_files[0]
    else:
        check_file = "advice"

    for raw_file in l_raw_files:
        if check_file >= raw_file:
            break

    return path_dir_raw_data.glob("*")


def transform_NLD(path_file_in, path_file_out, country_codes):
    
    
    with open(path_file_in, "r") as f:
        data = json.loads(f.read())

    dict_label = {
        "advise_from" : "NLD",
        "advise_on" : 
        "advise_country_name" : data['id'],
    }

    



    return data
