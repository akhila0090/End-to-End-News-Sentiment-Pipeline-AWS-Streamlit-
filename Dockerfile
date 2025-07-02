
FROM python:3.9-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set working directory
WORKDIR /app
# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Copy application code
COPY 
# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app 
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
