<script setup>
import AnnotationTypeList from '../components/AnnotationTypeList.vue'
</script>

<template>
  <aside>
    <AnnotationTypeList></AnnotationTypeList>
  </aside>
  <main>
    <h1>Documents</h1>
    <p><router-link :to="`/corpora/${$route.params.corpus_name}`">« zurück zur Dokument-Auswahl</router-link></p>
    <p>Corpus: {{$route.params.corpus_name}} / Document: {{$route.params.da_id}}</p>
    <p v-if="error" class="error">{{error}}</p>
    <hr>
    <div id="annotation_container" v-if="chars"></div>

  </main>
</template>

<style>
p {
  margin-bottom: 1em;
}
aside h2:not(.types),
aside ul:not(.types),
aside ul li.addtype {
  display: none;
}
#annotation_container {
  display: flex;
  flex-wrap: wrap;
  font-family: monospace;

}
.error {
  color: red;
  border: 1px solid red;
  padding: 1em;
  background-color: rgba(255,0,0,0.2);
}
</style>

<script>
import {AnnotationCharObject} from "@/models/annotation-char";
import {AnnotationService} from "@/services/Annotation.service";

export default {
  data() {
    return {
      corpora: [],
      message: null,
      error: null,
      annotations: [],
      chars: []
    }
  },
  methods: {
    Init() {
      this.chars = AnnotationService.Document
          .split('')
          .map((e, i) => {
            const char = new AnnotationCharObject({ char: e, index: i });
            char.annotations = this.annotations;
            if (char.annotations) {
              char.type = AnnotationService.AnnotationTypes.find(f => f.caption === char.annotation?.type);
            }
            return char;
          });
      setTimeout(() => {
        this.renderChars();
        this.annotations.forEach(e => this.setClassOnChars(e));
        AnnotationService.HideLoadingSpinner();
      });
    },
    /**
     * Setzt eine KlassenListe auf alle Chars
     * @param start
     * @param end
     * @param className
     */
    setClassNameOnChars(start, end, className = '') {
      for (let i = start; i < end; i++) {
        const el = document.querySelector(`[data-charindex="${i}"]`);
        const spacer = el.classList.contains('spacer');
        el.className = className;
        if (spacer) {
          el.classList.add('spacer');
        }
        this.getBordersByIndex(i);
      }
    },
    /**
     * Setzt eine Klasse auf alle Chars (anhand der Annotation)
     * @param annotation
     * @param cssclass
     */
    setClassOnChars(annotation, cssclass = annotation.status) {
      this.setClassNameOnChars(
          annotation.start,
          annotation.end,
          [cssclass, annotation.status]
              .filter((e,i,a) => a.indexOf(e) === i)
              .join(' ')
      );
    },
    /**
     * gibt den Style für die Unterstreichungen zurück
     * @param index
     * @returns {string|string}
     */
    getBordersByIndex(index) {
      const annotations = this.annotations.filter(f =>
          f.start <= index
          && f.end > index
      );
      return this.getBorders(annotations);
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
      if (!annotation.type) {
        return '';
      }
      let type = AnnotationService.GetTypeByCaption(annotation.type);
      if (index !== 0) { annotation.layer = index; }
      return annotation.layer ? `0 ${(annotation.layer * 3) - 2}px 0 var(--color-background), 0 ${(annotation.layer * 3)}px 0 var(--type-color-${type.index})` : `0 -2px 0 var(--type-color-${type.index}) inset`;
    },
    /**
     * Rendert die Character nach dem neu laden des Dokuments
     */
    renderChars() {
      const annotationContainer = document.getElementById('annotation_container');

      this.chars.forEach((c) => {
        const span = document.createElement('span');
        if (c.char === '\n') {
          span.classList.add('spacer');
        }
        span.dataset.charindex = c.index;
        span.style = this.getBordersByIndex(c.index);
        span.innerHTML = c.char === ' ' || c.char === '\n' ? '&nbsp;' : c.char;
        annotationContainer.append(span);
      });
    }
  },
  mounted() {
    AnnotationService.GetDocumentForViewOnly(this.$route.params.da_id).then(() => {
      this.annotations = AnnotationService.Annotations;
      this.Init();
    });
  }
}
</script>
