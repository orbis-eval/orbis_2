# orbis_2
An Extendable Evaluation Pipeline for Named Entity Drill-Down Analysis

The goal of this component is to provide a webservice of the current orbis-eval project, which was based on the local file system.

# REST API
 
# install with docker compose


1. make sure `./.env` file exists like this, with value being the target docker container:
    ```sh
   MONGO_HOST=orbis2_mongo_1
   ```
2. `docker build .`
3. `docker tag <container> orbis2:latest`
4. `docker-compose up`

# use curl

- `curl -X POST -H "Content-Type: application/json" -d @test_corpus.json localhost:63010/createCorpus`
- `curl -X POST -H "Content-Type: application/json" -d @test_document.json localhost:63010/addDocument`
- `curl -X PUT localhost:63010/addDocumentToAnnotationQueue/<<da_id>`