# Start Docker : Python + Kernal
FROM python:3.12

# ENV: Show Logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        gettext \
    && rm -rf /var/lib/apt/lists/*

# Create Project Folder 
WORKDIR /code

# Copy Requirements
COPY requirements.txt /code/requirements.txt

# Install Requirements
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y netcat-openbsd
# Copy Project Code > Docker
COPY . /code/