from typing import (Optional, 
                    List, 
                    Dict)

from pydantic import (BaseModel, 
                      Field)


class AnnotationModel(BaseModel):
    key: str = Field(..., description='Key which uniquely assigns the element to the corresponding entry '
                                      'in the x28 ontology.')
    type: str = Field(..., description='Annotation type.',
                             enum=['education', 'occupation', 'degree', 'industry', 'topic', 'position',
                                   'sco', 'softskill', 'languageSkill', 'school', 'skill', 'scope', 'predicate'])
    surface_form: str = Field(..., description='Annotated element as it is written '
                                               'in the text representation of the html.')
    start: int = Field(..., description='Start position of the annotated element '
                                        'in the text representation of the html.')
    end: int = Field(..., description='Start position of the annotated element in the text representation of the html.')
    scope: str = Field(..., description='Scope of the annotations')
    meta: Dict

    class Config:
        schema_extra = {
            "example":
                {
                    "key": "#somekey",
                    "type": "topic",
                    "surface_form": "Hello world",
                    "start": 21,
                    "end": 32,
                    "scope": "some_scope",
                    "meta": {"some": "other",
                             "key": "values"}
                }
        }


class AnnotationBlobModel(BaseModel):
    d_id: str = Field(..., description='Unique key for identifying document')
    annotator: str = Field(..., description='Service or Person used for annotations')
    annotations: List[AnnotationModel]

    class Config:
        schema_extra = {
            "example":
                {"d_id": "some_document_id",
                 "annotator": "some_annotator",
                 "annotations": [{
                     "key": "#somekey",
                     "type": "topic",
                     "surface_form": "Hello world",
                     "start": 21,
                     "end": 32,
                     "scope": "some_scope",
                     "meta": {"some": "other",
                              "key": "values"}
                 }]}
        }


class DataExchangeModel(BaseModel):
    da_id: str = Field(..., description='Unique key for identifying document annotations')
    meta: Dict
    data: AnnotationBlobModel

    class Config:
        schema_extra = {
                "example":
                {
                    "da_id": "some_da_id",
                    "meta": {"some": "more",
                             "key": "values"},
                    "data": {"d_id": "some_document_id",
                             "annotator": "some_annotator",
                             "annotations": [{
                                 "key": "#somekey",
                                 "type": "topic",
                                 "surface_form": "Hello world",
                                 "start": 21,
                                 "end": 32,
                                 "scope": "some_scope",
                                 "meta": {"some": "other",
                                          "key": "values"}
                                 }]}
                    }
                }


class DocumentPostModel(BaseModel):
    id: int = Field(..., description='Original ID of the Document')
    text: str = Field(..., description='Text of the document')
    gold_standard_annotation: Optional[Dict[str, List[AnnotationModel]]]
    annotations: Optional[Dict[str, List[AnnotationModel]]]

    class Config:
        schema_extra = {
                "example":
                {
                    "id": "197643",
                    "text": "Im a named entity",
                    "gold_standard_annotation": {"work_activity": [
                        {
                            "key": "#somekey",
                            "entity_type": "topic",
                            "surface_form": "named entity",
                            "start": 5,
                            "end": 17
                            }
                        ]},
                    "annotations": {"work_activity": [
                        {
                            "key": "#somekey",
                            "entity_type": "topic",
                            "surface_form": "named entity",
                            "start": 5,
                            "end": 17
                        }
                    ]}
                    }
                }


class CorpusModel(BaseModel):
    corpus_name: str = Field(..., description='Name of the corpus.')
    description: Optional[str] = Field(..., description='Description of the corpus.')

    class Config:
        schema_extra = {
            "example":
                {
                    "corpus_name": "Some corpus",
                    "description": "Just a random corpus"
                }
        }


class ResponseModel(BaseModel):
    status_code: int = Field(..., description='Status of response', enum=[200, 201, 400, 401])
    message: str = Field(..., description='Error Message if request could not be processed')
    content: Dict[str, Dict]

    class Config:
        schema_extra = {
                "example":
                {
                    "status_code": 200,
                    "message": "",
                    "content": {"da_id": "some_da_id"}
                    }
                }
