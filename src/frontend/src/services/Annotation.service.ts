import sampleData from '../assets/sample.json';
import {Annotation, enAnnotationStatus} from '@/models/annotation';
import {AnnotationType} from '@/models/annotation-type';

export class AnnotationService {
    static Document = '';
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
        return this.LoadSampleData();

        return fetch('/getDocumentForAnnotation')
            .then(response => {
              console.log(response);
              return response.json();
            })
            .then(data => {
              console.log(data);
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
}
