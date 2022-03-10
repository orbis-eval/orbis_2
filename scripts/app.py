from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]
sys.path.append(str(PROJECT_ROOT.absolute()))

from src.db_mock import TEST_DB
from src.db import DB
from scripts.models import (DocumentGetModel,
                            DocumentPostModel,
                            ResponseModel,
                            CorpusModel)
from src.models.response import Response


app = FastAPI(title='Orbis 2 Webservice',
              version='1.0')
db = DB()

annotator_queue = {}


@app.put('/addDocumentToAnnotationQueue/{da_id}', response_model=ResponseModel)
def add_document_to_annotation_queue(da_id: int):
    d_id, annotator, iteration_id = tuple(da_id.split('-'))
    annotator_queue.setdefault(annotator, []).append(da_id)
    response = Response(status_code=200)
    return response.as_json()


@app.get('/getNextDocumentForAnnotator')
def get_next_document_for_annotator(corpus_name=None, annotator=None):
    if not corpus_name or not annotator:
        response = Response(status_code=400,
                            message=f'No corpus name or annotator provided. Please check request parameters.')
    if queue := annotator_queue.get(annotator, []):
        response = Response(status_code=200,
                            content={'da_id': queue.pop(-1)})
    else:
        response = Response(status_code=400,
                            message=f'No document found in annotator_queue for annotator {annotator}') 
    return response.as_json()


@app.get('/getDocumentForAnnotator')
def get_document_for_annotator(corpus_name=None, annotator=None):
    if not corpus_name or not annotator:
        response = Response(status_code=400, 
                            message=f'No corpus name or annotator provided. Please check request parameters.')
    if response_da_id := get_next_document_for_annotator(corpus_name, annotator):
        response_content = get_document_content(da_id)
        response_annotations = get_document_annotations(da_id)
        if response_content and response_annotations:
            response = Response(status_code=200, 
                                content={'da_id': response_da_id['content'],
                                         'content': response_content['content'],
                                         'annotations': response_annotations['content']})
        else:
            response = Response(status_code=400, 
                                message=response_content.message)
    else:
        response = Response(status_code=400, 
                            message=response_da_id.message)
    return response.as_json()


@app.get('/getDocumentContent')
def get_document_content(da_id=None):
    if not da_id:
        response = Response(status_code=400, 
                            message='Missing da_id in request.')
    else:
        response = Response(status_code=200, 
                            content={'text': TEST_DB.get_document_content()})
    return response.as_json()


@app.get('/getDocumentAnnotations')
def get_document_annotations(da_id=None):
    if not da_id:
        response = Response(status_code=400, 
                            message='Missing da_id in request.')
    else:
        response = Response(status_code=200, 
                            content={'annotations': TEST_DB.get_document_annotations()})
    return response.as_json()


@app.post('/saveDocumentAnnotations')
def save_document_annotations(document: DocumentGetModel):
    if TEST_DB.save_document():
        response = Response(status_code=200)
    else:
        response = Response(status_code=400, 
                            message=f'Document {document} not saved in db')
    return response.as_json()


@app.post('/addDocument')
def add_doccument(document: DocumentPostModel):
    document = document.dict()
    print(document['id'])


@app.post('/createCorpus')
def create_corpus(corpus: CorpusModel):
    corpus = corpus.dict()
    corpus_id = db.create_corpus(corpus_name=corpus.get('name', ''),
                                 description=corpus.get('description', ''))
    if corpus_id:
        response = Response(status_code=200,
                            content={'corpus_id': corpus_id},
                            message=f'Corpus {corpus.get("name", "")} created.')
    else:
        response = Response(status_code=400)
    return response.as_json()


def get_app():
    return app


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
