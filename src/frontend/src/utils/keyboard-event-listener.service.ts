import {Observable} from 'rxjs';

export class KeyboardEventListenerService {
    static Observer: Observable<any> = new Observable(observer => {
        if(keyboardObserverIndex++ != 0)
            return;
        document.addEventListener('keydown', ($event) => {
            observer.next($event);
            console.log($event);
        });
    });
}
let keyboardObserverIndex = 0;
export const KeyboardObserver = KeyboardEventListenerService.Observer;
