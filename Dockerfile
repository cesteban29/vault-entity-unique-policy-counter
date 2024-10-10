# Base image for Python 3
FROM python:3.9-slim

# Set environment variables (these can be overridden at runtime using docker run -e)
ENV VAULT_ADDR=""
ENV VAULT_TOKEN=""
ENV CERT_AUTH_MOUNT_ACCESSORS=""
ENV VAULT_NAMESPACE=""

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir requests

# Make sure the script is executable
RUN chmod +x /app/vault_entity_unique_policy_counter.py

# Command to run the script when the container starts
CMD ["python", "/app/vault_entity_unique_policy_counter.py"]