
export class SettingsService {
    private static _annotatorid: string;
    private static _previousdocumentid: string;
    private static _documentid: string;
    private static _corpusname: string;

    public static get AnnotatorId() {
        return this._annotatorid;
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

    private static saveDataIntoSotrage() {
        if (this._annotatorid) {
            localStorage.setItem('annotatorid', this._annotatorid);
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
        this._annotatorid = localStorage.getItem('annotatorid');
        this._corpusname = localStorage.getItem('corpusname');
        this._previousdocumentid = localStorage.getItem('prevdid');
        this._documentid = localStorage.getItem('documentid');
    }

    public static LoadDataFromQueryString() {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('annotatorid')) {
            this._annotatorid = urlParams.get('annotatorid');
        }
        if (urlParams.has('corpusname')) {
            this._corpusname = urlParams.get('corpusname');
        }
        if (urlParams.has('documentid')) {
            this._documentid = urlParams.get('documentid');
        }
        this.saveDataIntoSotrage();
    }

    public static GetDataFromUser() {
        this._annotatorid = prompt('Bitte geben Sie Ihre AnnotatorID ein.');
        this._corpusname = prompt('Bitte geben Sie den Korpusnamen ein.');
        this.saveDataIntoSotrage();
    }

    public static ResetAnnotatorId() {
        const annotatorid = prompt('Bitte geben Sie Ihre AnnotatorID ein.', this._annotatorid || '');
        if (!!annotatorid && annotatorid !== this._annotatorid) {
            this._annotatorid = annotatorid;
            this.saveDataIntoSotrage();
        }
    }

    public static ResetCorpusName() {
        const corpusname = prompt('Bitte geben Sie den Korpusnamen ein.', this._corpusname || '');
        if (!!corpusname && corpusname !== this._corpusname) {
            this._corpusname = corpusname;
            this.saveDataIntoSotrage();
        }
    }

    public static ResetDocumentId() {
        const documentid = prompt('Bitte geben Sie die DokumentID ein.', this._documentid || '');
        if (!!documentid && documentid !== this._documentid) {
            this._documentid = documentid;
            this.saveDataIntoSotrage();
        }
    }

    public static SetDocumentId(documentid: string) {
        if (!!documentid && documentid !== this._documentid) {
            this._documentid = documentid;
            this.saveDataIntoSotrage();
        }
    }
}
