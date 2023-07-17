FROM python:3

RUN mkdir -p /opt/src/store
WORKDIR /opt/src/store

COPY ./application/daemon/application.py ./application.py
COPY ./application/daemon/config.py ./config.py
COPY ./application/daemon/models.py ./models.py
COPY ./application/daemon/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./application.py"]