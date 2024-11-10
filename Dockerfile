# Use Python 3.12 as base image
FROM python:3.12

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other files
COPY . .

# Set the default command
CMD ["python", "main.py"]
