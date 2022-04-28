import json
from pathlib import Path
import pytest

from src.annotator_queue import AnnotatorQueue
from src.db import DB

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
async def test_first_in_first_out():
    db = await get_db_instance()
    document_annotations = load_test_file('test_annotator_queue.json')
    annotator_queue = AnnotatorQueue(db)
    await annotator_queue.add_document_annotations(document_annotations)

    da_id_expected = document_annotations[0]['da_id']
    da_id_actual = await annotator_queue.get_id_for_annotation()

    await delete_db(db)

    assert da_id_expected == da_id_actual


@pytest.mark.asyncio
async def test_get_id_for_annotation_corpus_filter():
    db = await get_db_instance()
    document_annotations = load_test_file('test_annotator_queue.json')
    annotator_queue = AnnotatorQueue(db)
    await annotator_queue.add_document_annotations(document_annotations)

    da_id_expected = 'da_id_2'
    da_id_actual = await annotator_queue.get_id_for_annotation(corpus_name='fhgr')

    await delete_db(db)

    assert da_id_expected == da_id_actual


@pytest.mark.asyncio
async def test_get_id_for_annotation_annotator_filter():
    db = await get_db_instance()
    document_annotations = load_test_file('test_annotator_queue.json')
    annotator_queue = AnnotatorQueue(db)
    await annotator_queue.add_document_annotations(document_annotations)

    da_id_expected = 'da_id_1'
    da_id_actual = await annotator_queue.get_id_for_annotation(annotator='gold')

    await delete_db(db)

    assert da_id_expected == da_id_actual


@pytest.mark.asyncio
async def test_get_id_for_annotation_corpus_and_annotator_filter():
    db = await get_db_instance()
    document_annotations = load_test_file('test_annotator_queue.json')
    annotator_queue = AnnotatorQueue(db)
    await annotator_queue.add_document_annotations(document_annotations)

    da_id_expected = 'da_id_4'
    da_id_actual = await annotator_queue.get_id_for_annotation(corpus_name='fhgr',
                                                               annotator='ner')

    await delete_db(db)

    assert da_id_expected == da_id_actual


@pytest.mark.asyncio
async def test_update_document_status():
    db = await get_db_instance()
    document_annotation = load_test_file('test_annotator_queue.json')[0]
    annotator_queue = AnnotatorQueue(db)
    await annotator_queue.add_document_annotations([document_annotation])

    da_id = document_annotation.get('da_id')
    success = annotator_queue.update_document_annotation_status(da_id, 'done')

    expected_status = 'done'
    actual_status = annotator_queue.get_document_annotation_status(da_id)

    await delete_db(db)

    assert expected_status == actual_status
    assert success == True


@pytest.mark.asyncio
async def test_remove_document_status():
    db = await get_db_instance()
    document_annotation = load_test_file('test_annotator_queue.json')[0]
    annotator_queue = AnnotatorQueue(db)
    await annotator_queue.add_document_annotations([document_annotation])

    first_da_id_expected = document_annotation.get('da_id')
    first_da_id = await annotator_queue.get_id_for_annotation()

    expected_da = {}
    actual_da = await annotator_queue.get_id_for_annotation()

    await delete_db(db)

    assert expected_da == actual_da
    assert first_da_id == first_da_id_expected
