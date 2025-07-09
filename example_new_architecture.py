#!/usr/bin/env python3
"""
Example demonstrating the new architecture with separated secrets and environment URLs.
"""

from automate_ui.apps.api_app.client import APIClient
from automate_ui.common.utils.config_manager import ConfigManager
from automate_ui.common.utils.config_manager import create_config_manager


def example_direct_config_manager_usage():
    """Example of using ConfigManager directly."""
    print("=== Direct ConfigManager Usage ===\n")

    # Create config manager for development environment
    config_manager = ConfigManager(
        yaml_file_path='local_secrets.yaml',
        environment='development'
    )

    # Get secrets (from YAML/AWS)
    api_key = config_manager.get_secret('api.public.key')
    admin_key = config_manager.get_secret('api.private.admin_key')

    # Get environment-specific URLs
    api_url = config_manager.get_url('api.public', 'base_url')
    web_url = config_manager.get_url('web_app', 'base_url')
    admin_url = config_manager.get_url('web_app', 'admin_url')

    print(f"API Key: {api_key}")
    print(f"API URL: {api_url}")
    print(f"Web App URL: {web_url}")
    print(f"Admin URL: {admin_url}")

    # Create API client
    client = APIClient(base_url=api_url)
    client.authenticate(api_key=api_key)

    print(f"Configured API Client: {client.base_url}")


def example_different_environments():
    """Example of using different environments."""
    print("\n=== Different Environments ===\n")

    environments = ['development', 'staging', 'production']

    for env in environments:
        print(f"--- {env.upper()} Environment ---")

        config_manager = ConfigManager('local_secrets.yaml', env)

                # Same secrets, different URLs
        api_key = config_manager.get_secret('api.public.key')  # Same key
        api_url = config_manager.get_url('api.public', 'base_url')  # Different URL
        web_url = config_manager.get_url('web_app', 'base_url')  # Different URL
        admin_url = config_manager.get_url('web_app', 'admin_url')  # Different URL

        print(f"API Key: {api_key}")
        print(f"API URL: {api_url}")
        print(f"Web URL: {web_url}")
        print(f"Admin URL: {admin_url}")
        print()


def example_aws_integration():
    """Example of AWS integration with environment URLs."""
    print("\n=== AWS Integration Example ===\n")

    # This would be used when AWS credentials are available
    config_manager = ConfigManager(
        yaml_file_path='local_secrets.yaml',
        environment='production',
        aws_secret_name='my-app-prod-secrets',
        aws_region='us-west-2'
    )

    # Secrets come from AWS, URLs come from environment mapping
    api_key = config_manager.get_secret('api.public.key')  # From AWS
    api_url = config_manager.get_url('api.public', 'base_url')  # From environment mapping

    print(f"API Key: {api_key}")
    print(f"API URL: {api_url}")


def example_complete_configurations():
    """Example of getting complete configurations."""
    print("\n=== Complete Configurations ===\n")

    config_manager = ConfigManager('local_secrets.yaml', 'development')

    # Get complete API configuration
    api_config = config_manager.get_api_config()
    print("API Configuration:")
    print(f"  Public Key: {api_config['public']['key']}")
    print(f"  Public URL: {api_config['public']['base_url']}")
    print(f"  Admin Key: {api_config['private']['admin_key']}")
    print(f"  Internal URL: {api_config['private']['internal_url']}")

    # Get complete web app configuration
    web_config = config_manager.get_web_app_config()
    print("\nWeb App Configuration:")
    print(f"  Base URL: {web_config['base_url']}")
    print(f"  Admin URL: {web_config['admin_url']}")

    # Get database configuration
    db_config = config_manager.get_database_config()
    print("\nDatabase Configuration:")
    print(f"  Host: {db_config['host']}")
    print(f"  Port: {db_config['port']}")
    print(f"  Username: {db_config['username']}")
    print(f"  Database: {db_config['name']}")


def example_test_scenarios():
    """Example test scenarios using the new architecture."""
    print("\n=== Test Scenarios ===\n")

    print("1. API Integration Test:")
    print("""
    def test_api_integration(config_manager):
        # Get API configuration
        api_key = config_manager.get_secret('api.public.key')
        api_url = config_manager.get_url('api.public', 'base_url')

        # Create API client
        client = APIClient(base_url=api_url)
        client.authenticate(api_key=api_key)

        # Make API calls
        response = client.get('/users')
        assert response.status_code == 200
    """)

    print("\n2. Web App Test:")
    print("""
    def test_web_app_login(config_manager):
        # Get web app URL
        web_url = config_manager.get_url('web_app', 'base_url')

        # Navigate to web app
        page.goto(web_url)

        # Perform login test
        page.fill('#username', 'test@example.com')
        page.fill('#password', 'password')
        page.click('#login-button')

        assert page.url.endswith('/dashboard')
    """)

    print("\n3. Database Test:")
    print("""
    def test_database_connection(config_manager):
        # Get database configuration
        db_config = config_manager.get_database_config()

        # Test database connection
        connection = create_db_connection(
            host=db_config['host'],
            port=db_config['port'],
            username=db_config['username'],
            password=db_config['password'],
            database=db_config['name']
        )

        assert connection.is_connected()
    """)


def example_command_line_usage():
    """Example of command-line usage."""
    print("\n=== Command Line Usage ===\n")

    print("1. Development environment (default):")
    print("   pytest")
    print("   # Uses: local_secrets.yaml, env=development")

    print("\n2. Staging environment:")
    print("   pytest --env=staging")
    print("   # Uses: local_secrets.yaml, env=staging")

    print("\n3. Production with AWS:")
    print("   pytest --env=production --aws-secret=my-app-prod-secrets --aws-region=us-west-2")
    print("   # Uses: AWS secrets, env=production URLs")

    print("\n4. Custom YAML with staging:")
    print("   pytest --env=staging --yaml-config=staging_secrets.yaml")
    print("   # Uses: staging_secrets.yaml, env=staging URLs")


if __name__ == "__main__":
    example_direct_config_manager_usage()
    example_different_environments()
    example_aws_integration()
    example_complete_configurations()
    example_test_scenarios()
    example_command_line_usage()