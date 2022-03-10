import datetime

import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class DB:

    def __init__(self, host='localhost', port=27017, db_name='orbis'):
        self.__client = MongoClient(host=host, port=port)
        self.__db_name = db_name
        self.__db = self.__client[db_name]
        self.__db['corpus'].create_index('corpus_name', unique=True)
        self.__db['document'].create_index([('id', pymongo.ASCENDING),
                                            ('corpus_name', pymongo.ASCENDING)], unique=True)

    def _delete(self):
        self.__client.drop_database(self.__db_name)

    def __insert(self, table_name, record):
        try:
            result = self.__db[table_name].insert_one(record)
        except DuplicateKeyError:
            print('Record already exists.')
            return None
        print(f'Inserted record with id {result.inserted_id}')
        return str(result.inserted_id)

    def __get_record(self, table_name, record_filter):
        return self.__db[table_name].find_one(record_filter)

    def __get_record_id(self, table_name, record_filter):
        return str(self.__db[table_name].find_one(record_filter).get('_id'))

    def __get_records(self, table_name, record_filter):
        return list(self.__db[table_name].find(record_filter))

    def _add_document_annotation(self, d_id, annotator, iteration_id=0, precessor='NEW'):
        document_annotation_record = {'d_id': d_id,
                                      'annotator': annotator,
                                      'iteration_id': iteration_id,
                                      'datetime': datetime.datetime.today().strftime('%Y-%m-%d'),
                                      'precessor': precessor}
        document_annotation_id = self.__insert('document_annotation', document_annotation_record)
        return document_annotation_id

    def _add_annotations(self, da_id, d_id, record):
        annotation_record = {'da_id': da_id,
                             'd_id': d_id,
                             'annotations': record}
        annotation_id = self.__insert('annotation', annotation_record)
        return annotation_id

    def create_corpus(self, corpus_name, description):
        record = {'corpus_name': corpus_name,
                  'description': description}
        if not (corpus_id := self.__insert('corpus', record)):
            corpus_filter = {'corpus_name': corpus_name}
            corpus_id = self.__get_record_id('corpus', corpus_filter)
        return corpus_id

    def add_document(self, d_origin_id, corpus_name, text, annotator, annotations):
        document_record = {'id': d_origin_id,
                           'corpus_name': corpus_name,
                           'content': text}
        if not (d_id := self.__insert('document', document_record)):
            document_filter = {'id': d_origin_id,
                               'corpus_name': corpus_name}
            d_id = self.__get_record_id('document', document_filter)
            return d_id, None, None
        da_id = self._add_document_annotation(d_id, annotator)
        annotation_id = self._add_annotations(da_id, d_id, annotations)

        return d_id, da_id, annotation_id

    def get_document_content(self, d_id):
        record_filter = {'d_id': d_id}
        if result := self.__get_record('document', record_filter):
            return result.get('content', '')

    def get_document_annotations(self, da_id):
        record_filter = {'da_id': da_id}
        if result := self.__get_record('annotation', record_filter):
            return result.get('annotations', '')

    def save_document_annotations(self, annotations, annotator, iteration_id, da_id):
        document_filter = {'da_id': da_id}
        d_id = self.__get_record('document', document_filter)
        new_da_id = self._add_document_annotation(d_id, annotator, iteration_id, da_id)
        annotation_id = self._add_annotations(da_id, d_id, annotations)
        return new_da_id, annotation_id

