FROM python:3.13-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service code
COPY services/inference_service/ ./
# Copy common utils
COPY common/ ./common/

COPY .env ./
EXPOSE 8000
ENV DOCKER_ENV=true

ENV PYTHONPATH="${PYTHONPATH}:/app/common"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
