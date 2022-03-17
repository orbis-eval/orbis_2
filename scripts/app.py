from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]
sys.path.append(str(PROJECT_ROOT.absolute()))

from src.db import DB
from src.annotator_queue import AnnotatorQueue
from scripts.models import (DataExchangeModel,
                            DocumentPostModel,
                            ResponseModel,
                            CorpusModel)
from src.models.response import Response


app = FastAPI(title='Orbis 2 Webservice',
              version='1.0')
db = DB()
annotator_queue = AnnotatorQueue()


@app.put('/addDocumentToAnnotationQueue/{da_id}', response_model=ResponseModel)
def add_document_to_annotation_queue(da_id: int):
    if document_annotation_for_queue := db.get_document_annotation_for_queue(da_id):
        annotator_queue.add_document_annotation(document_annotation_for_queue)
        response = Response(status_code=200,
                            message=f'{da_id} added to queue.')
    else:
        response = Response(status_code=400,
                            message=f'{da_id} not added to queue.')
    return response.as_json()


@app.get('/getDocumentForAnnotation', response_model=ResponseModel)
def get_document_for_annotation(corpus_name=None, annotator=None):
    if da_id := annotator_queue.get_id_for_annotation(corpus_name, annotator):
        response_content = get_document_content(da_id)
        response_annotations = get_document_annotations(da_id)
        if response_content and response_annotations:
            response = Response(status_code=200, 
                                content={'da_id': da_id,
                                         'content': response_content['content'],
                                         'annotations': response_annotations['content']})
        else:
            response = Response(status_code=400, 
                                message='Empty annotator queue for request.')
    else:
        response = Response(status_code=400, 
                            message='Empty annotator queue for request.')
    return response.as_json()


@app.get('/getDocumentContent', response_model=ResponseModel)
def get_document_content(da_id=None):
    if not da_id:
        response = Response(status_code=400, 
                            message='Missing da_id in request.')
    elif text := db.get_document_content(da_id):
        response = Response(status_code=200, 
                            content={'text': text})
    else:
        response = Response(status_code=400,
                            message=f'{da_id} not found in DB.')
    return response.as_json()


@app.get('/getDocumentAnnotations', response_model=ResponseModel)
def get_document_annotations(da_id=None):
    if not da_id:
        response = Response(status_code=400, 
                            message='Missing da_id in request.')
    elif annotations := db.get_document_annotations(da_id):
        response = Response(status_code=200, 
                            content={'annotations': annotations})
    else:
        response = Response(status_code=400,
                            message=f'{da_id} not found in DB.')
    return response.as_json()


@app.post('/saveDocumentAnnotations', response_model=ResponseModel)
def save_document_annotations(data: DataExchangeModel):
    data = data.dict()
    if da_id := db.save_document_annotations(**data):
        response = Response(status_code=200,
                            content={'da_id': da_id})
    else:
        response = Response(status_code=400, 
                            message=f'Document Annotation not saved in db')
    return response.as_json()


@app.post('/addDocument', response_model=ResponseModel)
def add_document(document: DocumentPostModel):
    document = document.dict()
    d_id, da_id, annotation_id = db.add_document(**document)
    if d_id and da_id and annotation_id:
        response = Response(status_code=200,
                            content={'d_id': d_id,
                                     'da_id': da_id,
                                     'annotation_id': annotation_id},
                            message=f'Document {document.get("source_id", "")} added '
                                    f'to corpus {document.get("corpus_name")}created.')
    else:
        response = Response(status_code=400,
                            message='Document not added.')
    return response.as_json()


@app.post('/createCorpus', response_model=ResponseModel)
def create_corpus(corpus: CorpusModel):
    corpus = corpus.dict()
    if corpus_id := db.create_corpus(**corpus):
        response = Response(status_code=200,
                            content={'corpus_id': corpus_id},
                            message=f'Corpus {corpus.get("name", "")} created.')
    else:
        response = Response(status_code=400,
                            message='Corpus not created.')
    return response.as_json()


def get_app():
    return app


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
