import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import locale_de from './assets/locale_de.json'
import locale_en from './assets/locale_en.json'
import {SettingsService} from '@/services/Settings.service';

const app = createApp(App);

let locale = locale_de;
if (localStorage && localStorage.getItem('locale')) {
    switch (localStorage.getItem('locale')) {
        case 'en': locale = locale_en; break;
    }
}

SettingsService.LoadDataFromStorage();
SettingsService.LoadDataFromQueryString();
if (!SettingsService.AnnotatorId) {
    SettingsService.GetDataFromUser();
}

app.directive('locale', (el, binding) => {
    el.textContent = locale[binding.value];
});

app.directive('title', (el, binding) => {
    el.title = locale[binding.value];
});

app.use(router);

app.mount('#app');
