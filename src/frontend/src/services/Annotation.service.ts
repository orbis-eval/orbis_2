import {Annotation, enAnnotationStatus} from '@/models/annotation';
import {AnnotationType} from '@/models/annotation-type';
import {SettingsService} from '@/services/Settings.service';
import {Subject} from 'rxjs';

export class AnnotationService {
    private static _spinner = document.getElementById('loading_spinner');
    static Document = '';
    static DocumentId = '';
    static DocumentMeta: any = {};
    static DocumentLoadTimeStamp: number;
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
            DocumentLoadDate: this.DocumentLoadTimeStamp,
            Annotations: this.Annotations,
            AnnotationTypes: this.AnnotationTypes,
        });
    }

    static GetDocumentForAnnotation() {
        this.Document = '';
        this.DocumentId = '';
        this.DocumentMeta = {};
        this.Annotations = [];
        this.AnnotationTypes = [];

        this._showLoadingSpinner();

        return fetch(`${import.meta.env.DEV ? 'http://localhost:63010/' : '/'}getDocumentForAnnotation?corpus_name=${SettingsService.CorpusName}&annotator=${SettingsService.Annotator}`)
            .then(response => {
                return response.json();
            })
            .then(this._handleGetResponse)
            .catch(error => {
                this._hideLoadingSpinner();
                console.error(error);
            });
    }

    static GetDocumentForViewOnly(da_id: string) {
        this.Document = '';
        this.DocumentId = '';
        this.DocumentMeta = {};
        this.Annotations = [];
        this.AnnotationTypes = [];

        this._showLoadingSpinner();

        return fetch(`${import.meta.env.DEV ? 'http://localhost:63010/' : '/'}getDocument?da_id=${da_id}`)
            .then(response => {
                return response.json();
            })
            .then(this._handleGetResponse)
            .catch(error => {
                this._hideLoadingSpinner();
                console.error(error);
            });
    }

    private static _handleGetResponse(data: any) {
        if (data.status_code !== 200) {
            alert(data.message);
            return;
        }
        AnnotationService.Document = data.content.text;
        AnnotationService.DocumentId = data.content.annotations.d_id;
        AnnotationService.DocumentMeta = data.content.annotations.meta;
        AnnotationService.Annotations = data.content.annotations.annotations
            .map((e: any) => new Annotation(e))
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
        AnnotationService._hideLoadingSpinner();
        AnnotationService.changes();
        AnnotationService.DocumentLoadTimeStamp = new Date().getTime();

        return AnnotationService.Annotations;
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

        return fetch(`${import.meta.env.DEV ? 'http://localhost:63010/' : '/'}/saveDocumentAnnotations`, {
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

    /**
     * gibt den TimeStamp zurück, basierend auf der Request Time in den Metadaten und dem Delta dazu
     * @constructor
     */
    static GetDocumentMetaTimeStamp(): number {
        const delta_in_seconds = (new Date().getTime() - this.DocumentLoadTimeStamp) / 1000;
        return Number(this.DocumentMeta['request_time']) + delta_in_seconds;
    }

    static AddAnnotationType(annotationType: AnnotationType) {
        this.AnnotationTypes.push(annotationType);
        this.changes();
    }

    private static _showLoadingSpinner() {
        if (!AnnotationService._spinner) {
            AnnotationService._spinner = document.getElementById('loading_spinner');
        }
        setTimeout(() => { AnnotationService._spinner?.classList.add('active'); });
    }

    private static _hideLoadingSpinner() {
        setTimeout(() => {
            AnnotationService._spinner?.classList.remove('active');
        }, 100);
    }

    static HideLoadingSpinner() {
        setTimeout(() => {
            AnnotationService._spinner?.classList.remove('active');
        }, 100);
    }
}
