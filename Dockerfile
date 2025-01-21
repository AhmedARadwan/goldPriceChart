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

RUN apt install -y wget && wget -q -O google-chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_123.0.6312.86-1_amd64.deb \
    && apt-get install -y ./google-chrome.deb \
    && rm google-chrome.deb

RUN apt install -y unzip && wget -q -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && cp /usr/local/bin/chromedriver-linux64/chromedriver /usr/bin/

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
WORKDIR /home/radwan
