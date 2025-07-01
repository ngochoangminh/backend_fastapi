FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*
ADD requirements.txt requirements.txt 
RUN pip install -r requirements.txt

COPY . .

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]