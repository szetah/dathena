FROM python:3.6.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
ADD requirements.txt /src/
RUN pip install -r /src/requirements.txt
ADD . /src/
RUN adduser --disabled-password --gecos '' myuser
