FROM python:3.9-slim-buster

WORKDIR /app

COPY ./requirements.txt /app

# Install NLTK and download data
RUN pip install nltk
RUN python -m nltk.downloader punkt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host", "0.0.0.0"]