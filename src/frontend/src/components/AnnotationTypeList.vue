<script setup>
import {AnnotationType} from '@/models/annotation-type';
</script>

<template>
  <h2 v-locale="'metadata-title'"
      v-if="annotationMeta && annotationMeta.display"
      @click="toggleCollapse(annotationMetaCollapsed)"
      :class="annotationMetaCollapsed.value ? 'collapsed' : ''"
      class="metadata"
  ></h2>
  <div v-if="annotationMetaCollapsed.value === false && annotationMeta.display"
       class="metadata"
  >
    <fieldset v-for="(value, key, index) in annotationMeta.display" :key="`${ key }-${ index }`">
      <legend>{{ key }}</legend>
      <div>{{ value }}</div>
    </fieldset>
  </div>

  <h2 v-locale="'annotation-types'"
      @click="toggleCollapse(annotationTypesCollapsed)"
      :class="annotationTypesCollapsed.value ? 'collapsed' : ''"
      class="types"
  ></h2>
  <ul v-if="annotationTypesCollapsed.value === false"
      class="types"
  >
    <li v-for="(type, index) of annotationTypes"
        :key="`${ type }-${ index }`"
        class="marked types click"
        :class="['type_' + type.index]"
        @click="simulateKey(type.key, getKeyCode(keyList[index]))"
    >
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-stack-1x fa-inverse" :class="[ 'fa-' + keyList[index] ]"></i>
      </span>
      {{ type.caption }}
    </li>
    <li
        class="marked types click addtype"
        :class="['type_' + annotationTypes.length]"
        v-if="annotationTypes.length <= keyList.length"
    >
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-stack-1x fa-inverse" :class="[ 'fa-' + keyList[annotationTypes.length] ]"></i>
      </span>
      <span v-locale="'add-new-type'" @click="addNewType()"></span>
    </li>
  </ul>

  <h2 v-locale="'keyboardlegend-title'"
      @click="toggleCollapse(keyboardlegendCollapsed)"
      :class="keyboardlegendCollapsed.value ? 'collapsed' : ''"
  ></h2>
  <ul v-if="keyboardlegendCollapsed.value === false">
    <li class="marked type_x click" @click="simulateKey('Enter')">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-arrow-turn-down fa-rotate-90 fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-enter'"></span>
    </li>
    <li class="marked type_x click" @click="simulateKey('Delete')">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-backspace fa-stack-1x fa-inverse"></i>
      </span>/<span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-delete-left fa-rotate-180 fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-delete'"></span>
    </li>
    <li class="marked type_x click" @click="simulateKey('ArrowRight')">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-arrow-right fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-arrow-right'"></span>
    </li>
    <li class="marked type_x click" @click="simulateKey('ArrowLeft')">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-arrow-left fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-arrow-left'"></span>
    </li>
    <li class="marked type_x click" @click="simulateKey('KeyA')">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-a fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-unshift'"></span>
    </li>
    <li class="marked type_x click" @click="simulateKey('KeyS')">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-s fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-shift'"></span>
    </li>
    <li class="marked type_x click" @click="simulateKey('KeyX')">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-x fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-pop'"></span>
    </li>
    <li class="marked type_x click" @click="simulateKey('KeyC')">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-c fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-push'"></span>
    </li>
    <li class="marked type_x click" @click="simulateKey('KeyA', 'KeyA', 'Shift')">
      <span class="shift">Shift</span> +
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-a fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-unshift-word'"></span>
    </li>
    <li class="marked type_x click" @click="simulateKey('KeyS', 'KeyS', 'Shift')">
      <span class="shift">Shift</span> +
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-s fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-shift-word'"></span>
    </li>
    <li class="marked type_x click" @click="simulateKey('KeyX', 'KeyX', 'Shift')">
      <span class="shift">Shift</span> +
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-x fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-pop-word'"></span>
    </li>
    <li class="marked type_x click" @click="simulateKey('KeyC', 'KeyC', 'Shift')">
      <span class="shift">Shift</span> +
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-c fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-push-word'"></span>
    </li>
  </ul>

  <h2 v-locale="'mouselegend-title'"
      @click="toggleCollapse(mouselegendCollapsed)"
      :class="mouselegendCollapsed.value ? 'collapsed' : ''"
  ></h2>
  <ul v-if="mouselegendCollapsed.value === false">
    <li class="marked type_x" v-locale="'mouselegend-click'"></li>
    <li class="marked type_x" v-locale="'mouselegend-drag'"></li>
    <li class="marked type_x" v-locale="'mouselegend-dblclick'"></li>
    <li class="marked type_x" v-locale="'mouselegend-dblclickshift'"></li>
  </ul>

</template>

<script>
import {AnnotationService} from "@/services/Annotation.service";

export default {
  name: "AnnotationTypeList",
  data() {
    return {
      annotationTypes: [],
      keyList: [],
      annotationMeta: {},
      annotationMetaCollapsed: {key: 'annotationMetaCollapsed', value: false},
      annotationTypesCollapsed: {key: 'annotationTypesCollapsed', value: false},
      keyboardlegendCollapsed: {key: 'keyboardlegendCollapsed', value: false},
      mouselegendCollapsed: {key: 'mouselegendCollapsed', value: false},
    }
  },
  /**
   * Click-Event nach oben propagieren
   */
  emits: ['clicker'],
  methods: {
    /**
     * Initialisiert alle Daten vom Service
     */
    init() {
      this.annotationTypes = AnnotationService.AnnotationTypes;
      this.annotationMeta = AnnotationService.DocumentMeta;
      this.keyList = AnnotationService.TypeKeyList;
      this.annotationTypesCollapsed.value = !this.annotationTypesCollapsed.value;
      setTimeout(() => {
        this.annotationTypesCollapsed.value = !this.annotationTypesCollapsed.value;
      });
    },
    /**
     * toggle collapse status
     * @param element Legende
     */
    toggleCollapse(element) {
      element.value = !element.value;
      localStorage.setItem(element.key, element.value);
    },
    /**
     * Simuliert einen Tastenanschlag, um eine Aktion auszuführen
     * @param key Taste
     * @param code Tastencode
     * @param specialKey Shift, Ctrl oder Alt
     */
    simulateKey(key, code = key, specialKey = null) {
      const keyboardEvent = new KeyboardEvent("keydown", {key, code});
      if (specialKey) {
        switch (specialKey.toLowerCase()) {
          case 'shift':
            keyboardEvent.shiftKey = true;
            break;
          case 'alt':
            keyboardEvent.altKey = true;
            break;
          case 'ctrl':
            keyboardEvent.ctrlKey = true;
            break;
        }
      }
      document.dispatchEvent(keyboardEvent);
    },
    /**
     * gibt den Tastencode anhand der Taste zurück
     * @param key Taste
     * @returns {string} Tastencode
     */
    getKeyCode(key) {
      return key <= 9 ? 'Digit' + key : 'Key' + key.toUpperCase()
    },
    /**
     * Prompt für neuen Type anzeigen und dem Service übergeben
     */
    addNewType() {
      let caption = prompt('Wie soll der Typ heissen?');
      if (!caption) {
        return;
      }
      let index = this.annotationTypes.length;
      let newType = new AnnotationType({ index, key: this.keyList[index], caption});
      AnnotationService.AddAnnotationType(newType);
    }
  },
  mounted() {
    this.annotationMetaCollapsed.value = localStorage.getItem('annotationMetaCollapsed') === 'true';
    this.annotationTypesCollapsed.value = localStorage.getItem('annotationTypesCollapsed') === 'true';
    this.keyboardlegendCollapsed.value = localStorage.getItem('keyboardlegendCollapsed') === 'true';
    this.mouselegendCollapsed.value = localStorage.getItem('mouselegendCollapsed') === 'true';

    this.init();
    AnnotationService.Changes.subscribe(() => {
      this.init();
    });
  }
}
</script>

<style scoped>
h2 {
  cursor: pointer;
}

h2:hover {
  opacity: 0.8;
}

h2::before {
  content: "\f146";
  font-family: "Font Awesome 6 Free";
  font-size: .75em;
  margin-right: .5em;
}

h2.collapsed::before {
  content: "\f150";
}

h2, ul {
  padding: 0 .5em 0;
}

fieldset {
  margin: 0 0.5em 0.5em;
  padding: 0em .75em;
}

ul {
  margin-bottom: 1em;
}

li.marked {
  padding: .2em;
  list-style: none;
  user-select: none;
  user-focus: none;
  box-shadow: none;
  border-bottom: 1px solid var(--color-border);
}

li.marked .svg-inline--fa {
  height: 1em;
  width: 1em;
}

li.marked .fa-stack-2x {
  color: var(--vt-c-divider-dark-1);
}

li.types {
  color: #181818;
}

li.addtype {
  font-style: italic;
}

li.click {
  cursor: pointer;
}

.type_x {
  background-color: var(--color-border);
  color: var(--color-text);
  font-size: .9em;
}

.shift {
  background-color: var(--color-border);
  margin: 0 .4em;
  padding: .5em;
  border-radius: 4px;
  font-size: .75em;
}

</style>
