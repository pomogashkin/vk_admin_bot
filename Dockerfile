FROM python:3.9.10

ENV ALBUM_ID=123123
ENV GROUP=123123
ENV ME=123123
ENV LOGIN=123123
ENV PASSWORD=123123
ENV URL=https://random-word-api.herokuapp.com/word

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /code/

CMD ["python", "main.py"]