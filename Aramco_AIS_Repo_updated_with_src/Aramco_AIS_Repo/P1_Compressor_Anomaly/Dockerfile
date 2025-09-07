# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy source code and supporting files
COPY src /app/src
COPY configs /app/configs
COPY dashboards /app/dashboards
COPY docs /app/docs

# Expose service port
EXPOSE 8000

# Default command: start the FastAPI scoring service
CMD ["uvicorn", "src.serve:app", "--host", "0.0.0.0", "--port", "8000"]