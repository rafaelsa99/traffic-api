FROM python:3.7

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin libblas-dev libatlas-base-dev

RUN apt-get install -y python3-dev gcc libc-dev libffi-dev libzbar-dev

# Install GDAL dependencies
RUN apt-get install -y libgdal-dev g++ --no-install-recommends && \
    apt-get clean -y

ENV PYTHONUNBUFFERED=1

WORKDIR /django

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
