# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables for non-interactive apt installs
ENV DEBIAN_FRONTEND=noninteractive

# Install Git and any other dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*  # Clean up APT when done

# Set the working directory inside the container
WORKDIR /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir faker git+https://github.com/dpkp/kafka-python.git

COPY main.py .

# Command to run your chat app (this can be overridden when the pod starts)
#CMD ["python"]
CMD ["tail", "-f", "/dev/null"]
