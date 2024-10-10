# Vault Entity Unique Policy Counter

This Python script interacts with the HashiCorp Vault API to retrieve Vault entities and calculate how many entities have unique policies attached. It specifically focuses on entities that have a Certificate Authentication Method role associated with them.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Setup](#setup)
- [Execution](#execution)
  - [Using Python Directly](#using-python-directly)
  - [Using Docker](#using-docker)
- [Error Handling](#error-handling)
- [Example Output](#example-output)

## Prerequisites

Before running this script, ensure you have the following:

- **Python 3.x** installed on your machine (if not using Docker).
- **Docker** installed if you plan to run the script inside a container.
- Access to a running **HashiCorp Vault** instance.
- **Vault Token** with sufficient permissions to list and retrieve Vault entities and policies.
- Required **environment variables** configured (see below).

### Python Dependencies

The following Python packages are required if you are not using Docker:

- `requests`: Used to make HTTP requests to Vault's API.
- `os`: A standard Python library used for interacting with environment variables.

Install the required dependencies by running:

```bash
pip install requests
```

## Environment Variables

To run the script, you need to set the following environment variables:

| Variable Name           | Description                                                                                          | Example                          |
|-------------------------|------------------------------------------------------------------------------------------------------|----------------------------------|
| `VAULT_ADDR`             | The address of your Vault instance.                                                                  | `https://vault.example.com`      |
| `VAULT_TOKEN`            | Your Vault token for authentication.                                                                | `s.xxxx-yyyy-zzzz`               |
| `CERT_AUTH_MOUNT_ACCESSORS` | A comma-separated list of cert authentication method mount accessors.                                | `auth_cert/abcd,auth_cert/efgh`  |
| `VAULT_NAMESPACE`        | (Optional) Vault namespace if you are using Enterprise Vault with namespaces. Defaults to an empty string. | `my-namespace`                   |

To set these environment variables, you can either export them in your shell or pass them as arguments when running the Docker container.

For example, in a bash shell:

```bash
export VAULT_ADDR="https://vault.example.com"
export VAULT_TOKEN="your-vault-token-here"
export CERT_AUTH_MOUNT_ACCESSORS="auth_cert_mount_accessor"
export VAULT_NAMESPACE="optional-namespace"
```

## Setup

You have two options for running the script: **Using Python directly** or **Using Docker**.

### Option 1: Using Python Directly

1. **Clone the repository or copy the script** to your local machine.
2. **Install dependencies**: Ensure you have the `requests` library installed using:

   ```bash
   pip install requests
   ```

3. **Configure the environment**: Set the environment variables as described in the [Environment Variables](#environment-variables) section.

### Option 2: Using Docker

You can use the provided Dockerfile to build and run the script in a containerized environment, eliminating the need to install Python or dependencies on your local machine.

#### Building the Docker Image

1. **Build the Docker image** by running the following command in your terminal (navigate to the directory containing the `Dockerfile`):

   ```bash
   docker build -t vault-entity-counter .
   ```

This will build a Docker image named `vault-entity-counter` that contains Python and all the necessary dependencies to run the script.

## Execution

### Using Python Directly

Once you have set the required environment variables and installed the dependencies, you can run the script using Python.

```bash
python vault_entity_unique_policy_counter.py
```

### Using Docker

You can run the container with the following command, passing the necessary environment variables to Docker:

```bash
docker run --rm \
  -e VAULT_ADDR="https://vault.example.com" \
  -e VAULT_TOKEN="your-vault-token" \
  -e CERT_AUTH_MOUNT_ACCESSORS="auth_cert_mount_accessor" \
  -e VAULT_NAMESPACE="optional-namespace" \
  vault-entity-counter
```

or you can pass the environment variables using a `.env` file after creating one with the environment variables.

```bash
docker run --rm --env-file .env vault-entity-counter
```

### What the script does:

- It retrieves all Vault entities.
- For each entity, it checks if the entity has a single alias tied to a certificate authentication method.
- It collects the policies attached to the entity and ensures that the policies are sorted and unique.
- It counts how many entities have a unique set of policies attached and displays the result.

## Error Handling

The script is equipped with error handling to manage various scenarios, including:

1. **Vault API Communication Errors**:
   - If the Vault server is unreachable or if there’s an issue with the API request, the script will catch `requests.RequestException` and print an error message.

2. **Unexpected Response Structures**:
   - If the API response doesn’t match the expected format (e.g., missing keys), the script will catch `KeyError` and print an appropriate message.

3. **Other Exceptions**:
   - Any other unexpected issues will be caught and printed as general exceptions.

## Example Output

After successful execution, the script will output the following:

```bash
Total Vault entities with unique policies and tied to Cert Auth: 5
Namespace used: my-namespace
Cert Auth Mount Accessors used: auth_cert_mount_accessor1, auth_cert_mount_accessor2
```

This indicates that there are 5 unique Vault entities that meet the criteria and provides additional information about the namespace and certificate authentication mount accessors used.

## Contact

For further questions or issues, feel free to email me at:

- [cesteban@hashicorp.com](mailto:cesteban@hashicorp.com)
