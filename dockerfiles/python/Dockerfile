FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

ARG PYTHON_VERSION=3.8

RUN apt-get update && apt-get install -y --no-install-recommends \
  curl \
  git \
  python${PYTHON_VERSION}-venv python${PYTHON_VERSION}-dev python3-setuptools \
  sudo \
  vim \
  wget

#RUN useradd -m -s /bin/bash -G sudo ubuntu \
#    && echo "ubuntu:ubuntu" | chpasswd \
#    && echo "ubuntu ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/init-users \
#    && chmod 0440 /etc/sudoers.d/init-users

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TZ JST-9

RUN curl -kL https://bootstrap.pypa.io/get-pip.py | python${PYTHON_VERSION} \
  && pip3 install --no-cache-dir pytest black \
  && pip3 install --no-cache-dir --upgrade pip setuptools

RUN cd /usr/local/bin \
  && ln -s /usr/bin/python${PYTHON_VERSION} python \
  && apt-get clean \ 
  && rm -fr /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=""

#WORKDIR /home/ubuntu
#USER ubuntu

CMD ["/bin/bash"]

