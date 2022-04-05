<script setup>
import Annotation from '../components/Annotation.vue'
import AnnotationTypeList from '../components/AnnotationTypeList.vue'
</script>

<template>
  <aside>
    <AnnotationTypeList
        :annotation-types="annotationTypes"
        @clicker="click($event)"
    ></AnnotationTypeList>
  </aside>
  <main>
    <Annotation
        v-if="annotations.length"
    />
  </main>
</template>

<script>
import {AnnotationService} from "@/services/Annotation.service";
import {enAnnotationStatus} from "@/models/annotation";

export default {
  data() {
    return {
      annotations: [],
      annotationTypes: [],
    }
  },
  methods: {
    click(event) {
      if (event === 'send') {
        let request = {
          annotator: '',
          DA_id: '',
          data: {
            d_id: 'abc',
            meta: {},
            annotations: AnnotationService.Annotations
                .filter(e => [enAnnotationStatus.NEW, enAnnotationStatus.EDITED, enAnnotationStatus.APPROVED].indexOf(e.status) >= 0)
                .map(e => {
                  e.surface_form = AnnotationService.Document.substring(e.start, e.end);
                  e.scope = 'entity';
                  e.meta = {};
                  return e;
                })
          }
        };
        console.log(event, request);
        // fetch('/saveDocumentAnnotations', {
        //   method: 'POST',
        //   headers: ["Content-Type", "application/json"],
        //   body: JSON.stringify(request)
        // })
        //     .then(response => {
        //       console.log(response);
        //       return response.json();
        //     })
        //     .then(data => {
        //       console.log(data);
        //     });
      }
    }
  },
  mounted() {
    this.annotations = AnnotationService.Annotations;
    this.annotationTypes = AnnotationService.AnnotationTypes;
    if (!AnnotationService.Document) {
      AnnotationService.GetDocumentForAnnotation().then(data => {
        // console.log(data);
        this.annotations = AnnotationService.Annotations;
        this.annotationTypes = AnnotationService.AnnotationTypes;
      });
    }
  }
}
</script>
