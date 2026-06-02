FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
		apt-get install -y \
		tesseract-ocr \
		tesseract-ocr-eng

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
RUN playwright install-deps chromium

COPY . .

CMD ["python3", "run_pipeline.py"]
