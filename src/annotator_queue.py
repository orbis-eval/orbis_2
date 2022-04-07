# Import required for eval operation (_id of type ObjectId will be queried)
from bson.objectid import ObjectId

from src.db import DB


class AnnotatorQueue:

    def __init__(self, db: DB):
        self.__db = db
        self.__da_ids = set()
        self.__queue = []

    async def add_document_annotation(self, document_annotation):
        if (da_id := document_annotation.get('da_id')) not in self.__da_ids:
            if success := await self.__db.add_annotator_queue_entry(document_annotation):
                self.__queue.append(document_annotation)
                self.__da_ids.add(da_id)
                return True
        return False

    def __filter_queue(self, corpus_name, annotator, logical_operator):
        queue_filter = eval(f'filter(lambda q: '
                            f'q["corpus_name"] == "{corpus_name}" {logical_operator} '
                            f'q["annotator"] == "{annotator}", '
                            f'{self.__queue})')
        return list(queue_filter)

    async def get_id_for_annotation(self, corpus_name=None, annotator=None):
        da_id = None

        if not self.__queue:
            return {}
        if not corpus_name and not annotator:
            da_id = self.__queue[0].get('da_id')
        elif corpus_name and annotator:
            if filtered_list := self.__filter_queue(corpus_name, annotator, 'and'):
                da_id = filtered_list[0].get('da_id')
        else:
            if filtered_list := self.__filter_queue(corpus_name, annotator, 'or'):
                da_id = filtered_list[0].get('da_id')

        if da_id:
            if success := await self.__remove_document_annotation(da_id):
                return da_id
        return None

    def get_document_annotation_status(self, da_id):
        if da_id in self.__da_ids:
            document_annotation = list(filter(lambda q: q['da_id'] == da_id, self.__queue))[0]
            return document_annotation.get('status')

    def update_document_annotation_status(self, da_id, new_status):
        if da_id in self.__da_ids:
            document_annotation = list(filter(lambda q: q['da_id'] == da_id, self.__queue))[0]
            document_annotation['status'] = new_status
            return True
        return False

    async def load_queue_from_db(self):
        if annotator_queue := await self.__db.get_annotator_queue_entries():
            # walrus operator doesnt allow tuple unpacking
            self.__queue = annotator_queue[0]
            self.__da_ids = annotator_queue[1]

    async def __remove_document_annotation(self, da_id):
        if da_id in self.__da_ids:
            document_annotation = list(filter(lambda q: q['da_id'] == da_id, self.__queue))[0]
            if success := await self.__db.remove_annotator_queue_entry(da_id):
                self.__queue.remove(document_annotation)
                self.__da_ids.remove(da_id)
                return True
        return False
