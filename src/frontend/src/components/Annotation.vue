<script setup>
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
import {KeyboardObserver} from "@/utils/keyboard-event-listener.service";

export default {
  data() {
    return {
      chars: [],
      keyboardObserver: KeyboardObserver,
      keyList: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p']
    };
  },
  props: {
    annotationText: {
      type: String,
      default: ''
    },
    annotations: {
      type: Array,
      default: []
    },
    annotationTypes: {
      type: Array,
      default: []
    },
  },
  methods: {
    /**
     * ganze Annotation wählen bei klick auf einen Char
     * @param annotation Annotation
     */
    click(annotation) {
      if (!annotation) {
        return;
      }
      const selected = !annotation.selected;
      this.annotations
          .filter(e => e.selected)
          .forEach(e => e.selected = false);
      annotation.selected = selected;
    },
    /**
     * Keyborad Events abhandeln
     * @param event Keyboard Event
     */
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
          this.selectNextAnnotation();
          break;
        case 'ArrowLeft':
          this.selectNextAnnotation(true);
          break;
        case 'KeyA':
          this.editAnnotation('start', 1);
          break;
        case 'KeyS':
          this.editAnnotation('start', -1);
          break;
        case 'KeyX':
          this.editAnnotation('end', -1);
          break;
        case 'KeyC':
          this.editAnnotation('end', 1);
          break;
        case 'Digit1': case 'Digit2': case 'Digit3': case 'Digit4': case 'Digit5': case 'Digit6': case 'Digit7': case 'Digit8': case 'Digit9': case 'Digit0':
        case 'Numpad1': case 'Numpad2': case 'Numpad3': case 'Numpad4': case 'Numpad5': case 'Numpad6': case 'Numpad7': case 'Numpad8': case 'Numpad9': case 'Numpad0':
        case 'KeyQ': case 'KeyW': case 'KeyE': case 'KeyR': case 'KeyT': case 'KeyZ': case 'KeyU': case 'KeyI': case 'KeyO': case 'KeyP':
          this.setAnnotationType(event.key);
          break;
      }
    },
    /**
     * Annotation als «bestätigt» markieren
     */
    approveAnnotation() {
      const selected = this.annotations.find(e => e.selected);
      if (!selected) {
        return;
      }
      if (selected.status !== enAnnotationStatus.edited) {
        selected.status = enAnnotationStatus.approved;
      }
    },
    /**
     * Annotation als «gelöscht» markieren
     */
    deleteAnnotation() {
      const selected = this.annotations.find(e => e.selected);
      if (!selected) {
        return;
      }
      selected.status = enAnnotationStatus.deleted;
    },
    /**
     * Annotation anpassen (erweitern/reduzieren)
     * @param dir Richtung
     * @param amount Anzahl (+1 / -1)
     */
    editAnnotation(dir, amount = 1) {
      const selected = this.annotations.find(e => e.selected);
      if (!selected) {
        return;
      }
      this.replaceAnnotation(selected);

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
    /**
     * Einem Char-Objekt eine Annotation (oder null) zuweisen (bei ändern/erweitern/reduzieren der Annotation)
     * @param charIndex Index
     * @param annotation Annotation
     */
    setAnnotationOnChar(charIndex, annotation) {
      const char = this.chars.find(e => e.charIndex === charIndex);
      char.annotation = annotation;
      char.type = annotation ? this.annotationTypes.indexOf(annotation.type) : null;
      char.annotationIndex = annotation ? this.annotations.indexOf(annotation) : null;
    },
    /**
     * ersetzt die bestehende selektierte Annotation
     * @param selected selektierte Annotation
     */
    replaceAnnotation(selected) {
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
    },
    /**
     * setzt einen neuen AnnotationType und springt weiter
     * @param key Tastaturtaste
     */
    setAnnotationType(key) {
      const selected = this.annotations.find(e => e.selected);
      if (!selected) {
        return;
      }
      this.replaceAnnotation(selected);
      selected.status = enAnnotationStatus.edited;
      selected.typeIndex = this.keyList.indexOf(key);
      selected.type = this.annotationTypes[selected.typeIndex];
      this.selectNextAnnotation();
    },
    /**
     * nächste Annotation auswählen
     * @param back zurück zur vorherigen, statt zur nächsten
     */
    selectNextAnnotation(back = false) {
      let index = 0;
      const activeAnnotations = this.annotations.filter(e => e.status !== enAnnotationStatus.replaced);
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

      // View anpassen, damit das selektierte Wort immer im mittleren Drittel ist
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
  /**
   * Entry Point
   * Wird ausgeführt, wenn die Seite geöffnet wird
   * => Daten laden, mappen, etc.
   */
  mounted() {
    // Tastatur Event Listener Abbonieren
    //document.addEventListener('keydown', this.handleKeyboardEvents);
    KeyboardObserver.subscribe(this.handleKeyboardEvents);

    // Text in einzelne Zeichen (= Objekte) aufteilen
    this.chars = this.annotationText
        .split('')
        .map((e, i) => {
          const currentAnnotation = this.annotations.find(f => f.start <= i && f.end > i);
          if (currentAnnotation) {
            currentAnnotation.typeIndex = this.annotationTypes.indexOf(currentAnnotation.type);
          }
          return {
            char: e,
            charIndex: i,
            annotation: currentAnnotation,
            annotationIndex: currentAnnotation ? this.annotations.indexOf(currentAnnotation) : null,
            type: currentAnnotation ? this.annotationTypes.indexOf(currentAnnotation.type) : null
          };
        });
  }
}
</script>
