FROM ubuntu:22.04

RUN apt update --fix-missing && \
    apt -y install python3.10 python3.10-venv python3-pip \
    binutils git wget \
    unzip texlive-latex-base graphviz nano vim \
    libgtk2.0-0 libgtk-3-0 libxss1 libasound2 plantuml && \
    apt -y install sudo && \
    mkdir -p /repo && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

RUN apt-get install python3-pip && \
    apt-get clean && \
    apt-get autoremove --yes

WORKDIR /home/dev

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt && \
    rm requirements.txt

RUN printf "\n\nADDING USER user TO SUDOERS - DEV ENV ONLY!\n\n" >&2 && \
    groupadd user -g 1000; \
    useradd -m -s /bin/bash -N -u 1000 user -g 1000 && \
    echo "user:user" | chpasswd && \
    echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

WORKDIR /repo