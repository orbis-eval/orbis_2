import {Subject} from 'rxjs';

export class SettingsService {
    private static _annotator: string;
    private static _previousdocumentid: string;
    private static _documentid: string;
    private static _corpusname: string;

    public static Changes = new Subject();

    public static get Annotator() {
        return this._annotator;
    }

    public static get PreviousDocumentId(): string {
        return this._previousdocumentid;
    }

    public static get DocumentId(): string {
        return this._documentid;
    }

    public static get CorpusName(): string {
        return this._corpusname;
    }

    public static AllData() {
        return {
            Annotator: this.Annotator,
            CorpusName: this.CorpusName,
            PreviousDocumentId: this.PreviousDocumentId,
            DocumentId: this.DocumentId
        };
    }

    private static saveDataIntoSotrage() {
        if (this._annotator) {
            localStorage.setItem('annotator', this._annotator);
        }
        if (this._corpusname) {
            localStorage.setItem('corpusname', this._corpusname);
        }
        if (this._documentid) {
            const previousdocumentid = localStorage.getItem('documentid');
            if (this._documentid !== previousdocumentid) {
                this._previousdocumentid = previousdocumentid;
                localStorage.setItem('prevdid', this._previousdocumentid);
            }
            localStorage.setItem('documentid', this._documentid);
        }
    }

    public static LoadDataFromStorage() {
        this._annotator = localStorage.getItem('annotator');
        this._corpusname = localStorage.getItem('corpusname');
        this._previousdocumentid = localStorage.getItem('prevdid');
        this._documentid = localStorage.getItem('documentid');
        this.Changes.next(this.AllData());
    }

    public static LoadDataFromQueryString() {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('annotator')) {
            this._annotator = urlParams.get('annotator');
        }
        if (urlParams.has('corpusname')) {
            this._corpusname = urlParams.get('corpusname');
        }
        if (urlParams.has('documentid')) {
            this._documentid = urlParams.get('documentid');
        }
        this.Changes.next(this.AllData());
        this.saveDataIntoSotrage();
    }

    public static GetDataFromUser() {
        this._annotator = prompt('Bitte geben Sie Ihre AnnotatorID ein.');
        this._corpusname = prompt('Bitte geben Sie den Korpusnamen ein.');
        this.Changes.next(this.AllData());
        this.saveDataIntoSotrage();
    }

    public static ResetAnnotator() {
        const annotator = prompt('Bitte geben Sie Ihre AnnotatorID ein.', this._annotator || '');
        if (!!annotator && annotator !== this._annotator) {
            this._annotator = annotator;
            this.Changes.next(this.AllData());
            this.saveDataIntoSotrage();
        }
    }

    public static ResetCorpusName() {
        const corpusname = prompt('Bitte geben Sie den Korpusnamen ein.', this._corpusname || '');
        if (!!corpusname && corpusname !== this._corpusname) {
            this._corpusname = corpusname;
            this.Changes.next(this.AllData());
            this.saveDataIntoSotrage();
        }
    }

    public static ResetDocumentId() {
        const documentid = prompt('Bitte geben Sie die DokumentID ein.', this._documentid || '');
        if (!!documentid && documentid !== this._documentid) {
            this._documentid = documentid;
            this.Changes.next(this.AllData());
            this.saveDataIntoSotrage();
        }
    }

    public static SetDocumentId(documentid: string) {
        if (!!documentid && documentid !== this._documentid) {
            this._documentid = documentid;
            this.Changes.next(this.AllData());
            this.saveDataIntoSotrage();
        }
    }

    public static SetCorpusName(corpusname: string) {
        if (!!corpusname && corpusname !== this._corpusname) {
            this._corpusname = corpusname;
            this.Changes.next(this.AllData());
            this.saveDataIntoSotrage();
        }
    }
}
