FROM python:3.10.12
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY src/ /code/
COPY scripts/runserver.sh /code/
COPY config/ /code/config/
RUN chmod +x ./runserver.sh
EXPOSE 8000