import pytest

from tests.test_helpers import (load_test_file,
                                get_db_instance,
                                delete_db)


@pytest.mark.asyncio
async def test_create_corpus_already_exsisting():
    corpus = load_test_file('test_corpus.json')
    db = await get_db_instance()
    corpus_insert_id = await db.create_corpus(**corpus)
    duplicate_corpus_insert_id = await db.create_corpus(**corpus)

    await delete_db(db)

    assert corpus_insert_id == duplicate_corpus_insert_id


@pytest.mark.asyncio
async def test_add_document_already_exsisting():
    document = load_test_file('test_document.json')
    db = await get_db_instance()

    d_insert_id, da_insert_id, annotation_insert_id, document_exists = await db.add_document(**document)
    duplicate_d_insert_id, duplicate_da_insert_id, duplicate_annotation_insert_id, duplicate_document_exists = await db.add_document(**document)

    await delete_db(db)

    assert d_insert_id == duplicate_d_insert_id
    assert da_insert_id == duplicate_da_insert_id
    assert annotation_insert_id == duplicate_annotation_insert_id
    assert duplicate_document_exists == True
