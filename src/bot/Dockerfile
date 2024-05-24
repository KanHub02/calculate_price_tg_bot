FROM python:3.10

RUN mkdir -p /opt/services/uncle_mao_bot
WORKDIR /opt/services/uncle_mao_bot

ADD ./requirements.txt /opt/services/uncle_mao_bot/

RUN apt-get update && \
    apt-get install -y gettext && \
    apt-get clean && \
    pip install -r requirements.txt

ADD ./ /opt/services/uncle_mao_bot/

CMD ["python", "main_2.py"]