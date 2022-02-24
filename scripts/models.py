from typing import (Optional, 
                    List, 
                    Dict)

from pydantic import (BaseModel, 
                      Field)

class AnnotationModel(BaseModel):
    key: str = Field(..., description='Key which uniquely assigns the element to the corresponding entry '
                                      'in the x28 ontology.')
    entity_type: str = Field(..., description='Annotation type.',
                             enum=['education', 'occupation', 'degree', 'industry', 'topic', 'position',
                                   'sco', 'softskill', 'languageSkill', 'school', 'skill', 'scope', 'predicate'])
    surface_form: str = Field(..., description='Annotated element as it is written '
                                               'in the text representation of the html.')
    start: int = Field(..., description='Start position of the annotated element '
                                        'in the text representation of the html.')
    end: int = Field(..., description='Start position of the annotated element in the text representation of the html.')



class DocumentModel(BaseModel):
    da_id: str = Field(..., description='Unique key for identifying document and annotartor within an iteration')
    annotator: str = Field(..., description='Service odr Person used for annotations')
    data: Optional[List[AnnotationModel]] 


    class Config:
        schema_extra = {
                "example":
                {
                    "da_id": "document_1-ner-1",
                    "annotator": "ner",
                    "data": {"annotations": [
                        {
                            "key": "#somekey",
                            "entity_type": "topic",
                            "surface_form": "Hello world",
                            "start": 21,
                            "end": 32
                            }
                        ]}
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
