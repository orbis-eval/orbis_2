import locale_de from '@/assets/locale_de.json';
import locale_en from '@/assets/locale_en.json';
import {Subject} from 'rxjs';

class LocaleService {
    private _currentLocale = locale_de;
    Languages = ['de', 'en'];
    CurrentLanguage = 'de';

    Changes = new Subject();

    get Locale() {
        return this._currentLocale;
    }

    constructor() {
        this._currentLocale = locale_de;
        if (localStorage && localStorage.getItem('locale')) {
            const locale = localStorage.getItem('locale');
            if (locale && this.Languages.indexOf(locale) >= 0) {
                this.SetLocale(locale);
            }
        }
    }

    private _changes() {
        this.Changes.next({
            CurrentLanguage: this.CurrentLanguage,
            Locale: this.Locale
        });
    }

    Get(value: string): string {
        console.log('get...');
        return this._currentLocale[value] || '';
    }

    SetLocale(locale: 'de'|'en'): void {
        switch (locale) {
            case 'de':
                this._currentLocale = locale_de;
                this.CurrentLanguage = 'de';
                break;
            case 'en':
                this._currentLocale = locale_en;
                this.CurrentLanguage = 'en';
                break;
        }
        if (localStorage) {
            localStorage.setItem('locale', this.CurrentLanguage);
        }
        this._changes();
    }
}

export default new LocaleService();
