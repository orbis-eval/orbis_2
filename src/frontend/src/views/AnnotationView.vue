<script setup>
import sampleData from '../assets/sample.json';
import Annotation from '../components/Annotation.vue'
import AnnotationTypeList from '../components/AnnotationTypeList.vue'
</script>

<template>
  <aside>
    <AnnotationTypeList :annotation-types="annotationTypes" @clicker="click($event)"></AnnotationTypeList>
  </aside>
  <main>
    <Annotation
        :annotation-text="annotationText"
        :annotation-types="annotationTypes"
        :annotations="annotations"
        v-if="annotations.length" />
  </main>
</template>

<script>
import {enAnnotationStatus} from "@/models/enAnnotationStatus";

export default {
  data() {
    return {
      sourceDocument: {},
      annotationText: '',
      annotations: [],
      annotationTypes: [],
    }
  },
  methods: {
    click(event) {
      console.log(event, this.annotations);
    }
  },
  mounted() {
    //todo: load data from server
    fetch('/getDocumentForAnnotation')
        // .then(response => response.json())
        .then(data => {
          console.log(data);
        });
    // this.annotationText = 'Hallo Welt';
    this.sourceDocument = sampleData;
    this.annotationText = sampleData.text;
    this.annotations = []
        .concat(sampleData.gold_standard_annotation.certificates)
        .concat(sampleData.gold_standard_annotation.course_contents)
        .concat(sampleData.gold_standard_annotation.target_groups)
        .concat(sampleData.gold_standard_annotation.unknown)
        .sort((a, b) => a.start > b.start ? 1 : -1);
    this.annotations.forEach(e => e.status = enAnnotationStatus.pending);

    // Annotationstypen extrahieren
    this.annotationTypes = this.annotations
        .map(e => e.type)
        .filter((e, i, a) => a.indexOf(e) === i);
    // this.annotationTypes = this.annotationTypes.concat(this.annotationTypes);
  }
}
</script>
