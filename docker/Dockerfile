FROM debian:bullseye

COPY . /buzzer
#COPY ./conf/asound.conf /etc

RUN apt update
RUN apt install -y  python3 python3-pip libasound2-dev alsa-utils
RUN pip3 install simpleaudio
RUN pip3 install requests

CMD python3 buzzer
