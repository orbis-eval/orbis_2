<script setup>
import {AnnotationService} from "../services/Annotation.service";
</script>

<template>
  <h2 v-locale="'documentlegend-title'"></h2>
  <ul>
    <li class="marked type_x click" @click="save()"><span v-locale="'documentlegend-save'"></span></li>
    <li class="marked type_x click" @click="save(true)" v-locale="'documentlegend-savenext'"></li>
  </ul>
</template>

<script>
export default {
  name: "AnnotationControls",
  data() {
    return {}
  },
  methods: {
    save(next = false) {
      AnnotationService.SaveDocumentAnnotations(next);
    }
  }
}
</script>

<style scoped>
h2 {
  cursor: pointer;
}

h2, ul {
  padding: 0 .5em 0;
}

li.marked {
  padding: .2em;
  list-style: none;
  user-select: none;
  user-focus: none;
  box-shadow: none;
  background-color: var(--color-success);
  border-bottom: 1px solid var(--color-border);
  color: var(--vt-c-text-light-1);
}

li.marked:hover {
  opacity: 0.8;
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
