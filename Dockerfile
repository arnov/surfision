FROM python:3.6.9-slim
RUN apt-get update
RUN apt-get install -y python3-dev python3-virtualenv \
       git curl wget httpie htop gcc gfortran build-essential \
       ffmpeg

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
RUN mkdir data
COPY . .

RUN pip3 install -r requirements.txt
CMD python get_data.py
