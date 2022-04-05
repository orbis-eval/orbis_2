FROM python:3.8-slim-buster

# TODO: configure host and port via helm values?
ENV MONGO_HOST=localhost
ENV MONGO_PORT=27017

RUN apt-get update
RUN apt-get install curl -y
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash
RUN apt-get install nodejs -y
RUN node -v
RUN npm -v

RUN mkdir -p /app /src

COPY ./src /app/src
COPY ./scripts /app/src/scripts
COPY requirements.txt /app/
RUN ls -la
WORKDIR /app/src/frontend
RUN npm install
RUN npm run build

WORKDIR /app
RUN pwd
RUN mv ./src/frontend/dist/* .

RUN pip3 install -r requirements.txt

EXPOSE 63010

ENTRYPOINT ["uvicorn", "src.scripts.app:app", "--host", "0.0.0.0", "--port", "63010"]

