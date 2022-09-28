import sys
from pathlib import Path
import json
import argparse

PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(PROJECT_DIR / 'src'))

from scripts.app import get_app

parser = argparse.ArgumentParser()
parser.add_argument('-fn', '--filename', help='How the output file should be named')
args = parser.parse_args()

filename = 'openapi.json'


# To execute, uncomment the app.mount line in scripts/app.py
if __name__ == '__main__':
    app = get_app()
    if args.filename:
        filename = args.filename

    with open(Path(__file__).parent / filename, 'w+') as file:
        json.dump(app.openapi(), file)
