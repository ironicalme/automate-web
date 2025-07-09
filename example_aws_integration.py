#!/usr/bin/env python3
"""
Example script demonstrating AWS Secrets Manager integration with YAML fallback.
"""

from automate_ui.common.utils.config_manager import ConfigManager


def example_usage():
    """Demonstrate how to use the AWS integration with fallback."""

    print("=== AWS Secrets Manager Integration Example ===\n")

    # Example 1: Try AWS first, fallback to YAML
    try:
        config_manager = ConfigManager(
            yaml_file_path='local_secrets.yaml',
            environment='development',
            aws_secret_name='my-app-secrets',
            aws_region='us-east-1'
        )
        api_key = config_manager.get_secret('api.public.key')
        print(f"Retrieved API key: {api_key}")
    except Exception as e:
        print(f"Error retrieving API key: {e}")

    # Example 2: Database configuration
    try:
        config_manager = ConfigManager(
            yaml_file_path='local_secrets.yaml',
            environment='development',
            aws_secret_name='my-app-database-secrets'
        )
        db_config = config_manager.get_database_config()
        print(f"Database host: {db_config['host']}")
    except Exception as e:
        print(f"Error retrieving database host: {e}")

    # Example 3: AWS credentials (for AWS services)
    try:
        config_manager = ConfigManager(
            yaml_file_path='local_secrets.yaml',
            environment='development',
            aws_secret_name='my-app-aws-config'
        )
        aws_region = config_manager.get_secret('aws.region')
        print(f"AWS region: {aws_region}")
    except Exception as e:
        print(f"Error retrieving AWS region: {e}")

    # Example 4: Environment-specific URLs
    try:
        config_manager = ConfigManager(
            yaml_file_path='local_secrets.yaml',
            environment='production',
            aws_secret_name='my-app-prod-secrets'
        )
        api_url = config_manager.get_url('api.public', 'base_url')
        web_url = config_manager.get_url('web_app', 'base_url')
        print(f"Production API URL: {api_url}")
        print(f"Production Web URL: {web_url}")
    except Exception as e:
        print(f"Error retrieving URLs: {e}")

if __name__ == "__main__":
    example_usage()