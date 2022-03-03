<template>
  <h2 v-locale="'keyboardlegend-title'"></h2>
  <ul>
    <li class="marked type_x">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-arrow-turn-down fa-rotate-90 fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-enter'"></span>
    </li>
    <li class="marked type_x">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-backspace fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-backspace'"></span>
    </li>
    <li class="marked type_x">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-delete-left fa-rotate-180 fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-delete'"></span>
    </li>
    <li class="marked type_x">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-arrow-right fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-arrow-right'"></span>
    </li>
    <li class="marked type_x">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-arrow-left fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-arrow-left'"></span>
    </li>
    <li class="marked type_x">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-a fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-unshift'"></span>
    </li>
    <li class="marked type_x">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-s fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-shift'"></span>
    </li>
    <li class="marked type_x">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-d fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-pop'"></span>
    </li>
    <li class="marked type_x">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-f fa-stack-1x fa-inverse"></i>
      </span>
      <span v-locale="'keyboardlegend-push'"></span>
    </li>

    <li class="">&nbsp;</li>
    <li v-for="(type, index) of annotationTypes" class="marked" :class="['type_' + index]">
      <span class="fa-stack fa-1x">
        <i class="fa-solid fa-square fa-stack-2x"></i>
        <i class="fa-solid fa-stack-1x" :class="[ 'fa-' + keyList[index] ]"></i>
      </span>
      {{ type }}
    </li>
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
  }
}
</script>

<style scoped>
h2, ul {
  padding: 0 .5em 0;
}

li {
  padding: .2em;
  list-style: none;
}

.type_x {
  background-color: var(--color-border);
  color: var(--color-text);
  font-size: .9em;
}
</style>
