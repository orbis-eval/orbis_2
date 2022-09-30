<template>
  <main>
    <h1>Documents</h1>
    <p><router-link to="/corpora">« zurück zur Übersicht</router-link></p>
    <p>Corpus: {{$route.params.corpus_name}}</p>
    <p v-if="message" class="msg">{{message}}</p>
      <div class="grid">
        <span>Document ID</span>
        <span>Annotator</span>
        <span>Last Edit</span>
      </div>
      <router-link v-for="corpus of corpora"
                   class="grid"
                   :to="`/documents/${$route.params.corpus_name}/${corpus.da_id}`">
        <span>{{corpus.d_id}}</span>
        <span>{{corpus.annotator}}</span>
        <span>{{corpus.last_edited}}</span>
      </router-link>
    <p v-if="error" class="error">{{error}}</p>
  </main>
</template>

<style>
p {
  margin-bottom: 1em;
}
.msg {
  color: blue;
  border: 1px solid blue;
  padding: 1em;
  background-color: rgba(0,0,255,0.2);
}
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  cursor: pointer;
}
.grid:nth-of-type(2n) {
  background-color: rgba(0,0,0,0.05);
}
.grid:hover {
  background-color: rgba(0,0,0,0.1);
}
.error {
  color: red;
  border: 1px solid red;
  padding: 1em;
  background-color: rgba(255,0,0,0.2);
}
</style>

<script>
import { DocumentService } from "@/services/Document.service";

export default {
  data() {
    return {
      corpora: [],
      message: null,
      error: null
    }
  },
  mounted() {
    DocumentService.getDocuments(this.$route.params.corpus_name).then((data) => {
      if (data.status_code === 200) {
        this.message = data.message;
        this.corpora = data.content.corpora
            .sort((a, b) => a.d_id > b.d_id ? 1 : -1)
            .sort((a, b) => a.last_edit > b.last_edit ? 1 : -1);
      } else {
        this.error = data.message;
      }
    });
  }
}
</script>
