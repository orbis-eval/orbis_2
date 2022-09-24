import json
import glob
from pathlib import Path
import requests
import os


def import_into_db(gold_dir, service_url, max_files=5, prod=False):
    session = requests.session()
    if prod:
        session.auth = (os.environ['ORBIS_PROD_USER'], os.environ['ORBIS_PROD_PW'])
    files = glob.glob(f'{gold_dir}/*.json')
    for f in files[:max_files]:
        with open(f, 'r+') as file:
            data = json.loads(file.read())
            r = session.post(f'{service_url}addDocument', json=data)
            r = json.loads(r.content.decode())
            if r['status_code'] == 200:
                print(f'Document {f} added.')
                da_id = r['content']['da_id']
                r2 = session.put(f'{service_url}addDocumentToAnnotationQueue/{da_id}')
                if json.loads(r2.content.decode())['status_code'] == 200:
                    print(f'Document {f} added to annotator queue.')
                else:
                    print(f'Document {f} not added to annotator queue.')
            else:
                print(f'Document {f} not added.')


if __name__ == '__main__':
    # LIVE_SERVICE_URL = 'https://orbis2.prod.semanticlab.net/'
    # LOCAL_SERVICE_URL = 'http://0.0.0.0:63010/'
    GOLD_DIR = Path(__file__).parent / 'goldDocuments' / 'orbis'
    import_into_db(GOLD_DIR, os.environ['SERVICE_URL'], 1000, True)
    # import_into_db(GOLD_DIR, LOCAL_SERVICE_URL, 1000, True)
