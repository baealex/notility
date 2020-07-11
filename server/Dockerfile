FROM python:3.8

COPY ./app/requirements.txt /app/
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY ./app /app

ENTRYPOINT ["uwsgi"]
CMD ["--socket", ":5000", "--module", "wsgi", "--enable-threads", "-b", "32768"]