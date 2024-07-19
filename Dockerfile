# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install pygame dependencies
RUN apt-get update && apt-get install -y \
    python3-pygame \
    && rm -rf /var/lib/apt/lists/*

# Run main.py when the container launches
CMD ["python", "-m", "chess_ai.main"]
