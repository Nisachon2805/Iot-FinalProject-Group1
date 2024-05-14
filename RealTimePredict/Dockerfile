# Use the official Python image as base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# # Copy the requirements file into the container
# COPY requirements.txt .

EXPOSE 5000

# Install Gunicorn
RUN pip install gunicorn

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run Gunicorn with your Flask application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "RealTimePrediction:app"]
