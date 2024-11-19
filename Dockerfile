# Base Python Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the crawler script
CMD ["python", "crawler.py"]
