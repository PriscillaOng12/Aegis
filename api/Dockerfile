FROM python:3.11-slim

WORKDIR /app

COPY api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY api ./api

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]