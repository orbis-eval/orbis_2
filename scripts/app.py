import time

from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path

from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

PROJECT_ROOT = Path(__file__).parents[1]
sys.path.append(str(PROJECT_ROOT.absolute()))

from src.db import DB
from src.annotator_queue import AnnotatorQueue
from scripts.models import (DataExchangeModel,
                            DocumentPostModel,
                            ResponseModel,
                            CorpusModel)
from src.models.response import Response


db = DB()

app = FastAPI(title='Orbis 2 Webservice',
              version='1.0')
app.add_event_handler('startup', db.open_)
app.add_event_handler('shutdown', db.close)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

annotator_queue = AnnotatorQueue(db)

app.add_event_handler('startup', annotator_queue.load_queue_from_db)


@app.get('/', response_class=FileResponse)
def home():
    return FileResponse('index.html')


@app.get('/annotation', response_class=RedirectResponse)
def annotation():
    return RedirectResponse("/")


@app.put('/addDocumentToAnnotationQueue/{da_id}', response_model=ResponseModel)
async def add_document_to_annotation_queue(da_id: str):
    response = None
    if document_annotation_for_queue := await db.get_document_annotation_for_queue(da_id):
        if success := await annotator_queue.add_document_annotation(document_annotation_for_queue):
            response = Response(status_code=200,
                                message=f'{da_id} added to queue.')
    if not response:
        response = Response(status_code=400,
                            message=f'{da_id} not added to queue.')
    return response.as_json()


@app.get('/getDocumentForAnnotation', response_model=ResponseModel)
async def get_document_for_annotation(corpus_name=None, annotator=None):
    print(f'get_document_for_annotation with corpus "{corpus_name}" and annotator "{annotator}"')

    if da_id := await annotator_queue.get_id_for_annotation(corpus_name, annotator):
        print('check for document content')
        response_content = await get_document_content(da_id)
        print('check for document annotation')
        response_annotations = await get_document_annotations(da_id)

        if response_content and response_annotations:
            response = Response(status_code=200,
                                content={'da_id': da_id,
                                         'text': response_content['content']['text'],
                                         'annotations': response_annotations['content']['annotations']})
        else:
            response = Response(status_code=400,
                                message='Empty annotator queue for request.',
                                content={'corpus_name': corpus_name, 'annotator': annotator})
    else:
        response = Response(status_code=400,
                            message='Empty annotator queue for request.',
                            content={'corpus_name': corpus_name, 'annotator': annotator})
    return response.as_json()


@app.get('/getDocumentContent', response_model=ResponseModel)
async def get_document_content(da_id=None):
    if not da_id:
        response = Response(status_code=400,
                            message='Missing da_id in request.')
    elif text := await db.get_document_content(da_id):
        response = Response(status_code=200,
                            content={'text': text})
    else:
        response = Response(status_code=400,
                            message=f'{da_id} not found in DB.')
    return response.as_json()


@app.get('/getDocumentAnnotations', response_model=ResponseModel)
async def get_document_annotations(da_id=None):
    if not da_id:
        response = Response(status_code=400,
                            message='Missing da_id in request.')
    elif annotations := await db.get_document_annotations(da_id):
        annotations['meta']['request_time'] = time.time()
        response = Response(status_code=200,
                            content={'annotations': annotations})
    else:
        response = Response(status_code=400,
                            message=f'{da_id} not found in DB.')
    return response.as_json()


@app.get('/getAnnotatorQueue', response_model=ResponseModel)
def get_annotator_queue(corpus_name=None, annotator=None):
    if queue := annotator_queue.get_filtered_queue(corpus_name, annotator):
        response = Response(status_code=200,
                            content={'text': f'Success. Found {len(queue)} result for corpus name {corpus_name} '
                                             f'and annotator {annotator}.',
                                     'queue': queue})
    else:
        response = Response(status_code=400,
                            message='Empty annotator queue for request.',
                            content={'corpus_name': corpus_name, 'annotator': annotator})
    return response.as_json()


@app.post('/saveDocumentAnnotations', response_model=ResponseModel)
async def save_document_annotations(data: DataExchangeModel):
    data = data.dict()
    if da_id := await db.save_document_annotations(**data):
        response = Response(status_code=200,
                            content={'da_id': da_id})
    else:
        response = Response(status_code=400,
                            message=f'Document Annotation not saved in db for da: {da_id}')
    return response.as_json()


@app.post('/addDocument', response_model=ResponseModel)
async def add_document(document: DocumentPostModel):
    document = document.dict()
    d_id, da_id, annotation_id, document_exists = await db.add_document(**document)
    if document_exists:
        response = Response(status_code=400,
                            content={'d_id': d_id},
                            message='Document not added, as it already exists.')
    else:
        response = Response(status_code=200,
                            content={'d_id': d_id,
                                     'da_id': da_id,
                                     'annotation_id': annotation_id},
                            message=f'Document {document.get("source_id", "")} added '
                                    f'to corpus {document.get("corpus_name")}created.')
    return response.as_json()


@app.post('/createCorpus', response_model=ResponseModel)
async def create_corpus(corpus: CorpusModel):
    corpus = corpus.dict()
    if corpus_id := await db.create_corpus(**corpus):
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
