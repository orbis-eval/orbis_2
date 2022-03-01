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
        <span>
        </span>
      </div>

      <div class="right">
        <span id="mode-toggler" @click="toggle()"></span>
      </div>
    </nav>
  </header>
  <aside></aside>
  <main>
    <RouterView />
  </main>
</template>

<style>
@import '@/assets/base.scss';
</style>

<style scoped>
h1 {
  grid-column: 1;
  grid-row: 1;
  padding: 2rem;
  font-size: 1.5em;
}

h1 a {
  font-weight: 800;
}

header {
  grid-column: 2;
  grid-row: 1;
}

nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

nav a {
  margin: 0 1rem;
}

aside {
  grid-column: 1;
  grid-row: 2;
}

main {
  grid-column: 2;
  grid-row: 2;
  padding: 1rem;
  max-width: 100%;
  max-height: 100%;
  overflow: auto;
  border-top: 1px solid rgba(127,127,127,0.1);
  scroll-behavior: smooth;
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
const appElement = document.body;
const storageSetting = localStorage.getItem('screen-mode');
if (storageSetting === 'dark') {
  appElement?.classList.add('dark-mode');
} else {
  appElement?.classList.add('light-mode');
}

export default {
  methods: {
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
