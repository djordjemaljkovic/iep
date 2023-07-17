FROM python:3

RUN mkdir -p /opt/src/store
WORKDIR /opt/src/store

COPY ./application/buyer/application.py ./application.py
COPY ./application/buyer/config.py ./config.py
COPY ./application/buyer/models.py ./models.py
COPY ./application/buyer/decorater.py ./decorater.py
COPY ./application/buyer/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./application.py"]