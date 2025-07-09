#!/usr/bin/env python3
"""
Example demonstrating environment-specific configuration usage.
"""

from automate_ui.apps.api_app.client import APIClient


def example_development_usage():
    """Example usage for development environment."""
    print("=== Development Environment Example ===\n")

    # This would be run with: pytest --env=development
    # Or use the default development environment

    # In a real test, you would inject the config fixture:
    # def test_development_api(config_manager):
    #     api_key = config_manager.get_secret('api.public.key')
    #     api_url = config_manager.get_url('api.public', 'base_url')

    # For demonstration, we'll simulate the config values
    api_key = "dev-api-key-here"
    api_url = "https://dev-api.example.com"
    web_url = "https://dev-app.example.com"

    print(f"API Key: {api_key}")
    print(f"API URL: {api_url}")
    print(f"Web App URL: {web_url}")

    # Create API client
    client = APIClient(base_url=api_url)
    client.authenticate(api_key=api_key)

    print(f"Configured API Client: {client.base_url}")
    print(f"Authorization Header: {client.session.headers.get('Authorization')}")


def example_staging_usage():
    """Example usage for staging environment."""
    print("\n=== Staging Environment Example ===\n")

    # This would be run with: pytest --env=staging

    # Simulate staging config values
    api_key = "staging-api-key-here"
    api_url = "https://staging-api.example.com"
    web_url = "https://staging-app.example.com"

    print(f"API Key: {api_key}")
    print(f"API URL: {api_url}")
    print(f"Web App URL: {web_url}")

    # Create API client
    client = APIClient(base_url=api_url)
    client.authenticate(api_key=api_key)

    print(f"Configured API Client: {client.base_url}")
    print(f"Authorization Header: {client.session.headers.get('Authorization')}")


def example_production_usage():
    """Example usage for production environment."""
    print("\n=== Production Environment Example ===\n")

    # This would be run with: pytest --env=production

    # Simulate production config values
    api_key = "prod-api-key-here"
    api_url = "https://api.example.com"
    web_url = "https://app.example.com"

    print(f"API Key: {api_key}")
    print(f"API URL: {api_url}")
    print(f"Web App URL: {web_url}")

    # Create API client
    client = APIClient(base_url=api_url)
    client.authenticate(api_key=api_key)

    print(f"Configured API Client: {client.base_url}")
    print(f"Authorization Header: {client.session.headers.get('Authorization')}")


def example_command_line_options():
    """Example of different command-line options."""
    print("\n=== Command Line Options Examples ===\n")

    print("1. Default development environment:")
    print("   pytest")
    print("   # Uses: local_secrets.yaml, env=development")

    print("\n2. Staging environment with custom YAML:")
    print("   pytest --env=staging --yaml-config=staging_secrets.yaml")

    print("\n3. Production environment with AWS Secrets Manager:")
    print("   pytest --env=production --aws-secret=my-app-prod-secrets --aws-region=us-west-2")

    print("\n4. Custom environment with all options:")
    print("   pytest --env=staging --yaml-config=custom.yaml --aws-secret=backup-secrets --aws-region=eu-west-1")


def example_test_scenarios():
    """Example test scenarios using the environment config."""
    print("\n=== Example Test Scenarios ===\n")

    print("1. API Integration Test:")
    print("""
    def test_api_integration(config_manager):
        # Get environment-specific API configuration
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
        # Get environment-specific web app URL
        web_url = config_manager.get_url('web_app', 'base_url')

        # Navigate to web app
        page.goto(web_url)

        # Perform login test
        page.fill('#username', 'test@example.com')
        page.fill('#password', 'password')
        page.click('#login-button')

        assert page.url.endswith('/dashboard')
    """)

    print("\n3. Admin Panel Test:")
    print("""
    def test_admin_panel(config_manager):
        # Get environment-specific admin panel URL
        admin_url = config_manager.get_url('web_app', 'admin_url')

        # Navigate to admin panel
        page.goto(admin_url)

        # Perform admin authentication
        page.fill('#admin-username', 'admin@example.com')
        page.fill('#admin-password', 'admin-password')
        page.click('#admin-login')

        assert page.url.endswith('/admin/dashboard')
    """)

    print("\n4. Database Test:")
    print("""
    def test_database_connection(config_manager):
        # Get environment-specific database config
        db_config = config_manager.get_database_config()
        db_host = db_config['host']
        db_port = db_config['port']
        db_name = db_config['name']

        # Test database connection
        # ... database testing code ...
    """)


if __name__ == "__main__":
    example_development_usage()
    example_staging_usage()
    example_production_usage()
    example_command_line_options()
    example_test_scenarios()