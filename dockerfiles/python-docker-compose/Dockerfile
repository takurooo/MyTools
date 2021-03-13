FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
  curl \
  git \
  python3.8-venv python3.8-dev python3-setuptools \
  sudo \
  vim \
  wget

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TZ JST-9

RUN cd /opt && wget https://bootstrap.pypa.io/get-pip.py \ 
  && python3.8 get-pip.py \
  && rm get-pip.py \
  && pip3 install --no-cache-dir pytest black \
  && pip3 install --no-cache-dir --upgrade pip setuptools


RUN cd /usr/local/bin \
  && ln -s /usr/bin/python3.8 python \
  && apt-get clean \ 
  && rm -fr /var/lib/apt/lists/*


CMD ["/bin/bash"]
