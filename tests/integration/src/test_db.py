import pytest
from bson.objectid import ObjectId

from src.annotator_queue import AnnotatorQueue
from tests.test_helpers import (load_test_file,
                                get_db_instance,
                                delete_db)


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


@pytest.mark.asyncio
async def test_annotator_queue_insert_entry():
    db = await get_db_instance()
    document_annotation = load_test_file('test_annotator_queue.json')[0]
    annotator_queue = AnnotatorQueue(db)
    await annotator_queue.add_document_annotations([document_annotation])

    queue_entries = annotator_queue.get_filtered_queue()
    actual_no_entries = len(queue_entries)
    expected_no_entries = 1

    assert actual_no_entries == expected_no_entries

    # Simulation of app crash
    del annotator_queue

    annotator_queue = AnnotatorQueue(db)
    await annotator_queue.load_queue_from_db()

    queue_entries = annotator_queue.get_filtered_queue()
    actual_no_entries = len(queue_entries)
    assert actual_no_entries == expected_no_entries
