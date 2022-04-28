import datetime
import os

import pymongo
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DEFAULT_URL = "mongodb://localhost:27017/?retryWrites=true&w=majority"


class DB:

    def __init__(self, mongo_url=None, db_name='orbis'):
        self.__mongo_url = mongo_url
        self.__db_name = db_name

    async def open(self):
        # check for database params:
        if self.__mongo_url:
            self.__client = AsyncIOMotorClient(self.__mongo_url)
        elif os.environ.get('MONGO_HOST') and os.environ.get('MONGO_PORT'):
            mongo_url = f"mongodb://" \
                        f"{os.environ.get('MONGO_HOST')}:" \
                        f"{os.environ.get('MONGO_PORT')}/" \
                        f"?retryWrites=true&w=majority"
        else:
            mongo_url = MONGO_DEFAULT_URL

        # init database:
        self.__client = AsyncIOMotorClient(mongo_url)
        print(f'using url "{mongo_url}" for database')
        self.__db = self.__client[self.__db_name]
        await self.__db['corpus'].create_index('corpus_name', unique=True)
        await self.__db['document'].create_index([('id', pymongo.ASCENDING),
                                                  ('corpus_name', pymongo.ASCENDING)], unique=True)

    def close(self):
        self.__client.close()

    async def _delete(self):
        await self.__client.drop_database(self.__db_name)

    async def __insert_record(self, table_name, record):
        '''
        Inserts new record to table. Returns None in case of DuplicateKeyError
        '''
        try:
            response = await self.__db[table_name].insert_one(record)
            print(f'Inserted record into {table_name} with id {response.inserted_id}')
            return str(response.inserted_id)
        except DuplicateKeyError:
            print('Record already exists.')
            return None

    async def __delete_record(self, table_name, record_filter):
        try:
            response = await self.__db[table_name].delete_one(record_filter)

            if response.deleted_count == 1:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    async def _get_record(self, table_name, record_filter):
        return await self.__db[table_name].find_one(record_filter)

    async def __get_record_attr(self, table_name, record_filter, attr):
        if result := await self.__db[table_name].find_one(record_filter):
            return result.get(attr)

    async def __get_record_id(self, table_name, record_filter, attr):
        result = await self.__get_record_attr(table_name, record_filter, attr)
        return str(result)

    async def __get_records(self, table_name, record_filter):
        if result := await self.__db[table_name].find(record_filter).to_list(1000000):
            return result
        return []

    async def _add_document_annotation(self, d_id, annotator, iteration_id=1, precessor='NEW'):
        document_annotation_record = {'d_id': ObjectId(d_id),
                                      'annotator': annotator,
                                      'iteration_id': iteration_id,
                                      'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                      'precessor': precessor}
        document_annotation_id = await self.__insert_record('document_annotation', document_annotation_record)
        return document_annotation_id

    async def _add_annotations(self, da_id, d_id, record):
        # check if d_id is equal, replace d_id in record with param.
        if record.get("d_id") != d_id:
            print(f'conflicting d_id detected: {d_id}, overwriting..')
            record["d_id"] = d_id

        annotation_record = {'da_id': ObjectId(da_id),
                             'd_id': ObjectId(d_id),
                             'annotations': record}
        return await self.__insert_record('annotation', annotation_record)

    async def _get_d_id_from_da_id(self, da_id):
        record_filter = {'_id': ObjectId(da_id)}
        return await self.__get_record_id('document_annotation', record_filter, 'd_id')

    async def create_corpus(self, corpus_name, description):
        record = {'corpus_name': corpus_name,
                  'description': description}
        print(record)
        if not (corpus_id := await self.__insert_record('corpus', record)):
            print('Hello world')
            corpus_filter = {'corpus_name': corpus_name}
            corpus_id = await self.__get_record_attr('corpus', corpus_filter, '_id')
            corpus_id = str(corpus_id)
        return corpus_id

    async def add_document(self, source_id, corpus_name, text, annotator, data):
        document_exists = False
        document_record = {'id': source_id,
                           'corpus_name': corpus_name,
                           'content': text}

        # checks if document already existed: None if already existed, d_id if insert was successful.
        if (d_id := await self.__insert_record('document', document_record)):
            da_id = await self._add_document_annotation(d_id, annotator)
            annotation_id = await self._add_annotations(da_id, d_id, data)

        else:
            print(f'Document with id {source_id} already in corpus {corpus_name}')
            document_filter = {'id': source_id,
                               'corpus_name': corpus_name}
            d_id = await self.__get_record_id('document', document_filter, '_id')
            annotation_filter = {'d_id': ObjectId(d_id)}
            da_id = await self.__get_record_id('annotation', annotation_filter, 'da_id')
            annotation_id = await self.__get_record_id('annotation', annotation_filter, '_id')
            document_exists = True

        return d_id, da_id, annotation_id, document_exists

    async def add_annotator_queue_entry(self, entry):
        if (result := await self.__insert_record('annotator_queue', entry)):
            print(f'{entry.get("da_id")} added to annotator queue.')
            return True
        else:
            print(f'{entry.get("da_id")} not added to annotator queue.')
            return False

    async def remove_annotator_queue_entry(self, da_id):
        record_filter = {'da_id': da_id}
        if (success := await self.__delete_record('annotator_queue', record_filter)):
            print(f'{da_id} removed from annotator queue')
            return True
        else:
            print(f'{da_id} not removed from annotator queue.')
            return False

    async def get_annotator_queue_entries(self):
        if entries := await self.__get_records('annotator_queue', {}):
            da_ids = {entry.get('da_id') for entry in entries}
            return entries, da_ids
        return [], set()

    async def get_document_content(self, da_id):
        d_id = await self._get_d_id_from_da_id(da_id)
        record_filter = {'_id': ObjectId(d_id)}
        return (await self._get_record('document', record_filter)).get('content', '')

    async def get_document_annotation_for_queue(self, da_id):
        da_result = self.__db['document_annotation'].aggregate([{"$lookup": {
            "from": "document",
            "localField": "d_id",
            "foreignField": "_id",
            "as": "linked_collections"
        }},
            {"$match": {"_id": ObjectId(da_id)}}
        ])

        if not da_result:
            print(f'No record found for id {da_id}')
            return None

        # There should always be exactly one element in the database since _id is unique
        da_result = (await da_result.to_list(length=1))[0]
        # Linked collections is a key with value of a list of one element
        d_result = da_result.get('linked_collections')[0]

        result = {'da_id': da_id,
                  'corpus_name': d_result.get('corpus_name'),
                  'annotator': da_result.get('annotator'),
                  'iteration_id': da_result.get('iteration_id'),
                  'status': 'new',
                  'lastUpdate': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        return result

    async def get_document_annotations(self, da_id):
        record_filter = {'da_id': ObjectId(da_id)}
        if annotations := await self._get_record('annotation', record_filter):
            return annotations.get('annotations', '')

    async def save_document_annotations(self, da_id, annotator, data):
        d_id = await self._get_d_id_from_da_id(da_id)

        new_da_id = await self._add_document_annotation(d_id=d_id,
                                                        annotator=annotator,
                                                        iteration_id=data['meta'].get('iteration', None),
                                                        precessor=da_id)
        annotation_id = self._add_annotations(new_da_id, d_id, data.get("annotations", []))
        return new_da_id
