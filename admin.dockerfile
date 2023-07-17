FROM python:3

RUN mkdir -p /opt/src/store
WORKDIR /opt/src/store

COPY ./application/admin/application.py ./application.py
COPY ./application/admin/config.py ./config.py
COPY ./application/admin/decorater.py ./decorater.py
COPY ./application/admin/models.py ./models.py
COPY ./application/admin/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./application.py"]