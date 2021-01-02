FROM python:3.8.7-buster

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN python -m nltk.downloader stopwords

CMD ["python", "manage.py", "run" ]