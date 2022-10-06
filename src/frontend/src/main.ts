import {createApp} from 'vue';
import App from './App.vue';
import router from './router';
import {SettingsService} from '@/services/Settings.service';
import LocaleService from '@/services/Locale.service';

const app = createApp(App);


SettingsService.LoadDataFromStorage();
SettingsService.LoadDataFromQueryString();
if (!SettingsService.Annotator) {
    SettingsService.GetDataFromUser();
}

app.directive('locale', (el, binding) => {
    el.textContent = LocaleService.Get(binding.value);
});

app.directive('title', (el, binding) => {
    el.title = LocaleService.Get(binding.value);
});

app.use(router);

app.mount('#app');
