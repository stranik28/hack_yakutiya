FROM rasa/rasa:3.5.6-full

WORKDIR /app
COPY . /app

USER root
COPY ./data /app/data

#RUN  rasa train

VOLUME /app
VOLUME /app/data
VOLUME /app/models

CMD ["run","-m","/app/models/","--debug","--endpoints", "endpoints.yml", "--log-file", "out.log","--enable-api"]
