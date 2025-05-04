# Use the official Streamlit image as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's code into the container
COPY . /app

# Expose the port Streamlit will run on
EXPOSE 8501

# Command to run Streamlit when the container starts
CMD ["streamlit", "run","main.py"]
