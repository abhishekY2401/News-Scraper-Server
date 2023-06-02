FROM python:3.9
COPY . /app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
COPY . .
ENV PORT 5000
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "summarize.py" ]