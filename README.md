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

or (2. & 3. together) `docker build -t orbis2:latest .`

4. `docker-compose up`

or (2. - 4. together) `docker build -t orbis2:latest . && docker-compose up` 

# use curl

- `curl -X POST -H "Content-Type: application/json" -d @test_corpus.json localhost:63010/createCorpus`
- `curl -X POST -H "Content-Type: application/json" -d @test_document.json localhost:63010/addDocument`
- `curl -X PUT localhost:63010/addDocumentToAnnotationQueue/<<da_id>`

## Endpoints

https://gitlab.semanticlab.net/fhgr/future-of-work/orbis_2_webservice/-/blob/main/openapi.json


## Tests

In order to run static code checks or test locally, ensure having installed tox locally. You can do so by:

`pip install tox`
`pip install tox-pip-version`

Static code checks:

`tox -e pep8`

Tests (esnure, that a local mongodb is running on port 27017):

`tox -e coverage`

