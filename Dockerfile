FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow

RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get install -y \
    hping3 \
    build-essential \
    git  \
    hydra \
    tcpdump \
    && apt install -y \
    python3.10 \
    python3-pip

WORKDIR /opt/app

RUN pip install \
    --pre scapy[basic] \
    scapy

COPY . .

CMD ["python3", "main.py"]