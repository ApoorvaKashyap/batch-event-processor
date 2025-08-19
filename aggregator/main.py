import pandas as pd
import json
from configparser import ConfigParser

configs = ConfigParser()
configs.read(".configs/config.ini")

def aggregate(file:str) -> list[dict]:
    with open(file, 'r') as f:
        events = [json.loads(line) for line in f]
    df = pd.DataFrame(events)
    aggregated = df.groupby('userId').sum().drop(columns=['productId', 'timestamp', 'eventType'])
    return aggregated.reset_index().to_dict(orient='records')

def main():
    print(aggregate(configs["variables"]["input_file"]))


if __name__ == "__main__":
    main()
