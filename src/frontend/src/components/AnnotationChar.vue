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
  /**
   * Properties
   */
  props: {
    char: {},
  },
  /**
   * Click-Event nach oben propagieren
   */
  emits: ['clicker'],
  methods: {
    /**
     * darzustellenden Char (bei Leerzeichen, Zeilenumbrüchen, etc.)
     * @returns {string|*}
     */
    getCharacter() {
      switch (this.char.char) {
        case ' ':
        case '\n': return '&nbsp;';
        default: return this.char.char;
      }
    },
    /**
     * Hover-Effekt für ganze Annotation (over)
     */
    mouseOver() {
      if (!this.char.annotation) {
        return;
      }
      document.querySelectorAll('.marked.hover')
          .forEach(e => e.classList.remove('hover'));
      document.querySelectorAll(`.marked[data-annotationindex="${this.char.annotationIndex}"]`)
          .forEach(e => e.classList.add('hover'));
    },
    /**
     * Hover-Effekt für ganze Annotation (out)
     */
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
