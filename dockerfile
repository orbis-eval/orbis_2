FROM python:3.8-slim-buster

RUN mkdir /src

COPY ./src /src
COPY ./scripts /src/scripts
COPY requirements.txt ./
WORKDIR .

ENV MONGO_HOST='localhost'
ENV MONGO_PORT='27017'

RUN pip3 install -r requirements.txt

EXPOSE 63010

ENTRYPOINT ["uvicorn", "src.scripts.app:app", "--host", "0.0.0.0", "--port", "63010"]

