FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y python3-pip python3-matplotlib
RUN pip3 install requests \
                 beautifulsoup4 \
                 pymongo \
                 flask \
                 plotly \
                 packaging
WORKDIR /home/radwan
