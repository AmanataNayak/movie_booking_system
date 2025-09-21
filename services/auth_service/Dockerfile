FROM python:3.13-slim

WORKDIR /app

# Copy requirements and install
COPY services/auth_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service code
COPY auth_service/ ./
# Copy common utils
COPY common/ ./common/
RUN pip install -r ./common/requirements.txt

COPY .env ./
EXPOSE 8000
ENV DOCKER_ENV=true

ENV PYTHONPATH="${PYTHONPATH}:/app/common"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
