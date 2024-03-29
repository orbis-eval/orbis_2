<script setup>
import {AnnotationService} from "../services/Annotation.service";
</script>

<template>
  <h2 v-locale="'keyboardlegend-title'"></h2>
  <ul>
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

    <li class="">&nbsp;</li>
    <li v-for="(type, index) of annotationTypes"
        class="marked types click"
        :class="['type_' + type.index]"
        @click="simulateKey(type.key, getKeyCode(keyList[index]))"
    >
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-stack-1x" :class="[ 'fa-' + keyList[index] ]"></i>
      </span>
      {{ type.caption }}
    </li>
    <li class="">&nbsp;</li>
    </ul>

  <h2 v-locale="'mouselegend-title'"></h2>
  <ul>
    <li class="marked type_x" v-locale="'mouselegend-click'"></li>
    <li class="marked type_x" v-locale="'mouselegend-drag'"></li>
    <li class="marked type_x" v-locale="'mouselegend-dblclick'"></li>
    <li class="marked type_x" v-locale="'mouselegend-dblclickshift'"></li>
    <li class="">&nbsp;</li>
  </ul>

  <h2 v-locale="'documentlegend-title'"></h2>
  <ul>
    <li class="marked type_x click" @click="save()"><span v-locale="'documentlegend-save'"></span></li>
    <li class="marked type_x click" @click="save(true)" v-locale="'documentlegend-savenext'"></li>
  </ul>
</template>

<script>
export default {
  name: "AnnotationTypeList",
  data() {
    return {
      keyList: [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p']
    }
  },
  props: {
    annotationTypes: {
      type: Array,
      default: []
    }
  },
  /**
   * Click-Event nach oben propagieren
   */
  emits: ['clicker'],
  methods: {
    /**
     * Simuliert einen Tastenanschlag, um eine Aktion auszuführen
     * @param key Taste
     * @param code Tastencode
     */
    simulateKey(key, code = key) {
      document.dispatchEvent(new KeyboardEvent("keydown", {key, code}));
    },
    /**
     * gibt den Tastencode anhand der Taste zurück
     * @param key Taste
     * @returns {string} Tastencode
     */
    getKeyCode(key) {
      return key <= 9 ? 'Digit' + key : 'Key' + key.toUpperCase()
    },
    save(next = false) {
      AnnotationService.SaveDocumentAnnotations(next);
    }
  }
}
</script>

<style scoped>
h2, ul {
  padding: 0 .5em 0;
}

li.marked {
  padding: .2em;
  list-style: none;
  user-select: none;
  user-focus: none;
  box-shadow: none;
  border-bottom: 1px solid #181818;
}

li.types {
  color: #181818;
}

li.click {
  cursor: pointer;
}

.type_x {
  background-color: var(--color-border);
  color: var(--color-text);
  font-size: .9em;
}
</style>
