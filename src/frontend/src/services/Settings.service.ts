
export class SettingsService {
    private static _annotatorid: string;
    private static _previousdocumentid: string;
    private static _documentid: string;

    public static get AnnotatorId() {
        return this._annotatorid;
    }

    public static get PreviousDocumentId(): string {
        return this._previousdocumentid;
    }

    public static get DocumentId(): string {
        return this._documentid;
    }

    private static saveDataIntoSotrage() {
        if (this._annotatorid) {
            localStorage.setItem('annotatorid', this._annotatorid);
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
        this._previousdocumentid = localStorage.getItem('prevdid');
        this._documentid = localStorage.getItem('documentid');
    }

    public static LoadDataFromQueryString() {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('annotatorid')) {
            this._annotatorid = urlParams.get('annotatorid');
        }
        if (urlParams.has('documentid')) {
            this._documentid = urlParams.get('documentid');
        }
        this.saveDataIntoSotrage();
    }

    public static GetDataFromUser() {
        this._annotatorid = prompt('Bitte geben Sie Ihre AnnotatorID ein.');
        this._documentid = prompt('Bitte geben Sie die DokumentID ein.');
        this.saveDataIntoSotrage();
    }

    public static ResetAnnotatorId() {
        const annotatorid = prompt('Bitte geben Sie Ihre AnnotatorID ein.', this._annotatorid || '');
        if (!!annotatorid && annotatorid !== this._annotatorid) {
            this._annotatorid = annotatorid;
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
}
