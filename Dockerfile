# Use Python base image compatible with AMD64 architecture
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything from current folder into the container
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Command to run your script
ENTRYPOINT ["python", "main.py"]
