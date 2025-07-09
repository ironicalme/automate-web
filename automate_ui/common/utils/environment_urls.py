"""
Environment-specific URL and configuration mappings.
This module provides environment-specific URLs that are not stored in AWS Secrets Manager.
"""

from typing import Any, Dict

# Environment-specific URL mappings
ENVIRONMENT_URLS = {
    "development": {
        "api": {
            "public": {
                "base_url": "https://dev-api.example.com"
            },
            "private": {
                "internal_url": "https://dev-internal-api.example.com"
            }
        },
        "web_app": {
            "base_url": "https://www.google.com",
            "admin_url": "https://dev-admin.example.com"
        },

        "database": {
            "host": "dev-db.example.com",
            "port": 5432,
            "username": "dev_user",
            "password": "dev_password",
            "name": "dev_database"
        }
    },
    "staging": {
        "api": {
            "public": {
                "base_url": "https://staging-api.example.com"
            },
            "private": {
                "internal_url": "https://staging-internal-api.example.com"
            }
        },
        "web_app": {
            "base_url": "https://staging-app.example.com",
            "admin_url": "https://staging-admin.example.com"
        },

        "database": {
            "host": "staging-db.example.com",
            "port": 5432,
            "username": "staging_user",
            "password": "staging_password",
            "name": "staging_database"
        }
    },
    "production": {
        "api": {
            "public": {
                "base_url": "https://api.example.com"
            },
            "private": {
                "internal_url": "https://internal-api.example.com"
            }
        },
        "web_app": {
            "base_url": "https://app.example.com",
            "admin_url": "https://admin.example.com"
        },

        "database": {
            "host": "prod-db.example.com",
            "port": 5432,
            "username": "prod_user",
            "password": "prod_password",
            "name": "prod_database"
        }
    }
}


def get_environment_urls(environment: str) -> Dict[str, Any]:
    """
    Get environment-specific URLs and configurations.

    Args:
        environment: The environment name (development/staging/production)

    Returns:
        Dictionary containing environment-specific URLs and configurations

    Raises:
        KeyError: If the environment doesn't exist
    """
    if environment not in ENVIRONMENT_URLS:
        available_envs = list(ENVIRONMENT_URLS.keys())
        raise KeyError(f"Environment '{environment}' not found. Available environments: {available_envs}")

    return ENVIRONMENT_URLS[environment]


def get_environment_url(environment: str, service: str, url_type: str = "base_url") -> str:
    """
    Get a specific URL for an environment and service.

    Args:
        environment: The environment name (development/staging/production)
        service: The service name (api.public, web_app, mobile_app, etc.)
        url_type: The URL type (base_url, admin_url, internal_url, etc.)

    Returns:
        The URL for the specified environment, service, and type

    Raises:
        KeyError: If the environment, service, or URL type doesn't exist
    """
    env_urls = get_environment_urls(environment)

    # Navigate to the service level
    service_parts = service.split('.')
    current = env_urls

    for part in service_parts:
        if part not in current:
            raise KeyError(f"Service '{service}' not found in environment '{environment}'")
        current = current[part]

    # Get the specific URL type
    if url_type not in current:
        raise KeyError(f"URL type '{url_type}' not found for service '{service}' in environment '{environment}'")

    return current[url_type]


def get_available_environments() -> list:
    """
    Get list of available environments.

    Returns:
        List of available environment names
    """
    return list(ENVIRONMENT_URLS.keys())


def get_environment_database_config(environment: str) -> Dict[str, Any]:
    """
    Get database configuration for a specific environment.

    Args:
        environment: The environment name (development/staging/production)

    Returns:
        Dictionary containing database configuration
    """
    env_urls = get_environment_urls(environment)
    return env_urls.get("database", {})