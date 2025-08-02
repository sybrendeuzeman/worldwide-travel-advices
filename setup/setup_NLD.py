from pathlib import Path
import json
import pandas as pd


# Get ISO 3166-1 list for the Netherlands
def setup_countrycode_list(dir_data):
    path_dir_setup_data = Path(dir_data) / "setup" / "NLD"
    path_dir_setup_data.mkdir(parents=True, exist_ok=True)

    df = (
        pd.read_html("https://nl.wikipedia.org/wiki/ISO_3166-1")[0]
    )

    dict_pair = dict(zip(df.Land, df['3-letterig']))
    with open(path_dir_setup_data / "countrycodes.json", "w") as f:
        json.dump(dict_pair, f)