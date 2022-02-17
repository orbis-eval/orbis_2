import datetime

ANNOTATIONS = [{'surface_form': 'Hellow World',
               'start': 0,
               'end': 11,
               'entity_type': 'topic'}]

DOCUMENT_ANNOTATION = {'da_id': 'document_1-ner-1',
                       'iteration_id': 1,
                       'annotator': 'ner',
                       'datetime': datetime.datetime.now(),
                       'precessor': 'gold',
                       'annotation': ANNOTATIONS}

DOCUMENT_1 = {'content': 'Helo World, happy to be here',
              'document_annotations': [DOCUMENT_ANNOTATION]}

DB_CONTENT = {'test_corpus': [{'document_1': DOCUMENT_1 
                             }]
             }



class DB:
    
    def get_document_for_annotation():
        return DOCUMENT_ANNOTATION['da_id']

    def get_document_content():
        return DOCUMENT_1['content']

    def get_document_annotations():
        return ANNOTATIONS

    def save_document_annotations():
        print('Saved document annotations')
        return 200
        

TEST_DB = DB()

