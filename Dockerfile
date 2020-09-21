FROM alkalineml/pmdarima:latest
# Reference for setting up Orca: https://hub.docker.com/r/cpsievert/plotly-orca/dockerfile

# Need this to add repo
RUN apt-get update && apt-get install -y software-properties-common
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 0x51716619e084dab9

# Install basic stuff and R
RUN apt-get update && apt-get install -y \
    sudo \
    git \
    wget \
    fonts-texgyre \
    texinfo \
    locales \
    libcurl4-gnutls-dev \
    libcairo2-dev \
    libxt-dev \
    libssl-dev \
    libxml2-dev 

# Update charset
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
   && locale-gen en_US.utf8 \
   && /usr/sbin/update-locale LANG=en_US.UTF-8
ENV LANG=en_US.UTF-8

# Install code-server
RUN curl -fOL https://github.com/cdr/code-server/releases/download/v3.5.0/code-server_3.5.0_amd64.deb
RUN dpkg -i code-server_3.5.0_amd64.deb
# RUN systemctl enable --now code-server@$USER

# Install sf system dependencies
# RUN add-apt-repository ppa:ubuntugis/ppa --yes
RUN apt-get -y update
RUN apt-get install -y libudunits2-dev libproj-dev libgeos-dev libgdal-dev

# Install packages
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Install system dependencies related to running orca
RUN apt-get install -y \
    libgtk2.0-0 \ 
    libgconf-2-4 \
    xvfb \
    fuse \
    desktop-file-utils

# Install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable

# Install orca
RUN wget https://github.com/plotly/orca/releases/download/v1.1.1/orca-1.1.1-x86_64.AppImage -P /home
RUN chmod 777 /home/orca-1.1.1-x86_64.AppImage 
RUN cd /home && /home/orca-1.1.1-x86_64.AppImage --appimage-extract
RUN printf '#!/bin/bash \nxvfb-run --auto-servernum --server-args "-screen 0 640x480x24" /home/squashfs-root/app/orca "$@"' > /usr/bin/orca
RUN chmod 777 /usr/bin/orca

EXPOSE 8989

CMD ["code-server", "--auth", "none", "--bind-addr", "0.0.0.0:8989"]
