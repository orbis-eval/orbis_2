<script setup lang="ts">
</script>

<template>
  <h1><RouterLink to="/">orbis</RouterLink></h1>
  <header>
    <nav>
      <div class="left">
        <RouterLink to="/annotation" v-locale="'annotation'"></RouterLink>
      </div>

      <div class="center">
        <span></span>
      </div>

      <div class="right">
        <a id="bugreport" :href="`mailto:orbis@fhgr.ch?subject=orbis%20bug%20report&body=%0D%0A%0D%0A-----%0D%0ABitte%20nicht%20löschen:%0D%0Aaid:%20${annotatorid}%0D%0Apid:%20${previousdocumentid}%0D%0Adid:%20${documentid}%0D%0Acn:%20${corpusname}%0D%0A-----`">
          <i class="fa fa-bug"></i>
          <span>Bug Report</span>
        </a>
        <div id="document" :title="corpusname" @click="resetCorpusName()">
          <i class="fa fa-file"></i>
          <span>{{corpusname}}</span>
        </div>
        <div id="annotator" :title="annotatorid" @click="resetAnnotatorId()">
          <i class="fas fa-user"></i>
          <span>{{annotatorid}}</span>
        </div>
        <div id="language-switcher">
          <span><i v-locale="'language'"></i>: {{currentLang}}</span>
          <div id="language-switcher-selection">
            <div @click="selectLanguage('de')">DE</div>
            <div @click="selectLanguage('en')">EN</div>
          </div>
        </div>
        <div id="mode-toggler" @click="toggle()"></div>
      </div>
    </nav>
  </header>
  <RouterView />
</template>

<style>
@import '@/assets/base.scss';
</style>

<style scoped>
#language-switcher, #annotator, #document, #bugreport {
  position: relative;
  display: flex;
  align-items: center;
  padding: .4em 1em;
  margin: 0 .5em;
  background: var(--color-text);
  color: var(--color-background-mute);
  border: 2px solid var(--color-border);
  border-radius: 2em;
  cursor: pointer;
}
#language-switcher span, #annotator span, #document span, #bugreport span {
  display: block;
  padding-left: .5em;
  max-width: 10em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
#language-switcher-selection {
  display: none;
  position: absolute;
  top: 100%;
  right: 1em;
  background: var(--color-text);
  color: var(--color-background-mute);
  border: 2px solid var(--color-border);
  border-radius: .2em;
  z-index: 9999;
}
#language-switcher:hover #language-switcher-selection {
  display: block;
}
#language-switcher-selection div {
  cursor: pointer;
  padding: .4em 1em;
}
#language-switcher-selection div:hover {
  background: var(--color-background-soft);
  color: var(--color-text);
}
#mode-toggler {
  display: inline-block;
  position: relative;
  width: calc(3.3em + 4px);
  height: calc(1.8em + 4px);
  margin: 0 2rem 0 .5em;
  background: var(--color-text);
  border: 2px solid var(--color-border);
  border-radius: 1.2em;
  font-size: 1.2em;
  cursor: pointer;
}

#mode-toggler::after {
  content: "\f186";
  position: absolute;
  left: .1em;
  top: .1em;
  width: 1.6em;
  height: 1.6em;
  background: var(--color-background-mute);
  /*background: var(--color-heading);*/
  border-radius: 50%;
  font-family: 'Font Awesome 6 Free';
  text-align: center;
  color: var(--color-heading);
  transition: left .2s ease-in-out;
}

.light-mode #mode-toggler::after {
  content: "\f185";
  left: 1.6em;
}
</style>

<script lang="ts">
import {SettingsService} from '@/services/Settings.service';

const appElement = document.body;
const storageSetting = localStorage.getItem('screen-mode');
if (storageSetting === 'dark') {
  appElement?.classList.add('dark-mode');
} else {
  appElement?.classList.add('light-mode');
}

export default {
  data() {
    return {
      currentLang: (localStorage.getItem('locale') || 'de').toUpperCase(),
      annotatorid: SettingsService.AnnotatorId,
      corpusname: SettingsService.CorpusName,
      documentid: SettingsService.DocumentId,
      previousdocumentid: SettingsService.PreviousDocumentId
    };
  },
  methods: {
    selectLanguage(lang: string) {
      localStorage.setItem('locale', lang);
      window.location.reload();
    },
    toggle() {
      if (appElement?.classList.contains('light-mode')) {
        appElement?.classList.remove('light-mode');
        appElement?.classList.add('dark-mode');
      } else {
        appElement?.classList.add('light-mode');
        appElement?.classList.remove('dark-mode');
      }
      localStorage.setItem('screen-mode', appElement?.classList.contains('light-mode') ? 'light' : 'dark');
    },
    resetAnnotatorId() {
      SettingsService.ResetAnnotatorId();
      this.annotatorid = SettingsService.AnnotatorId;
    },
    resetCorpusName() {
      SettingsService.ResetCorpusName();
      this.corpusname = SettingsService.CorpusName;
      this.previousdocumentid = SettingsService.PreviousDocumentId;
      this.documentid = SettingsService.DocumentId;
    }
  },
  mounted() {
    this.annotatorid = SettingsService.AnnotatorId;
    this.corpusname = SettingsService.CorpusName;
    this.previousdocumentid = SettingsService.PreviousDocumentId;
    this.documentid = SettingsService.DocumentId;
  }
}
</script>
