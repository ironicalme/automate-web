"""
Configuration manager that combines AWS secrets with environment-specific URLs.
This module provides a unified interface for accessing both secrets and environment-specific configurations.
"""

from typing import Any, Dict, Optional

from .aws_secrets import get_config_with_aws_fallback
from .aws_secrets import get_nested_value
from .environment_urls import get_environment_database_config
from .environment_urls import get_environment_url
from .environment_urls import get_environment_urls


class ConfigManager:
    """
    Manages configuration by combining AWS secrets with environment-specific URLs.
    """

    def __init__(self, yaml_file_path: str, environment: str, aws_secret_name: Optional[str] = None, aws_region: Optional[str] = None):
        """
        Initialize the config manager.

        Args:
            yaml_file_path: Path to the YAML configuration file
            environment: Environment name (development/staging/production)
            aws_secret_name: AWS Secrets Manager secret name (optional)
            aws_region: AWS region (optional)
        """
        self.yaml_file_path = yaml_file_path
        self.environment = environment
        self.aws_secret_name = aws_secret_name
        self.aws_region = aws_region

        # Load secrets from AWS or YAML
        self.secrets = get_config_with_aws_fallback(
            yaml_file_path=yaml_file_path,
            aws_secret_name=aws_secret_name,
            aws_region=aws_region
        )

        # Load environment-specific URLs
        self.env_urls = get_environment_urls(environment)

    def get_secret(self, key_path: str) -> Any:
        """
        Get a secret value using dot notation.

        Args:
            key_path: Dot-separated path to the secret (e.g., 'api.public.key')

        Returns:
            The secret value

        Raises:
            KeyError: If the key path doesn't exist
        """
        return get_nested_value(self.secrets, key_path)

    def get_url(self, service: str, url_type: str = "base_url") -> str:
        """
        Get an environment-specific URL.

        Args:
            service: The service name (api.public, web_app, mobile_app, etc.)
            url_type: The URL type (base_url, admin_url, internal_url, etc.)

        Returns:
            The URL for the specified service and type

        Raises:
            KeyError: If the service or URL type doesn't exist
        """
        return get_environment_url(self.environment, service, url_type)

    def get_database_config(self) -> Dict[str, Any]:
        """
        Get database configuration for the current environment.

        Returns:
            Dictionary containing database configuration
        """
        return get_environment_database_config(self.environment)

    def get_api_config(self) -> Dict[str, Any]:
        """
        Get complete API configuration (secrets + URLs) for the current environment.

        Returns:
            Dictionary containing API configuration
        """
        return {
            "public": {
                "key": self.get_secret("api.public.key"),
                "base_url": self.get_url("api.public", "base_url")
            },
            "private": {
                "admin_key": self.get_secret("api.private.admin_key"),
                "internal_url": self.get_url("api.private", "internal_url")
            }
        }

    def get_web_app_config(self) -> Dict[str, str]:
        """
        Get web app configuration for the current environment.

        Returns:
            Dictionary containing web app URLs
        """
        return {
            "base_url": self.get_url("web_app", "base_url"),
            "admin_url": self.get_url("web_app", "admin_url")
        }



    def get_aws_config(self) -> Dict[str, Any]:
        """
        Get AWS configuration (from secrets).

        Returns:
            Dictionary containing AWS configuration
        """
        return {
            "region": self.get_secret("aws.region"),
            "access_key": self.get_secret("aws.access_key"),
            "secret_key": self.get_secret("aws.secret_key")
        }

    def get_all_secrets(self) -> Dict[str, Any]:
        """
        Get all secrets (from YAML/AWS).

        Returns:
            Dictionary containing all secrets
        """
        return self.secrets


def create_config_manager(yaml_file_path: str, environment: str, aws_secret_name: Optional[str] = None, aws_region: Optional[str] = None) -> ConfigManager:
    """
    Create a config manager instance.

    Args:
        yaml_file_path: Path to the YAML configuration file
        environment: Environment name (development/staging/production)
        aws_secret_name: AWS Secrets Manager secret name (optional)
        aws_region: AWS region (optional)

    Returns:
        ConfigManager instance
    """
    return ConfigManager(yaml_file_path, environment, aws_secret_name, aws_region)