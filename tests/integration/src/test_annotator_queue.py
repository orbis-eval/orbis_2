import json
from pathlib import Path
from src.annotator_queue import AnnotatorQueue

TEST_DATA_PATH = Path(__file__).parents[2] / 'testdata'


def load_test_file(fn='test_document.json'):
    with open(TEST_DATA_PATH / fn, 'r+') as file:
        data = json.loads(file.read())
    return data


def test_first_in_first_out():
    document_annotations = load_test_file('test_annotator_queue.json')
    annotator_queue = AnnotatorQueue(document_annotations)

    da_id_expected = document_annotations[0]['da_id']
    da_id_actual = annotator_queue.get_id_for_annotation()

    assert da_id_expected == da_id_actual


def test_get_id_for_annotation_corpus_filter():
    document_annotations = load_test_file('test_annotator_queue.json')
    annotator_queue = AnnotatorQueue(document_annotations)

    da_id_expected = 'da_id_2'
    da_id_actual = annotator_queue.get_id_for_annotation(corpus_name='fhgr')

    assert da_id_expected == da_id_actual


def test_get_id_for_annotation_annotator_filter():
    document_annotations = load_test_file('test_annotator_queue.json')
    annotator_queue = AnnotatorQueue(document_annotations)

    da_id_expected = 'da_id_1'
    da_id_actual = annotator_queue.get_id_for_annotation(annotator='gold')

    assert da_id_expected == da_id_actual


def test_get_id_for_annotation_corpus_and_annotator_filter():
    document_annotations = load_test_file('test_annotator_queue.json')
    annotator_queue = AnnotatorQueue(document_annotations)

    da_id_expected = 'da_id_4'
    da_id_actual = annotator_queue.get_id_for_annotation(corpus_name='fhgr',
                                                         annotator='ner')

    assert da_id_expected == da_id_actual


def test_update_document_status():
    document_annotation = load_test_file('test_annotator_queue.json')[0]
    annotator_queue = AnnotatorQueue([document_annotation])

    da_id = document_annotation.get('da_id')
    success = annotator_queue.update_document_annotation_status(da_id, 'done')

    expected_status = 'done'
    actual_status = annotator_queue.get_document_annotation_status(da_id)

    assert expected_status == actual_status
    assert success == True


def test_remove_document_status():
    document_annotation = load_test_file('test_annotator_queue.json')[0]
    annotator_queue = AnnotatorQueue([document_annotation])

    da_id = document_annotation.get('da_id')
    success = annotator_queue.remove_document_annotation(da_id)

    expected_da = {}
    actual_da = annotator_queue.get_id_for_annotation()

    assert expected_da == actual_da
    assert success == True
