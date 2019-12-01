FROM consol/ubuntu-xfce-vnc

WORKDIR /headless
USER root

ENV WINEDLLOVERRIDES="mscoree,mshtml="
ENV WINEDEBUG=-all 

RUN \
apt-get update --fix-missing &&\
apt-get install -y wget &&\
apt-get install -y curl &&\
wget -nc https://dl.winehq.org/wine-builds/winehq.key &&\
apt-get install -y gnupg2 &&\
apt-key add winehq.key &&\
dpkg --add-architecture i386
RUN \
apt-get install -y vim &&\
apt-get install -y software-properties-common &&\
apt-get install -y apt-transport-https &&\
apt-get install -y xdotool
RUN \
apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ xenial main' &&\
apt-get update &&\
apt-get install --install-recommends -y winehq-staging
RUN \
wget https://www.python.org/ftp/python/3.7.4/python-3.7.4.exe &&\
wget https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe
RUN \
apt install -y xvfb
ENV DISPLAY=:1
COPY ./install_mt5.sh /headless/install_mt5.sh
RUN \
nohup bash -c "Xvfb :1 -screen 0 800x600x16 &" &&\
sleep 10 &&\
wine /headless/python-3.7.4.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 &&\
wine pip install MetaTrader5 pandas fastapi uvicorn email-validator &&\
bash /headless/install_mt5.sh

COPY ./pymt5.py /headless/pymt5.py
COPY ./main.py /headless/main.py
COPY ./entrypoint.sh /headless/entrypoint.sh

ENTRYPOINT ["bash", "/headless/entrypoint.sh"]
