FROM python:3.10

WORKDIR /app

ADD requirements.txt requirements.txt

RUN python -m pip install -r requirements.txt

ADD entry.py /app/entry.py
ADD core /app/core
ADD shared_grpc /app/shared_grpc
ADD services/user_service /app/services/user_service

CMD ["uvicorn", "services.user_service.main:app", "--host", "0.0.0.0","--port", "8000"]