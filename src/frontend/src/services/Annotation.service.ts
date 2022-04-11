import sampleData from '../assets/sample3.json';
import {Annotation, enAnnotationStatus} from '@/models/annotation';
import {AnnotationType} from '@/models/annotation-type';
import {SettingsService} from '@/services/Settings.service';
import * as console from 'console';

export class AnnotationService {
    static Document = '';
    static DocumentId = '';
    static DocumentMeta = {};
    static Annotations: Annotation[] = [];
    static AnnotationTypes: AnnotationType[] = [];
    static TypeKeyList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p'];

    static GetTypeByKey(key: string): AnnotationType|null {
        return this.AnnotationTypes.find(e => e.key == key) || null;
    }
    static GetTypeByCaption(caption: string): AnnotationType|null {
        return this.AnnotationTypes.find(e => e.caption === caption) || null;
    }
    static GetTypeByAnnotation(annotation: Annotation): AnnotationType|null {
        return annotation ? this.GetTypeByCaption(annotation.type) : null;
    }

    static GetDocumentForAnnotation() {
        //return this.LoadSingleSample();
        // return this.LoadSampleData();
        //return this.LoadSampleData3();

        return fetch(`/getDocumentForAnnotation?corpus_name=${SettingsService.CorpusName}&annotator=${SettingsService.AnnotatorId}`)
            .then(response => {
              return response.json();
            })
            .then(data => {
                AnnotationService.Document = data.content.text;
                AnnotationService.DocumentId = data.content.annotations.d_id;
                AnnotationService.DocumentMeta = data.content.annotations.meta;
                AnnotationService.Annotations = data.content.annotations.annotations
                    .map(e => new Annotation(e))
                    .sort((a: Annotation, b: Annotation) => a.start > b.start ? 1 : -1);
                AnnotationService.Annotations.forEach((e, i) => {
                    e.status = enAnnotationStatus.PENDING;
                    e.index = i;
                });

                // Annotationstypen extrahieren
                AnnotationService.AnnotationTypes = AnnotationService.Annotations
                    .map(e => e.type)
                    .filter((e, i, a) => a.indexOf(e) === i)
                    .map((e, i) => new AnnotationType({ index: i, key: AnnotationService.TypeKeyList[i], caption: e}));

                SettingsService.SetDocumentId(data.content.da_id);

                return AnnotationService.Annotations;
            });
    }

    static SaveDocumentAnnotations(next = false) {
        const pendingAnnotations = this.Annotations
            .filter(e => {
                return [enAnnotationStatus.PENDING].indexOf(e.status) >= 0
            });
        if (pendingAnnotations.length > 0) {
            if (!confirm(`Es gibt noch ${pendingAnnotations.length} unbearbeitete Annotationen. Diese gehen beim speichern verloren.`)) {
                return new Promise((resolve) => { resolve(AnnotationService.Document); });
            }
        }
        const requestBody = {
            "da_id": SettingsService.DocumentId,
            "annotator": SettingsService.AnnotatorId,
            "data": {
                "d_id": this.DocumentId,
                "meta": this.DocumentMeta,
                "annotations": this.Annotations
                    .filter(e => {
                        return [enAnnotationStatus.APPROVED, enAnnotationStatus.NEW, enAnnotationStatus.EDITED].indexOf(e.status) >= 0
                    })
                    .map(e => ({
                    "key": e.key,
                    "type": e.type,
                    "surface_form": this.Document.substring(e.start, e.end),
                    "start": e.start,
                    "end": e.end,
                    "scope": e.scope,
                    "meta": e.meta
                }))
            }
        };

        return fetch('/saveDocumentAnnotations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        })
            .then(response => {
                return next ? this.GetDocumentForAnnotation() : response.json();
            })
            .catch(error => {
                console.error(error);
            });
    }

    static LoadSingleSample() {
        console.log('load single sample');

        AnnotationService.Document = 'Die Welt ist schön! Es gibt auch dreifach oder vierfach nominierte Annotationen! Mit einem weiteren Satz, in der Hoffnung, dass dieser umbricht, um zu sehen, wie sehr die Annotationen die darunter liegenden Sätze stören.';
        AnnotationService.Annotations = [
            new Annotation({ key: 1,  type: 'abc',  surface_form: '',  start: 4,  end: 8,  scope: '',  meta: {},  status: enAnnotationStatus.PENDING,  index: 1}),
            new Annotation({ key: 2,  type: 'uno',  surface_form: '',  start: 33,  end: 79,  scope: '',  meta: {},  status: enAnnotationStatus.PENDING,  index: 2}),
            new Annotation({ key: 3,  type: 'due',  surface_form: '',  start: 47,  end: 79,  scope: '',  meta: {},  status: enAnnotationStatus.PENDING,  index: 2}),
            new Annotation({ key: 4,  type: 'tre',  surface_form: '',  start: 56,  end: 79,  scope: '',  meta: {},  status: enAnnotationStatus.PENDING,  index: 2}),
            new Annotation({ key: 5,  type: 'quatro',  surface_form: '',  start: 67,  end: 79,  scope: '',  meta: {},  status: enAnnotationStatus.PENDING,  index: 2}),
            new Annotation({ key: 5,  type: 'quatro',  surface_form: '',  start: 67,  end: 79,  scope: '',  meta: {},  status: enAnnotationStatus.PENDING,  index: 2}),
        ];
        AnnotationService.AnnotationTypes = [
            new AnnotationType({ index: 0, key: 1, caption: 'abc' }),
            new AnnotationType({ index: 1, key: 2, caption: 'uno' }),
            new AnnotationType({ index: 2, key: 3, caption: 'due' }),
            new AnnotationType({ index: 3, key: 4, caption: 'tre' }),
            new AnnotationType({ index: 4, key: 5, caption: 'quatro' })
        ];
        return new Promise((resolve) => { resolve(AnnotationService.Document); });
    }

    static LoadSampleData() {
        AnnotationService.Document = sampleData.text;
        AnnotationService.Annotations = []
            .concat(sampleData.gold_standard_annotation.certificates)
            .concat(sampleData.gold_standard_annotation.course_contents)
            .concat(sampleData.gold_standard_annotation.target_groups)
            .concat(sampleData.gold_standard_annotation.unknown)
            .map(e => new Annotation(e))
            .sort((a, b) => a.start > b.start ? 1 : -1);
        AnnotationService.Annotations.forEach((e, i) => {
            e.status = enAnnotationStatus.PENDING;
            e.index = i;
        });

        // Annotationstypen extrahieren
        AnnotationService.AnnotationTypes = AnnotationService.Annotations
            .map(e => e.type)
            .filter((e, i, a) => a.indexOf(e) === i)
            .map((e, i) => new AnnotationType({ index: i, key: AnnotationService.TypeKeyList[i], caption: e}));

        return new Promise((resolve) => { resolve(AnnotationService.Document); });
    }

    static LoadSampleData3() {
        AnnotationService.Document = sampleData.content.text;
        AnnotationService.DocumentId = sampleData.content.annotations.d_id;
        AnnotationService.DocumentMeta = sampleData.content.annotations.meta;
        AnnotationService.Annotations = sampleData.content.annotations.annotations
            .map(e => new Annotation(e))
            .sort((a, b) => a.start > b.start ? 1 : -1);
        AnnotationService.Annotations.forEach((e, i) => {
            e.status = enAnnotationStatus.PENDING;
            e.index = i;
        });

        // Annotationstypen extrahieren
        AnnotationService.AnnotationTypes = AnnotationService.Annotations
            .map(e => e.type)
            .filter((e, i, a) => a.indexOf(e) === i)
            .map((e, i) => new AnnotationType({ index: i, key: AnnotationService.TypeKeyList[i], caption: e}));

        SettingsService.SetDocumentId(sampleData.content.da_id);

        return new Promise((resolve) => { resolve(AnnotationService.Document); });
    }
}
