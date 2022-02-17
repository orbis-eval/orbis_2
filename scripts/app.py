from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]
sys.path.append(str(PROJECT_ROOT.absolute()))

from src.db_mock import TEST_DB
from scripts.models import (Document,
                            Response)


app = FastAPI(title='Orbis 2 Webservice',
              version='1.0')

annotator_queue = {}

@app.put('/addDocument/{da_id}', response_model=Response)
def add_document_to_annotation_queue(da_id):
    d_id, annotator, iteration_id = tuple(da_id.split('-'))
    annotator_queue.setdefault(annotator, []).append(da_id)
    response = {'status': 'Success',
                'message': '',
                'content': {}}
    return JSONResponse(content=response)


@app.get('/{corpus_name}/{annotator}/getDocument', response_model=Response)
def get_document_for_annotator(corpus_name, annotator):
    if queue := annotator_queue.get(annotator, []):
        response = {'status': 'Success',
                    'message': '',
                    'content': {'da_id': queue.pop(-1)}
                    }
    else:
        response = {'status': 'Failed',
                    'message': f'No document found in annotator_queue for annotator {annotator}',
                    'content': {}
                    }
    return JSONResponse(content=response)


@app.get('/getDocumentContent/{da_id}', response_model=Response)
def get_document_content(da_id):
    response = {'status': 'Success',
                'message': '',
                'content': {'text': TEST_DB.get_document_content()}
                }
    return JSONResponse(content=response)


@app.get('/getDocumentAnnotations/{da_id}', response_model=Response)
def get_document_annotations(da_id):
    response = {'status': 'Success',
                'message': '',
                'content': {'annotations': TEST_DB.get_document_annotations()}
                }
    return JSONResponse(content=response)


@app.post('/saveDocumentAnnotations', response_model=Response)
def save_document_annotations(document: Document):
    if TEST_DB.save_document():
        response = {'status': 'Success',
                    'message': '',
                    'content': {}
                    }
    else:
        response = {'status': 'Failed',
                    'message': f'Document {document} not saved in db',
                    'content': {}
                    }
    return JSONResponse(content=response)


def get_app():
    return app


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
