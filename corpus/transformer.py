import json
import glob
from pathlib import Path
import datetime


def transform_education_extraction_gold(gold_dir, out_dir='out'):
    files = glob.glob(f'{gold_dir}/*.json')
    out_dir = gold_dir / out_dir
    out_dir.mkdir(exist_ok=True)
    for f in files:
        json_fn = f.split('/')[-1]
        with open(f, 'r+') as file:
            data = json.loads(file.read())
        transformed = _map_to_orbis2(data)
        with open(out_dir / json_fn, 'w') as file:
            file.write(json.dumps(transformed))


def _map_to_orbis2(data, annotator='gold'):
    annotations = []
    for k, v in data['gold_standard_annotation'].items():
        annotations.extend(v)
    for a in annotations:
        a['scope'] = 'home'
        a['meta'] = {}
    result = {
        "corpus_name": "education_extraction_corpus",
        "source_id": data['id'],
        "text": data['text'],
        "annotator": annotator,
        "data": {
            "d_id": data['id'],
            "meta": {
                "iteration": 1,
                "creation_date": datetime.datetime.now().strftime('%Y%m%d'),
            },
            "annotator": annotator,
            "annotations": annotations
        }
    }
    return result


if __name__ == '__main__':
    GOLD_DIR = Path(__file__).parent / 'goldDocuments'
    transform_education_extraction_gold(GOLD_DIR, 'orbis')
