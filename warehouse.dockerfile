FROM python:3

RUN mkdir -p /opt/src/store
WORKDIR /opt/src/store

COPY ./application/warehouse/application.py ./application.py
COPY ./application/warehouse/config.py ./config.py
COPY ./application/warehouse/decorater.py ./decorater.py
COPY ./application/warehouse/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./application.py"]