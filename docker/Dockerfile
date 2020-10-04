FROM debian:latest

COPY . /buzzer
COPY ./conf/asound.conf /etc

RUN apt update
RUN apt install -y git python3 python3-pip libasound2-dev python3-tk alsa-utils
RUN pip3 install simpleaudio
RUN pip3 install requests

CMD /bin/bash
