<script setup>
import sampleData from '../assets/sample.json';
import AnnotationChar from "./AnnotationChar.vue";
</script>
<template>
  <div id="annotation_container" v-if="chars">
    <AnnotationChar v-for="char in chars" :char="char" @clicker="click($event)"></AnnotationChar>
  </div>
</template>

<style lang="scss">
@import '@/assets/annotationtypes.scss';
</style>

<style scoped>
#annotation_container {
  display: flex;
  flex-wrap: wrap;
  font-family: monospace;

}
</style>

<script>

import {enAnnotationStatus} from "@/models/enAnnotationStatus";

export default {
  data() {
    return {
      chars: [],
      annotationText: '',
      annotations: [],
      annotationTypes: [],
    };
  },
  methods: {
    click(annotation) {
      // console.log('click', event);
      const selected = !annotation.selected;
      this.annotations
          .filter(e => e.selected)
          .forEach(e => e.selected = false);
      annotation.selected = selected;
    },
    handleKeyboardEvents(event) {
      switch (event.code) {
        // case 'Space':
        case 'Enter':
          this.approveAnnotation();
          this.selectNextAnnotation();
          break;
        case 'Backspace':
        case 'Delete':
          this.deleteAnnotation();
          this.selectNextAnnotation();
          break;
        case 'ArrowRight':
          if (event.shiftKey) {
            this.editAnnotation('start', -1);
          } else if (event.altKey) {
            this.editAnnotation('end', 1);
          } else {
            this.selectNextAnnotation();
          }
          break;
        case 'ArrowLeft':
          if (event.shiftKey) {
            this.editAnnotation('start', 1);
          } else if (event.altKey) {
            this.editAnnotation('end', -1);
          } else {
            this.selectNextAnnotation(true);
          }
          break;
      }
    },
    approveAnnotation() {
      const selected = this.annotations.find(e => e.selected);
      if (!selected) {
        return;
      }
      if (selected.status !== enAnnotationStatus.edited) {
        selected.status = enAnnotationStatus.approved;
      }
    },
    deleteAnnotation() {
      const selected = this.annotations.find(e => e.selected);
      if (!selected) {
        return;
      }
      selected.status = enAnnotationStatus.deleted;
    },
    editAnnotation(dir, amount = 1) {
      const selected = this.annotations.find(e => e.selected);
      if (!selected) {
        return;
      }
      if (selected.status !== enAnnotationStatus.edited) {
        const newSelected = Object.assign({}, selected);
        newSelected.status = enAnnotationStatus.replaced;
        newSelected.selected = false;
        selected.status = enAnnotationStatus.edited;
        selected.selected = true;
        this.annotations.splice(this.annotations.indexOf(selected), 0, newSelected);
      }

      if (dir === 'start') {
        this.setAnnotationOnChar(
            selected.start - (amount > 0 ? 1 : 0),
            amount > 0 ? selected : null
        );
        selected.start -= amount;
      } else {
        this.setAnnotationOnChar(
            selected.end + (amount > 0 ? 0 : -1),
            amount > 0 ? selected : null
        );
        selected.end += amount;
      }
    },
    setAnnotationOnChar(charIndex, annotation) {
      const char = this.chars.find(e => e.charIndex === charIndex);
      char.annotation = annotation;
      char.type = annotation ? this.annotationTypes.indexOf(annotation.type) : null;
    },
    selectNextAnnotation(back = false) {
      let index = 0;
      const activeAnnotations = this.annotations.filter(e => e.status != enAnnotationStatus.replaced);
      const selected = activeAnnotations.find(e => e.selected);
      if (selected) {
        index = activeAnnotations.indexOf(selected) + (back ? -1 : 1);
        selected.selected = false;
      }
      if (index < 0) {
        index = 0;
      }
      if (index >= activeAnnotations.length) {
        index = activeAnnotations.length - 1;
      }
      let newSelected = activeAnnotations[index];
      newSelected.selected = true;

      let annotationContainerElement = document.getElementById('annotation_container');
      let newSelectedElement = annotationContainerElement
          .querySelector(`[data-charindex="${newSelected.start}"]`);
      let viewRect = annotationContainerElement.parentElement.getBoundingClientRect();
      let elemRect = newSelectedElement.getBoundingClientRect();
      if (elemRect.bottom > viewRect.bottom - (viewRect.height / 3)) {
        annotationContainerElement.parentElement.scrollTop = newSelectedElement.offsetTop - (viewRect.height / 2);
      }
      if (elemRect.top < viewRect.top + (viewRect.height / 3)) {
        annotationContainerElement.parentElement.scrollTop = newSelectedElement.offsetTop - (viewRect.height / 2);
      }
    }
  },
  mounted() {
    //todo: load data from server
    // fetch('@/assets/sample.json')
    //     // .then(response => response.json())
    //     .then(data => {
    //       console.log(data);
    //     });
    // this.annotationText = 'Hallo Welt';
    document.addEventListener('keydown', this.handleKeyboardEvents);
    this.annotationText = sampleData.text;
    this.annotations = []
        .concat(sampleData.gold_standard_annotation.certificates)
        .concat(sampleData.gold_standard_annotation.course_contents)
        .concat(sampleData.gold_standard_annotation.target_groups)
        .concat(sampleData.gold_standard_annotation.unknown)
        .sort((a, b) => a.start > b.start ? 1 : -1);
    this.annotations.forEach(e => e.status = enAnnotationStatus.pending);
    this.annotationTypes = this.annotations
        .map(e => e.type)
        .filter((e, i, a) => a.indexOf(e) === i);

    this.chars = this.annotationText
        .split('')
        .map((e, i) => {
          const currentAnnotation = this.annotations.find(f => f.start <= i && f.end > i);
          return {
            char: e,
            charIndex: i,
            annotation: currentAnnotation,
            annotationIndex: currentAnnotation ? this.annotations.indexOf(currentAnnotation) : null,
            type: currentAnnotation ? this.annotationTypes.indexOf(currentAnnotation.type) : null
          };
        });
  },
}
</script>
