<template>
  <main>
    <h1>Documents</h1>
    <p><router-link to="/corpora">« zurück zur Übersicht</router-link></p>
    <p>Corpus: {{$route.params.corpus_name}}</p>
    <p v-if="message" class="msg">{{message}}</p>
    <div class="flex">
      <div v-for="g of corporaGroups" class="document">
        <div class="wrapper">
          <div class="d_id">{{g.d_id}}</div>
          <div class="last_edited">{{g.last_edited}}</div>
          <div class="annotation">
            <router-link v-for="c of g.corpora"
                         :to="`/documents/${$route.params.corpus_name}/${c.da_id}`"
                         :title="c.da_id"
            >
              <span>» {{c.da_id.substring(0, 3)}}...{{c.da_id.substring(21)}}</span>
              <span class="annotator">{{c.annotator}}</span>
              <span>{{c.last_edited}}</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
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
.flex {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 8px;
}
.document {
  border: 1px solid #999;
  padding: 5px;
}
.document:hover {
  box-shadow: 0 0 0 4px #999;
}
.document .wrapper {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
.d_id, .last_edited {
  padding: 0 4px;
}
.annotation {
  width: 100%;
}
.annotation a {
  display: flex;
  gap: 1em;
  margin: 2px;
  padding: 2px;
  background-color: rgba(0,0,0,0.05);
  font-size: .9em;
}
.annotation a:hover {
  background-color: rgba(0,0,0,0.15);
}
.dark-mode .annotation a {
  background-color: rgba(255,255,255,0.15);
}
.dark-mode .annotation a:hover {
  background-color: rgba(255,255,255,0.25);
}
.annotator {
  flex-grow: 1;
  font-weight: 700;
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
import {LoadingSpinnerService} from "@/services/LoadingSpinner.service";

export default {
  data() {
    return {
      corpora: [],
      corporaGroups: [],
      message: null,
      error: null
    }
  },
  mounted() {
    const loadingSpinnerID = LoadingSpinnerService.Show();
    DocumentService.getDocuments(this.$route.params.corpus_name).then((data) => {
      if (data.status_code === 200) {
        this.message = data.message;
        this.corpora = data.content.corpora
            .sort((a, b) => a.d_id > b.d_id ? 1 : -1)
            .sort((a, b) => a.last_edit > b.last_edit ? 1 : -1);
        this.corporaGroups = this.corpora
            .filter((e, i, a) => a.indexOf(a.find(f => f.d_id === e.d_id)) === i)
            .map(e => ({
              d_id: e.d_id,
              last_edited: e.last_edited,
              corpora: this.corpora.filter(f => f.d_id === e.d_id)
            }));
      } else {
        this.error = data.message;
      }
      LoadingSpinnerService.Close(loadingSpinnerID);
    }).catch(() => {
      LoadingSpinnerService.Close(loadingSpinnerID);
    });
  }
}
</script>
