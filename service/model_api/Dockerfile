FROM python:3.11-slim

WORKDIR /app
COPY . /app

# RUN apt-get update && apt-get install -y  ffmpeg libsm6 libxext6 && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y g++
RUN pip3 install -r requirements.txt

CMD ["python3", "entrypoints.py"]
