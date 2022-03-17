<script setup lang="ts">
import {RouterLink, RouterView} from 'vue-router'
import HelloWorld from '@/components/HelloWorld.vue'
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
        <div id="language-switcher">
          <span>Sprache: {{currentLang}}</span>
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
#language-switcher {
  position: relative;
  padding: .4em 1em;
  margin: 0 1em;
  background: var(--color-text);
  color: var(--color-background-mute);
  border: 2px solid var(--color-border);
  border-radius: 2em;
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
  margin-right: 2rem;
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
import {KeyboardObserver} from '@/utils/keyboard-event-listener.service';

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
      currentLang: localStorage.getItem('locale').toUpperCase()
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
    }
  }
}
</script>
