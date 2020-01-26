FROM python:buster

COPY ./requirements.txt /conuhacks5-python/requirements.txt

WORKDIR /conuhacks5-python

RUN pip install -r /conuhacks5-python/requirements.txt

COPY . /conuhacks5-python

ENV FLASK_ENV "development"
ENV FLASK_APP=run.py
ENV GOOGLE_APPLICATION_CREDENTIALS="/conuhacks5-python/credentials.json"

ENTRYPOINT [ "python" ]

CMD [ "run.py" ]

EXPOSE 5000