<script setup>
import AnnotationChar from "./AnnotationChar.vue";
</script>
<template>
  <div id="annotation_container" v-if="chars" @click="click($event)" @dblclick="dblclick($event)">
    <template v-for="char in chars">
      <span :class="[char.char === '\n' ? 'spacer' : '']"
            :data-charindex="char.index"
            :style="getBorders(char.annotations)"
      >
        {{char.char === ' ' || char.char === '\n' ? '&nbsp;' : char.char}}
      </span>
    </template>
<!--    <AnnotationChar v-for="char in chars" :char="char" @clicker="click($event)"></AnnotationChar>-->
  </div>
  <div id="context_menu_new" @click="approveAnnotation()" :class="[ selectedString ? 'active' : '' ]">
    <i class="fa fa-add"></i>
    <span> {{selectedString}}</span>
  </div>
</template>

<style lang="scss">
@import '@/assets/annotationtypes.scss';
</style>

<style scoped>
[data-annotations="1"] {
  box-shadow: 0 1px 0 #ddd, 0 3px 0 #6f6;
}
[data-annotations="1"] {
  box-shadow: 0 1px 0 #ddd, 0 3px 0 #6f6, 0 4px 0 #ddd, 0 6px 0 #6f6;
}
[data-annotations="2"] {
  box-shadow: 0 1px 0 #ddd, 0 3px 0 #6f6, 0 4px 0 #ddd, 0 6px 0 #6f6, 0 7px 0 #ddd, 0 9px 0 #6f6;
  background-color: #9f9;
}

#annotation_container {
  display: flex;
  flex-wrap: wrap;
  font-family: monospace;

}
#context_menu_new {
  display: none;
  position: absolute;
  top: 110px;
  left: 100px;
  padding: .4em 1em;
  background-color: var(--color-background-soft);
  color: var(--color-text);
  border: 1px solid var(--color-text);
  border-radius: .5em;
  transform: translate(-1.5ch, 1.5em);
  cursor: pointer;
}
#context_menu_new::before {
  content: "";
  position: absolute;
  top: -.3em;
  left: 1.5ch;
  width: .5em;
  height: .5em;
  background-color: var(--color-background-soft);
  border-top: 1px solid var(--color-text);
  border-left: 1px solid var(--color-text);
  transform: rotate(45deg);
}
#context_menu_new.active {
  display: block;
}
#context_menu_new span {
  margin-left: 1ch;
}
</style>

<script>

import {KeyboardObserver} from "@/utils/keyboard-event-listener.service";
import {AnnotationService} from "@/services/Annotation.service";
import {AnnotationCharObject} from "@/models/annotation-char";
import {enAnnotationStatus} from "@/models/annotation";

export default {
  data() {
    return {
      chars: [],
      annotations: [],
      newAnnotation: null,
      selectedString: '',
      keyboardObserver: KeyboardObserver,
    };
  },
  methods: {
    /**
     * Initailisierungsmethode
     * @constructor
     */
    InitAnnotationVue() {
      if (this.annotations === AnnotationService.Annotations) {
        return;
      }
      this.annotations = AnnotationService.Annotations;
      // Text in einzelne Zeichen (= Objekte) aufteilen
      console.log('build chars');
      this.chars = AnnotationService.Document
          .split('')
          .map((e, i) => {
            const char = new AnnotationCharObject({ char: e, index: i });
            char.annotations = this.annotations
                .filter(e => [enAnnotationStatus.REPLACED].indexOf(e.status) === -1 && e.start <= i && e.end > i);
            if (char.annotations) {
              char.type = AnnotationService.AnnotationTypes.find(f => f.caption === char.annotation?.type);
            }
            return char;
          });
      setTimeout(() => {
        this.annotations
            .filter(e => [enAnnotationStatus.REPLACED, enAnnotationStatus.PENDING, enAnnotationStatus.PROVISORY].indexOf(e.status) === -1)
            .forEach(e => this.setClassOnChars(e));
        this.selectNextAnnotation(true);
      });
      },
    /**
     * gibt den Style für die Unterstreichungen zurück
     * @param annotations
     * @returns {string|string}
     */
    getBorders(annotations) {
      const borders = annotations.map(this.getAnnotationBorder);
      return borders.length ? `box-shadow: ${borders.join(', ')};` : '';
    },
    /**
     * berechnet die Unterstreichungen
     * @param annotation
     * @param index
     * @returns {string}
     */
    getAnnotationBorder(annotation, index) {
      let type = AnnotationService.GetTypeByCaption(annotation.type);
      if (index !== 0) { annotation.layer = index; }
      return annotation.layer ? `0 ${(annotation.layer * 3) - 2}px 0 var(--color-background), 0 ${(annotation.layer * 3)}px 0 var(--type-color-${type.index})` : `0 -2px 0 var(--type-color-${type.index}) inset`;
    },
    /**
     * Setzt die Unterstreichung für alle selektieren Chars
     */
    setBordersForSelectedElements() {
      document.querySelectorAll('.selected').forEach(e => {
        e.style = this.getBorders(this.annotations.filter(f =>
            f.start <= e.getAttribute('data-charindex')
            && f.end > e.getAttribute('data-charindex')
            && [enAnnotationStatus.PENDING, enAnnotationStatus.PROVISORY, enAnnotationStatus.APPROVED, enAnnotationStatus.EDITED, enAnnotationStatus.NEW].indexOf(f.status) >= 0
        ));
      });
    },
    /**
     * Setzt eine Klasse auf alle Chars (anhand der Annotation)
     * @param annotation
     * @param cssclass
     */
    setClassOnChars(annotation, cssclass = annotation.status) {
      for (let i = annotation.start; i < annotation.end; i++) {
        document.querySelector(`[data-charindex="${i}"]`).className = cssclass;
      }
    },
    /**
     * ganze Annotation wählen bei klick auf einen Char
     * @param event ClickEvent
     */
    click(event) {
      if (event.target.nodeName === 'SPAN') {
        const annotations = this.annotations.filter(f => f.start <= event.target.dataset.charindex && f.end >= event.target.dataset.charindex);
        if (annotations.length > 0) {
          this.unselectAllAnnotationElements();
          this.annotations.filter(f => f.selected).forEach(e => e.selected = false);
          annotations[0].selected = true;
          this.setClassOnChars(annotations[0], 'selected');
        }
      }
    },
    /**
     * Auswahl eines Wortes bei Doppelklick (mit Shift Auswahl mehrerer zusammenhängender Worte)
     * @param event ClickEvent
     */
    dblclick(event) {
      if (event.target.nodeName === 'SPAN') {
        let start = event.target.dataset.charindex, end = start;
        if (event.shiftKey) {
          start = Math.min(document.querySelector('.selected').getAttribute('data-charindex'), start);
          end = Math.max(document.querySelectorAll('.selected')[document.querySelectorAll('.selected').length - 1].getAttribute('data-charindex'), end);
        } else {
          this.unselectAllAnnotationElements();
        }
        const selection = this.trimSelection(AnnotationService.Document, start, end);
        for (let i = selection.start; i < selection.end; i++) {
          document.querySelector(`[data-charindex="${i}"]`).classList.add('selected');
        }
        this.newAnnotation = { surface_form: selection.text, start: selection.start, end: selection.end, status: enAnnotationStatus.PROVISORY, index: Math.max(...this.annotations.map(a => a.index)) + 1, selected: true, created: true };
        this.clearMouseSelection();
      }
    },
    /**
     * Keyborad Events abhandeln
     * @param event Keyboard Event
     */
    handleKeyboardEvents(event) {
      switch (event.code) {
          // case 'Space':
        case 'Enter':
        case 'NumpadEnter':
          this.approveAnnotation();
          break;
        case 'Backspace':
        case 'Delete':
          this.deleteAnnotation();
          break;
        case 'Home':
          this.selectNextAnnotation(false, 0);
          break;
        case 'End':
          this.selectNextAnnotation(false, this.annotations.length - 1);
          break;
        case 'Tab':
          event.preventDefault();
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
        default:
          console.log('key pressed', event.code);
      }
    },
    /**
     * selektiert alle Chars zur aktuellen Annotation
     */
    selectAnnotationElement() {
      const selected = this.annotations.find(e => e.selected);
      if (!selected) {
        return;
      }
      for(let i = selected.start; i < selected.end; i++) {
        document.querySelector(`[data-charindex="${i}"]`).classList.add('selected');
      }
    },
    /**
     * deselektiert alle Annotationen
     */
    unselectAllAnnotationElements() {
      this.annotations.filter(e => e.selected).forEach(e => { this.setClassOnChars(e); });
      document.querySelectorAll('.selected').forEach(e => e.classList.remove('selected'));
    },
    /**
     * setzt die neue Annotation zurück (MouseSelect)
     */
    unsetNewAnnotation() {
      this.unselectAllAnnotationElements();
      this.newAnnotation = null;
    },
    /**
     * deselektiert alle neuen Annotationen
     */
    unselectNewAnnotations() {
      this.closeContextMenuForNewAnnotation();
      document.querySelectorAll('.selected').forEach(e => e.classList.remove('selected'));
      let selected = this.annotations.find(e => e.status === enAnnotationStatus.PROVISORY);
      if (selected) {
        for (let i = selected.start; i < selected.end; i++) {
          this.setAnnotationOnChar(i, null);
        }
        this.annotations.splice(this.annotations.indexOf(selected), 1);
      }
    },
    /**
     * Annotation als «bestätigt» markieren
     */
    approveAnnotation() {
      const selectNextAnnotation = !this.newAnnotation;
      this.closeContextMenuForNewAnnotation();
      let selected = this.newAnnotation ? this.addNewAnnotation() : this.annotations.find(e => e.selected);
      if (!selected) {
        return;
      }
      if (selected.status === enAnnotationStatus.PROVISORY) {
        selected.status = enAnnotationStatus.NEW;
      } else if (selected.status !== enAnnotationStatus.NEW) {
        selected.status = enAnnotationStatus.APPROVED;
      }
      if ([enAnnotationStatus.PROVISORY, enAnnotationStatus.EDITED, enAnnotationStatus.NEW].indexOf(selected.status) >= 0) {
        this.setClassOnChars(selected);
      }
      this.setTimeStamp(selected);
      if (selectNextAnnotation) {
        this.selectNextAnnotation();
      }
    },
    /**
     * Annotation als «gelöscht» markieren
     */
    deleteAnnotation() {
      const selected = this.newAnnotation ?? this.annotations.find(e => e.selected && e.status !== enAnnotationStatus.REPLACED);
      if (!selected) {
        return;
      }
      if (selected === this.newAnnotation) {
        this.newAnnotation = null;
        this.selectNextAnnotation();
        return;
      }
      if (selected.created === true) {
        selected.status = enAnnotationStatus.REPLACED;
        this.setBordersForSelectedElements();
        this.setClassOnChars(selected, 'unset');
        let index = this.annotations.indexOf(selected);
        this.annotations.splice(index, 1);
        this.annotations[index - 1].selected = true;
        this.selectNextAnnotation();
        return;
      }
      if ([enAnnotationStatus.NEW, enAnnotationStatus.PROVISORY].indexOf(selected.status) >= 0) {
        const original = this.annotations.find(e => e.index === selected.index && e.status === enAnnotationStatus.REPLACED);
        original.status = enAnnotationStatus.PENDING;
        original.selected = true;
        selected.status = enAnnotationStatus.REPLACED;
        this.setBordersForSelectedElements();
        this.setClassOnChars(selected, 'unset');
        this.setClassOnChars(original, 'selected');
        this.setBordersForSelectedElements();
        this.annotations.splice(this.annotations.indexOf(selected), 1);
      } else {
        selected.status = enAnnotationStatus.DELETED;
        this.setClassOnChars(selected);
        this.selectNextAnnotation();
      }
    },
    /**
     * fügt die per Maus hinzugefügte Annotation zur Liste hinzu
     * @returns {null}
     */
    addNewAnnotation() {
      const selected = Object.assign({}, this.newAnnotation);
      const prevAnnotations = this.annotations.filter(f => f.start < selected.start);
      prevAnnotations.sort((a, b) => a.start > b.start ? 1 : -1);
      this.annotations.splice(this.annotations.indexOf(prevAnnotations[prevAnnotations.length - 1]) + 1, 0, selected);
      this.newAnnotation = null;
      return selected;
    },
    /**
     * Annotation anpassen (erweitern/reduzieren)
     * @param dir Richtung
     * @param amount Anzahl (+1 / -1)
     */
    editAnnotation(dir, amount = 1) {
      let selected = this.newAnnotation ?? this.annotations.find(e => e.selected
          && [enAnnotationStatus.PENDING, enAnnotationStatus.PROVISORY, enAnnotationStatus.APPROVED, enAnnotationStatus.EDITED, enAnnotationStatus.NEW].indexOf(e.status) >= 0);
      if (!selected) {
        return;
      }
      if ([enAnnotationStatus.PENDING, enAnnotationStatus.APPROVED, enAnnotationStatus.EDITED].indexOf(selected.status) >= 0) {
        const newSelected = Object.assign({}, selected, { status: enAnnotationStatus.PROVISORY });
        selected.status = enAnnotationStatus.REPLACED;
        selected.selected = false;
        this.annotations.splice(this.annotations.indexOf(selected), 0, newSelected);
        selected = newSelected;
      } else if (selected.status === enAnnotationStatus.NEW) {
        selected.status = enAnnotationStatus.PROVISORY;
      }

      const indexes = [];
      document.querySelectorAll('.selected').forEach(e => indexes.push(+e.getAttribute('data-charindex')));
      let index = dir === 'start' ? Math.min(...indexes) : Math.max(...indexes);
      if (amount > 0) {
        let element = document.querySelector(`[data-charindex="${index + amount * (dir === 'start' ? -1 : 1)}"]`);
        element.classList.add('selected');
        if (dir === 'start') {
          selected.start--;
        } else {
          selected.end++;
        }
      } else {
        let element = document.querySelector(`[data-charindex="${index}"]`);
        element.classList.remove('selected');
        element.style.boxShadow = '';
        if (dir === 'start') {
          selected.start++;
        } else {
          selected.end--;
        }
      }

      this.setBordersForSelectedElements();
    },
    /**
     * Einem Char-Objekt eine Annotation (oder null) zuweisen (bei ändern/erweitern/reduzieren der Annotation)
     * @param charIndex Index
     * @param annotation Annotation
     */
    setAnnotationOnChar(charIndex, annotation) {
      const char = this.chars.find(e => e.index === charIndex);
      char.annotation = annotation;
      char.type = AnnotationService.GetTypeByAnnotation(annotation);
      const charElement = document.querySelector(`[data-charindex="${charIndex}"]`);
      if (annotation) {
        charElement.classList.add('marked', 'selected', 'edited', `type_${char.type.index}`);
        charElement.setAttribute('data-annotationindex', annotation.index);
      } else {
        charElement.className = '';
        charElement.removeAttribute('data-annotationindex');
      }
    },
    /**
     * ersetzt die bestehende selektierte Annotation
     * @param selected selektierte Annotation
     */
    replaceAnnotation(selected) {
      if (!selected) {
        return;
      }
      if ([enAnnotationStatus.NEW, enAnnotationStatus.EDITED, enAnnotationStatus.PROVISORY].indexOf(selected.status) === -1) {
        const newSelected = Object.assign({}, selected);
        newSelected.status = enAnnotationStatus.REPLACED;
        newSelected.selected = false;
        selected.status = enAnnotationStatus.EDITED;
        selected.selected = true;
        this.annotations.splice(this.annotations.indexOf(selected), 0, newSelected);
      }
    },
    /**
     * setzt einen neuen AnnotationType und springt weiter
     * @param key Tastaturtaste
     */
    setAnnotationType(key) {
      const selectNextAnnotation = !this.newAnnotation;
      const selected = this.newAnnotation ? this.addNewAnnotation() : this.annotations.find(e => e.selected);
      if (!selected) {
        return;
      }
      const type = AnnotationService.GetTypeByKey(key);
      if (!type) {
        return;
      }
      this.replaceAnnotation(selected);
      if ([enAnnotationStatus.NEW].indexOf(selected.status) === -1) {
        selected.status = enAnnotationStatus.EDITED;
      }

      selected.type = type.caption;
      this.setTimeStamp(selected);

      this.setBordersForSelectedElements();
      if (selectNextAnnotation) {
        this.selectNextAnnotation();
      }
    },
    /**
     * nächste Annotation auswählen
     * @param back zurück zur vorherigen, statt zur nächsten
     */
    selectNextAnnotation(back = false, specificindex = null) {
      this.unsetNewAnnotation();
      let index = 0;
      const activeAnnotations = this.annotations.filter(e => e.status !== enAnnotationStatus.REPLACED);
      const selected = activeAnnotations.find(e => e.selected);
      if (selected) {
        index = activeAnnotations.indexOf(selected) + (back ? -1 : 1);
        selected.selected = false;
      }
      if (specificindex) {
        index = specificindex;
      }
      if (index < 0) {
        index = 0;
      }
      if (index < activeAnnotations.length) {
        let newSelected = activeAnnotations[index];
        newSelected.selected = true;
        this.setClassOnChars(newSelected, 'selected');

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
     * sucht im Text ganze Wörter heraus
     * @param input Text
     * @param start StartIndex
     * @param end EndIndex
     * @returns {{start, end, text}} neue Werte
     */
    trimSelection(input, start, end) {
      while (/[^a-z0-9äöüàéèÇ(]/i.test(input[start])) { start++; }
      while (/[a-z0-9äöüàéèÇ(]/i.test(input[start - 1]) && start > 0) { start--; }
      while (/[a-z0-9äöüàéèÇ)]/i.test(input[end]) && end <= input.length) { end++; }
      return { text: input.slice(start, end), start, end };
    },
    /**
     * Setzt einen Zeitstempel
     * @param annotation Annotation
     */
    setTimeStamp(annotation) {
      if (!annotation.meta) {
        annotation.meta = {};
      }
      annotation.meta.approved = new Date();
    },
    /**
     * Mouse-Selektion behandeln
     */
    mouseUpHandling() {
      const selection = window.getSelection();
      if (!selection) { return; }

      let start = Math.min(...[
        selection.anchorNode?.parentNode?.dataset?.charindex,
        selection.baseNode?.parentNode?.dataset?.charindex,
        selection.anchorNode?.dataset?.charindex,
        selection.baseNode?.dataset?.charindex,
      ].filter(e => !!e).map(e => parseInt(e)));
      let end = Math.max(...[
        selection.extentNode?.parentNode?.dataset?.charindex,
        selection.focusNode?.parentNode?.dataset?.charindex,
        selection.extentNode?.dataset?.charindex,
        selection.focusNode?.dataset?.charindex,
      ].filter(e => !!e).map(e => parseInt(e)));
      if (start === end || start === Infinity) {
        this.closeContextMenuForNewAnnotation();
        this.clearMouseSelection();
        return;
      }
      this.unselectAllAnnotationElements();
      const selected = this.annotations.find(e => e.selected);
      if (selected) {
        selected.selected = false;
      }

      end++;
      while (this.chars[start].char === ' ') { start++; }
      while (this.chars[end - 1].char === ' ') { end--; }
      for(let i = start; i < end; i++) {
        document.querySelector(`[data-charindex="${i}"`).classList.add('selected');
      }

      this.newAnnotation = {
        surface_form: AnnotationService.Document.substring(start, end),
        start: start,
        end: end,
        status: enAnnotationStatus.PROVISORY,
        index: Math.max(...this.annotations.map(a => a.index)) + 1,
        selected: true,
        created: true
      };

      this.clearMouseSelection();
    },
    clearMouseSelection()
    {
      if (window.getSelection) {window.getSelection().removeAllRanges();}
      else if (document.selection) {document.selection.empty();}
    },
    /**
     * Kontextmenü für neue Annotation öffnen
     * @param start StartIndex des Characters
     */
    openContextMenuForNewAnnotation(start) {
      let popover = document.getElementById('context_menu_new');
      let firstchar = document.querySelector(`span[data-charindex="${start}"]`);
      popover.style.top = firstchar.offsetTop + 'px';
      popover.style.left = firstchar.offsetLeft + 'px';
    },
    /**
     * Kontextmenü für neue Annotation schliessen
     */
    closeContextMenuForNewAnnotation() {
      this.selectedString = null;
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

    // MouseEvent Abbonieren
    document.getElementById('annotation_container').onmouseup = this.mouseUpHandling;

    this.InitAnnotationVue();
    AnnotationService.Changes.subscribe(() => {
      this.InitAnnotationVue();
    });
  }
}
</script>
