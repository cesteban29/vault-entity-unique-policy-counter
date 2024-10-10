import os  # Import the os module to access environment variables
import requests  # Import requests to make HTTP requests to Vault API
from typing import List, Dict, Tuple, Set  # Import type hints for better code clarity

# Vault API settings
vault_addr = os.environ["VAULT_ADDR"]  # Fetch the Vault address from the environment variable
vault_token = os.environ["VAULT_TOKEN"]  # Fetch the Vault token from the environment variable

# Get cert_auth_mount_accessors as a comma-separated list from environment variable
cert_auth_mount_accessors = os.environ["CERT_AUTH_MOUNT_ACCESSORS"].split(',')  # Split the cert auth mount accessors into a list

# Optional: Fetch the Vault namespace if provided in the environment variable, or use an empty string if not set
vault_namespace = os.environ.get("VAULT_NAMESPACE", "")

# Set up headers for Vault API request
headers = {
    "X-Vault-Token": vault_token  # Add Vault token to the request headers
}

# Add X-Vault-Namespace header if a namespace is specified
if vault_namespace:
    headers["X-Vault-Namespace"] = vault_namespace  # Include the namespace in headers if it's set

def get_entities() -> List[str]:
    """
    Retrieve all entity IDs from Vault.

    Returns:
        List[str]: A list of entity IDs.
    """
    url = f"{vault_addr}/v1/identity/entity/id"  # Construct the Vault API URL for fetching entity IDs
    response = requests.get(url, headers=headers)  # Make the HTTP GET request to Vault
    response.raise_for_status()  # Raise an error if the request was unsuccessful
    return response.json()['data']['keys']  # Return the list of entity IDs from the response

def get_entity_details(entity_id: str) -> Dict:
    """
    Fetch details for a specific entity.

    Args:
        entity_id (str): The ID of the entity.

    Returns:
        Dict: The details of the entity as a dictionary.
    """
    url = f"{vault_addr}/v1/identity/entity/id/{entity_id}"  # Construct the Vault API URL for fetching entity details
    response = requests.get(url, headers=headers)  # Make the HTTP GET request to Vault
    response.raise_for_status()  # Raise an error if the request was unsuccessful
    return response.json()['data']  # Return the entity details from the response

def has_cert_auth_alias(entity: Dict) -> bool:
    """
    Check if an entity has a single alias tied to any of the Certificate Auth methods.

    Args:
        entity (Dict): The entity details.

    Returns:
        bool: True if the entity has a single alias tied to a cert auth method, False otherwise.
    """
    aliases = entity['aliases']  # Get the list of aliases from the entity
    # Return True if there is exactly one alias and its mount_accessor matches any in cert_auth_mount_accessors
    return len(aliases) == 1 and aliases[0]['mount_accessor'] in cert_auth_mount_accessors

def get_entity_policies(entity: Dict) -> Tuple[str, ...]:
    """
    Get the sorted tuple of policies attached to the entity.

    Args:
        entity (Dict): The entity details.

    Returns:
        Tuple[str, ...]: A tuple of sorted policies attached to the entity.
    """
    return tuple(sorted(entity['policies']))  # Sort the policies alphabetically and return them as a tuple

def calculate_unique_policy_entities() -> int:
    """
    Calculate the number of entities with unique policies and Cert auth alias.

    Returns:
        int: The number of unique entities.
    """
    entities = get_entities()  # Get the list of all entity IDs
    unique_policies_seen: Set[Tuple[str, ...]] = set()  # Initialize an empty set to track unique policy combinations
    unique_policy_entities_count = 0  # Initialize a counter for entities with unique policies

    for entity_id in entities:
        entity = get_entity_details(entity_id)  # Fetch the details for the current entity
        if has_cert_auth_alias(entity):  # Check if the entity has a Cert auth alias
            policies = get_entity_policies(entity)  # Get the policies for the entity
            if policies not in unique_policies_seen:  # If these policies are unique, proceed
                unique_policies_seen.add(policies)  # Add the unique policies to the set
                unique_policy_entities_count += 1  # Increment the counter

    return unique_policy_entities_count  # Return the count of entities with unique policies

if __name__ == "__main__":
    try:
        result = calculate_unique_policy_entities()  # Calculate the number of unique entities
        print(f"Total Vault entities with unique policies and tied to Cert Auth: {result}")  # Output the result
        if vault_namespace:
            print(f"Namespace used: {vault_namespace}")  # Print the namespace if it was used
        print(f"Cert Auth Mount Accessors used: {', '.join(cert_auth_mount_accessors)}")  # Output the cert auth mount accessors being used
    except requests.RequestException as e:
        # Handle any errors related to the Vault API requests
        print(f"Error communicating with Vault: {str(e)}")
    except KeyError as e:
        # Handle unexpected data structures in the Vault response
        print(f"Unexpected data structure in Vault response: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {str(e)}")