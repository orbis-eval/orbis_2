import {Annotation, enAnnotationStatus} from '@/models/annotation';
import {AnnotationType} from '@/models/annotation-type';
import {SettingsService} from '@/services/Settings.service';
import {Subject} from 'rxjs';

export class AnnotationService {
    static Document = '';
    static DocumentId = '';
    static DocumentMeta = {};
    static Annotations: Annotation[] = [];
    static AnnotationTypes: AnnotationType[] = [];
    static TypeKeyList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p'];
    public static Changes = new Subject();

    static GetTypeByKey(key: string): AnnotationType|null {
        return this.AnnotationTypes.find(e => e.key == key) || null;
    }
    static GetTypeByCaption(caption: string): AnnotationType|null {
        return this.AnnotationTypes.find(e => e.caption === caption) || null;
    }
    static GetTypeByAnnotation(annotation: Annotation): AnnotationType|null {
        return annotation ? this.GetTypeByCaption(annotation.type) : null;
    }

    private static changes() {
        this.Changes.next({
            Document: this.Document,
            DocumentId: this.DocumentId,
            DocumentMeta: this.DocumentMeta,
            Annotations: this.Annotations,
            AnnotationTypes: this.AnnotationTypes
        });
    }

    static GetDocumentForAnnotation() {
        this.Document = '';
        this.DocumentId = '';
        this.DocumentMeta = {};
        this.Annotations = [];
        this.AnnotationTypes = [];

        return fetch(`${import.meta.env.DEV ? 'http://localhost:63010/' : '/'}getDocumentForAnnotation?corpus_name=${SettingsService.CorpusName}&annotator=${SettingsService.Annotator}`)
            .then(response => {
              return response.json();
            })
            .then(data => {
                if (data.status_code !== 200) {
                    alert(data.message);
                    return;
                }
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

                SettingsService.SetCorpusName(data.content.corpus_name);
                SettingsService.SetDocumentId(data.content.da_id);
                this.changes();

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
            "annotator": SettingsService.Annotator || '',
            "data": {
                "d_id": this.DocumentId,
                "meta": this.DocumentMeta,
                "annotations": this.Annotations
                    .filter(e => {
                        return [enAnnotationStatus.APPROVED, enAnnotationStatus.NEW, enAnnotationStatus.EDITED].indexOf(e.status) >= 0
                    })
                    .map(e => ({
                    "key": e.key || Date.now(),
                    "type": e.type || '',
                    "surface_form": this.Document.substring(e.start, e.end) || '',
                    "start": e.start,
                    "end": e.end,
                    "scope": e.scope || '',
                    "meta": e.meta || {}
                }))
            }
        };

        return fetch('/saveDocumentAnnotations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        })
            .then(response => {
                return next ? window.location.reload() : response.json();
            })
            .catch(error => {
                console.error(error);
            });
    }

    static AddAnnotationType(annotationType: AnnotationType) {
        this.AnnotationTypes.push(annotationType);
        this.changes();
    }
}
