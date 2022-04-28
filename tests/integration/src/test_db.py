import json
import pytest
from pathlib import Path
from src.db import DB
from bson.objectid import ObjectId

TEST_DATA_PATH = Path(__file__).parents[2] / 'testdata'


def load_test_file(fn='test_document.json'):
    with open(TEST_DATA_PATH / fn, 'r+') as file:
        data = json.loads(file.read())
    return data


async def get_db_instance():
    db = DB()
    await db.open()
    return db


async def delete_db(db):
    await db._delete()
    db.close()


@pytest.mark.asyncio
async def test_get_document_content():
    document = load_test_file('test_document.json')
    document_content_expected = document['text']
    db = await get_db_instance()

    d_insert_id, da_insert_id, annotation_insert_id, document_exists = await db.add_document(**document)
    document_content_actual = await db.get_document_content(da_insert_id)

    await delete_db(db)

    assert document_content_expected == document_content_actual


@pytest.mark.asyncio
async def test_get_document_annotations():
    document = load_test_file('test_document.json')
    document_annotations_expected = document['data']
    db = await get_db_instance()

    d_insert_id, da_insert_id, annotation_insert_id, document_exists = await db.add_document(**document)
    document_annotations_actual = await db.get_document_annotations(da_insert_id)

    await delete_db(db)

    assert document_annotations_expected == document_annotations_actual


@pytest.mark.asyncio
async def test_save_document_annotations():
    document = load_test_file('test_document.json')
    document_annotations = load_test_file('test_document_annotations.json')
    db = await get_db_instance()

    d_insert_id, da_insert_id, annotation_insert_id, document_exists = await db.add_document(**document)
    document_annotations['da_id'] = da_insert_id
    document_annotations['data']['d_id'] = d_insert_id

    new_da_id = await db.save_document_annotations(**document_annotations)
    record_filter = {'_id': ObjectId(new_da_id)}
    result = await db._get_record('document_annotation', record_filter)
    precessor = result.get('precessor')

    await delete_db(db)

    assert da_insert_id == precessor
