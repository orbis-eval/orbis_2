from typing import (Optional, 
                    List, 
                    Dict)

from pydantic import (BaseModel, 
                      Field)

class Annotation(BaseModel):
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



class Document(BaseModel):
    da_id: str = Field(..., description='Unique key for identifying document and annotartor within an iteration')
    annotator: str = Field(..., description='Service odr Person used for annotations')
    data: Optional[List[Annotation]] 


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

class Response(BaseModel):
    status: str = Field(..., description='Status of response', enum=['Success', 'Failed'])
    message: str = Field(..., description='Error Message if request could not be processed')
    content: Dict[str, Dict]

    class Config:
        schema_extra = {
                "example":
                {
                    "status": "Success",
                    "message": "",
                    "content": {"da_id": "some_da_id"}
                    }
                }
