FROM python:3.11

WORKDIR /api

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api ./api
COPY ./config ./config
COPY ./service ./service

CMD ["uvicorn", "api.main:api", "--host", "0.0.0.0", "--port", "8000"]