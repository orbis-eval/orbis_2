<template>
  <span
      v-html="getCharacter()"
      :class="[
          (char.annotation ? `marked type_${char.type}` : ''),
          (char.annotation && char.annotation.selected ? 'selected' : ''),
          (char.annotation ? char.annotation.status : ''),
      ]"
      :data-charindex="char.charIndex"
      :data-annotationindex="char.annotationIndex"
      @mouseover="mouseOver()"
      @mouseout="mouseOut()"
      @click="$emit('clicker', char.annotation)"
  ></span>
  <span v-if="char.char === '\n'" class="spacer"></span>
</template>

<style>
.spacer {
  flex-basis: 100%;
}
</style>

<script>
export default {
  name: "AnnotationChar",
  props: {
    char: {},
  },
  emits: ['clicker'],
  data() {
    return {
    }
  },
  mounted() {
  },
  methods: {
    getCharacter() {
      switch (this.char.char) {
        case ' ':
        case '\n': return '&nbsp;';
        default: return this.char.char;
      }
    },
    mouseOver() {
      if (!this.char.annotation) {
        return;
      }
      document.querySelectorAll('.marked.hover')
          .forEach(e => e.classList.remove('hover'));
      document.querySelectorAll(`.marked[data-annotationindex="${this.char.annotationIndex}"]`)
          .forEach(e => e.classList.add('hover'));
    },
    mouseOut() {
      if (!this.char.annotation) {
        return;
      }
      document.querySelectorAll('.marked.hover')
          .forEach(e => e.classList.remove('hover'));
    }
  }
}
</script>
