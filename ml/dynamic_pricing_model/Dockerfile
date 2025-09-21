FROM python:3.11-slim

WORKDIR /app

COPY ml/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ml/dynamic_pricing_model/ .

COPY common/ ./common/
RUN pip install -r ./common/requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/app/common"

ENTRYPOINT ["python", "-m", "train"]