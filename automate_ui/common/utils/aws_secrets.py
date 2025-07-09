import json
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import NoRegionError

from .config_loader import get_nested_value
from .config_loader import load_yaml_config


def check_aws_credentials() -> bool:
    """
    Check if AWS credentials are available and valid.

    Returns:
        True if AWS credentials are available and can be used, False otherwise
    """
    try:
        # Try to create a session to check credentials
        session = boto3.Session()
        sts = session.client('sts')
        sts.get_caller_identity()
        return True
    except (NoCredentialsError, NoRegionError, ClientError):
        return False


def get_secret_from_aws(secret_name: str, region_name: str = None) -> Optional[Dict[str, Any]]:
    """
    Retrieve a secret from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret in AWS Secrets Manager
        region_name: AWS region name (optional, uses default if not provided)

    Returns:
        Dictionary containing the secret data, or None if retrieval fails

    Raises:
        ClientError: If there's an AWS API error
    """
    try:
        # Create a Secrets Manager client
        if region_name:
            session = boto3.session.Session()
            client = session.client(
                service_name='secretsmanager',
                region_name=region_name
            )
        else:
            client = boto3.client('secretsmanager')

        # Get the secret
        response = client.get_secret_value(SecretId=secret_name)

        # Parse the secret string as JSON
        if 'SecretString' in response:
            return json.loads(response['SecretString'])
        else:
            # Handle binary secrets
            return {'binary_secret': response['SecretBinary']}

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print(f"Secret '{secret_name}' not found in AWS Secrets Manager")
        elif error_code == 'AccessDeniedException':
            print(f"Access denied to secret '{secret_name}' in AWS Secrets Manager")
        else:
            print(f"AWS Secrets Manager error for '{secret_name}': {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing secret '{secret_name}' as JSON: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error retrieving secret '{secret_name}': {e}")
        return None


def get_config_with_aws_fallback(
    yaml_file_path: str,
    aws_secret_name: str = None,
    aws_region: str = None
) -> Dict[str, Any]:
    """
    Get configuration with AWS Secrets Manager fallback.

    First tries to get configuration from AWS Secrets Manager if credentials are available.
    Falls back to YAML file if AWS is not available or fails.

    Args:
        yaml_file_path: Path to the local YAML configuration file
        aws_secret_name: Name of the secret in AWS Secrets Manager (optional)
        aws_region: AWS region name (optional)

    Returns:
        Dictionary containing the configuration data

    Raises:
        FileNotFoundError: If neither AWS nor YAML file is available
    """
    # Check if AWS credentials are available
    if check_aws_credentials() and aws_secret_name:
        print(f"AWS credentials available. Attempting to fetch secret '{aws_secret_name}' from AWS Secrets Manager...")

        # Try to get secret from AWS
        aws_config = get_secret_from_aws(aws_secret_name, aws_region)
        if aws_config:
            print(f"Successfully loaded configuration from AWS Secrets Manager: {aws_secret_name}")
            return aws_config
        else:
            print(f"Failed to retrieve secret '{aws_secret_name}' from AWS. Falling back to YAML file...")

    # Fallback to YAML file
    print(f"Loading configuration from YAML file: {yaml_file_path}")
    try:
        return load_yaml_config(yaml_file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Configuration not available from AWS Secrets Manager or YAML file. "
            f"Please ensure either AWS credentials are configured with secret '{aws_secret_name}' "
            f"or create a local configuration file at '{yaml_file_path}'."
        ) from e


def get_nested_config_value(
    yaml_file_path: str,
    key_path: str,
    aws_secret_name: str = None,
    aws_region: str = None
) -> Any:
    """
    Get a nested configuration value with AWS Secrets Manager fallback.

    Args:
        yaml_file_path: Path to the local YAML configuration file
        key_path: Dot-separated path to the value (e.g., 'api.public.key')
        aws_secret_name: Name of the secret in AWS Secrets Manager (optional)
        aws_region: AWS region name (optional)

    Returns:
        The value at the specified path

    Raises:
        KeyError: If the key path doesn't exist in the configuration
        FileNotFoundError: If neither AWS nor YAML file is available
    """
    config = get_config_with_aws_fallback(yaml_file_path, aws_secret_name, aws_region)
    return get_nested_value(config, key_path)