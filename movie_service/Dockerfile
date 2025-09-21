FROM python:3.13-slim

WORKDIR /app

# Copy requirements and install
COPY movie_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service code
COPY movie_service/ ./
# Copy common utils
COPY common/ ./common/
RUN pip install -r ./common/requirements.txt

COPY .env ./
EXPOSE 8000

ENV PYTHONPATH="${PYTHONPATH}:/app/common"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
