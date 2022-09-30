<template>
  <main>
    <h1>Corpora List</h1>
    <div v-if="corpora.length">
      <p v-for="corpus in corpora"><router-link :to="`/corpora/${corpus}`">» {{corpus}}</router-link></p>
    </div>
    <p v-if="error" class="error">{{error}}</p>
  </main>
</template>

<style>
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
      error: null
    }
  },
  mounted() {
    DocumentService.getCorpora().then((data) => {
      if (data.status_code === 200) {
        this.corpora = data.content.corpora;
      } else {
        this.error = data.message;
      }
    });
  }
}
</script>
