import json
import glob
from pathlib import Path
import requests


def import_into_db(gold_dir, service_url, max_files=5):
    files = glob.glob(f'{gold_dir}/*.json')
    for f in files[:max_files]:
        with open(f, 'r+') as file:
            data = json.loads(file.read())
            r = requests.post(service_url, json=data)
            if json.loads(r.content.decode())['status_code'] == 200:
                print(f'Document {f} added.')
            else:
                print(f'Document {f} not added.')


if __name__ == '__main__':
    LOCAL_SERVICE_URL = 'http://0.0.0.0:63010/addDocument'
    GOLD_DIR = Path(__file__).parent / 'goldDocuments' / 'orbis'
    import_into_db(GOLD_DIR, LOCAL_SERVICE_URL, 1000)
