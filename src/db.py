import datetime

from pymongo import MongoClient



class DB:

    def __init__(host='localhost', port=27017):
        self.__client = MongoClient(host=host, port=port)
        self.__db = self.__client.orbis

    def __insert(table_name, record):
        result = self.__db[table_name].insert_one(record)
        print(f'Inserted record with id {result.inserted_id}')
        return result.inserted_id

    def __get_record(table_name, record_filter):
        return self.__db[table_name].find(record_filter)

    def __get_records(table_name, record_filter):
        return list(self.__db[table_name].find(record_filter))

    def import_corpus(corpus_name, description, documents):
        record  ={'corpus_name': corpus_name,
                  'description': description}
        corpus_id = self.__insert('corpus', record)
        document_ids = []
        for document_record in documents:
            document['corpus_id'] = corpus_id
            document_id = self._insert('document', document_record)
            document_ids.append(document_id)
        return document_ids

    def get_document_content(self, d_id):
        record_filter = {'d_id': d_id}
        if result := self.__get_record('document', record_filter):
            return result.get('content', '')

    def get_document_annotations(self, da_id):
        record_filter = {'da_id': da_id}
        if result := self.__get_record('annotation', record_filter):
            return result.get('annotations', '')

    def save_document_annotations(annotations, annotator, da_id):
        d_id, annotator, iteration_id = tuple(da_id.split('-'))
        da_record = {'da_id': da_id,
                    'd_id': d_id,
                    'iteration_id': iteration_id,
                    'annotator': annotator,
                    'datetime': datetime.datetime.today().strftime('%Y-%m-%d'),
                    'precessor': ''}
        da_result = self.__insert('document_annotation', da_record)
        a_record = {'da_id': da_id,
                    'd_id': d_id,
                    'annotations': annotations}
        a_result = self.__insert('annotation', a_record)
        return (da_result and a_result)

