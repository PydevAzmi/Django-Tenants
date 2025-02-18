# Strat Docker : Python + Kernal
FROM python:3.13-slim-bullseye

# ENV: Show Logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create Project Folder 
WORKDIR /code

# install mysql dependencies
RUN apt-get update
RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

# Copy Requirements
COPY requirements.txt /code/requirements.txt

# Install Requirements
RUN pip install -U pip setuptools wheel
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

# Copy Project Code > Docker
COPY . /code/