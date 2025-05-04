# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install OS packages
RUN apt-get update && apt-get install -y git gcc g++ curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install DVC with GCS support
RUN pip install dvc[gcs]

# Copy project files
COPY . .

# Initialize DVC (if needed inside container)
RUN dvc init --no-scm && dvc config core.no_scm true

# Expose Streamlit port
EXPOSE 8501

# Entrypoint script
ENTRYPOINT ["python", "entrypoint.py"]
