FROM python:3.10
ENV PYTHONUNBUFFERED=1
RUN mkdir -p /opt/services/uncle_mao_backend
WORKDIR /opt/services/uncle_mao_backend

ADD ./requirements.txt /opt/services/uncle_mao_backend/

RUN apt-get update && \
    apt-get install -y gettext && \
    apt-get clean && \
    pip install -r requirements.txt

ADD ./ /opt/services/uncle_mao_backend/