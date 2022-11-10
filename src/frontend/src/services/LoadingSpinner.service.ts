export class LoadingSpinnerService {
    private static _spinner = document.getElementById('loading_spinner');
    private static _spinnerCallStack: string[] = [];

    public static Show(callStackID?: string) {
        if (!this._spinner) {
            this._spinner = document.getElementById('loading_spinner');
        }
        if (!callStackID) {
            callStackID = this._generateUUID();
        }
        if (this._spinnerCallStack.indexOf(callStackID) >= 0) {
            return callStackID;
        }
        this._spinnerCallStack.push(callStackID);
        setTimeout(() => { this._spinner?.classList.add('active'); });
        return callStackID;
    }

    public static Close(callStackID: string) {
        if (this._spinnerCallStack.indexOf(callStackID) < 0) {
            return;
        }
        this._spinnerCallStack.splice(this._spinnerCallStack.indexOf(callStackID), 1);
        setTimeout(() => {
            if (this._spinnerCallStack.length === 0) {
                this._spinner?.classList.remove('active');
            }
        }, 100);
    }

    private static _generateUUID() { // Public Domain/MIT
        let d = new Date().getTime();//Timestamp
        let d2 = ((typeof performance !== 'undefined') && performance.now && (performance.now()*1000)) || 0;//Time in microseconds since page-load or 0 if unsupported
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            let r = Math.random() * 16;//random number between 0 and 16
            if(d > 0){//Use timestamp until depleted
                r = (d + r)%16 | 0;
                d = Math.floor(d/16);
            } else {//Use microseconds since page-load if supported
                r = (d2 + r)%16 | 0;
                d2 = Math.floor(d2/16);
            }
            return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
    }
}
