from typing import List, Dict


class AnnotatorQueue:

    def __init__(self, document_annotations: List[Dict]=None):
        self.__da_ids = set()
        self.__queue = []

        if document_annotations:
            for da in document_annotations:
                self.add_document_annotation(da)

    def add_document_annotation(self, document_annotation):
        if (da_id := document_annotation.get('da_id')) not in self.__da_ids:
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

    def get_id_for_annotation(self, corpus_name=None, annotator=None):
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

        if not da_id:
            return {}
        else:
            self.__remove_document_annotation(da_id)
            return da_id

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

    def __remove_document_annotation(self, da_id):
        if da_id in self.__da_ids:
            document_annotation = list(filter(lambda q: q['da_id'] == da_id, self.__queue))[0]
            self.__queue.remove(document_annotation)
            self.__da_ids.remove(da_id)
