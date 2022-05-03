from pathlib import Path
import json

from src.db import DB


TEST_DATA_PATH = Path(__file__).parents[0] / 'testdata'


def load_test_file(fn='test_document.json'):
    with open(TEST_DATA_PATH / fn, 'r+') as file:
        data = json.loads(file.read())
    return data


async def get_db_instance():
    # Pipeline URL
    db = DB("mongodb://mongo:27017/?retryWrites=true&w=majority")
    # Local URL
    # db = DB()
    await db.open()
    return db


async def delete_db(db):
    await db._delete()
    db.close()
