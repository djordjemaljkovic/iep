FROM python:3

RUN mkdir -p /opt/src/authentication
WORKDIR /opt/src/authentication

COPY ./authentication/application.py ./application.py
COPY ./authentication/admin.py ./admin.py
COPY ./authentication/registrationCheck.py ./registrationCheck.py
COPY ./authentication/decorater.py ./decorater.py
COPY ./authentication/config.py ./config.py
COPY ./authentication/models.py ./models.py
COPY ./authentication/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./application.py"]