FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y python3-pip python3-matplotlib
RUN pip3 install requests \
                 beautifulsoup4 \
                 pymongo \
                 flask \
                 plotly \
                 packaging \
                 selenium
RUN pip3 install -U pip setuptools
RUN apt-get install -y locales \
    && echo "en_US UTF-8" > /etc/locale.gen \
    && locale-gen en_US.UTF-8 \
    && export LANG=en_US.UTF-8 \
    && export LANGUAGE=en_US:en \
    && export LC_ALL=en_US.UTF-8 \
    && pip3 install streamlit pandas

RUN apt install -y wget && wget -q -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome.deb \
    && rm google-chrome.deb

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
WORKDIR /home/radwan
