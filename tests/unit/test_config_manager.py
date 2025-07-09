from unittest.mock import Mock
from unittest.mock import patch

import pytest

from automate_ui.apps.api_app.client import APIClient
from automate_ui.common.utils.config_manager import ConfigManager
from automate_ui.common.utils.config_manager import create_config_manager


class TestConfigManager:
    """Test cases for the ConfigManager class."""

    def test_config_manager_initialization(self):
        """Test ConfigManager initialization."""
        config_manager = ConfigManager(
            yaml_file_path='local_secrets.yaml',
            environment='development',
            aws_secret_name=None,
            aws_region=None
        )

        assert config_manager.yaml_file_path == 'local_secrets.yaml'
        assert config_manager.environment == 'development'
        assert config_manager.aws_secret_name is None
        assert config_manager.aws_region is None
        assert config_manager.secrets is not None
        assert config_manager.env_urls is not None

    def test_get_secret(self):
        """Test getting secrets from the config manager."""
        config_manager = ConfigManager(
            yaml_file_path='local_secrets.yaml',
            environment='development'
        )

        # Test getting API key
        api_key = config_manager.get_secret('api.public.key')
        assert api_key == 'your-api-key-here'

        # Test getting admin key
        admin_key = config_manager.get_secret('api.private.admin_key')
        assert admin_key == 'your-admin-key'

    def test_get_url(self):
        """Test getting environment-specific URLs."""
        config_manager = ConfigManager(
            yaml_file_path='local_secrets.yaml',
            environment='development'
        )

        # Test getting API URL
        api_url = config_manager.get_url('api.public', 'base_url')
        assert api_url == 'https://dev-api.example.com'

        # Test getting web app URL
        web_url = config_manager.get_url('web_app', 'base_url')
        assert web_url == 'https://www.google.com'

        # Test getting admin URL
        admin_url = config_manager.get_url('web_app', 'admin_url')
        assert admin_url == 'https://dev-admin.example.com'

    def test_get_database_config(self):
        """Test getting database configuration."""
        config_manager = ConfigManager(
            yaml_file_path='local_secrets.yaml',
            environment='development'
        )

        db_config = config_manager.get_database_config()

        assert db_config['host'] == 'dev-db.example.com'
        assert db_config['port'] == 5432
        assert db_config['username'] == 'dev_user'
        assert db_config['name'] == 'dev_database'

    def test_get_api_config(self):
        """Test getting complete API configuration."""
        config_manager = ConfigManager(
            yaml_file_path='local_secrets.yaml',
            environment='development'
        )

        api_config = config_manager.get_api_config()

        # Test public API config
        assert api_config['public']['key'] == 'your-api-key-here'
        assert api_config['public']['base_url'] == 'https://dev-api.example.com'

        # Test private API config
        assert api_config['private']['admin_key'] == 'your-admin-key'
        assert api_config['private']['internal_url'] == 'https://dev-internal-api.example.com'

    def test_get_web_app_config(self):
        """Test getting web app configuration."""
        config_manager = ConfigManager(
            yaml_file_path='local_secrets.yaml',
            environment='development'
        )

        web_config = config_manager.get_web_app_config()

        assert web_config['base_url'] == 'https://www.google.com'
        assert web_config['admin_url'] == 'https://dev-admin.example.com'

    def test_get_aws_config(self):
        """Test getting AWS configuration."""
        config_manager = ConfigManager(
            yaml_file_path='local_secrets.yaml',
            environment='development'
        )

        aws_config = config_manager.get_aws_config()

        assert aws_config['region'] == 'us-east-1'
        assert aws_config['access_key'] == 'your-local-access-key'
        assert aws_config['secret_key'] == 'your-local-secret-key'

    def test_get_all_secrets(self):
        """Test getting all secrets."""
        config_manager = ConfigManager(
            yaml_file_path='local_secrets.yaml',
            environment='development'
        )

        all_secrets = config_manager.get_all_secrets()

        # Verify the structure
        assert 'api' in all_secrets
        assert 'database' in all_secrets
        assert 'aws' in all_secrets

        # Verify nested structure
        assert 'public' in all_secrets['api']
        assert 'private' in all_secrets['api']
        assert 'host' in all_secrets['database']
        assert 'port' in all_secrets['database']

    def test_different_environments(self):
        """Test that different environments return different URLs."""
        dev_config = ConfigManager('local_secrets.yaml', 'development')
        staging_config = ConfigManager('local_secrets.yaml', 'staging')
        prod_config = ConfigManager('local_secrets.yaml', 'production')

        # Test API URLs for different environments
        dev_api_url = dev_config.get_url('api.public', 'base_url')
        staging_api_url = staging_config.get_url('api.public', 'base_url')
        prod_api_url = prod_config.get_url('api.public', 'base_url')

        assert dev_api_url == 'https://dev-api.example.com'
        assert staging_api_url == 'https://staging-api.example.com'
        assert prod_api_url == 'https://api.example.com'

        # Test web app URLs for different environments
        dev_web_url = dev_config.get_url('web_app', 'base_url')
        staging_web_url = staging_config.get_url('web_app', 'base_url')
        prod_web_url = prod_config.get_url('web_app', 'base_url')

        assert dev_web_url == 'https://www.google.com'
        assert staging_web_url == 'https://staging-app.example.com'
        assert prod_web_url == 'https://app.example.com'

    def test_invalid_environment(self):
        """Test that invalid environment raises appropriate error."""
        with pytest.raises(KeyError) as exc_info:
            ConfigManager('local_secrets.yaml', 'invalid_env')

        assert "Environment 'invalid_env' not found" in str(exc_info.value)

    def test_invalid_service(self):
        """Test that invalid service raises appropriate error."""
        config_manager = ConfigManager('local_secrets.yaml', 'development')

        with pytest.raises(KeyError) as exc_info:
            config_manager.get_url('invalid_service', 'base_url')

        assert "Service 'invalid_service' not found" in str(exc_info.value)

    def test_invalid_url_type(self):
        """Test that invalid URL type raises appropriate error."""
        config_manager = ConfigManager('local_secrets.yaml', 'development')

        with pytest.raises(KeyError) as exc_info:
            config_manager.get_url('web_app', 'invalid_url_type')

        assert "URL type 'invalid_url_type' not found" in str(exc_info.value)

    def test_invalid_secret_key(self):
        """Test that invalid secret key raises appropriate error."""
        config_manager = ConfigManager('local_secrets.yaml', 'development')

        with pytest.raises(KeyError) as exc_info:
            config_manager.get_secret('invalid.key')

        assert "Key path 'invalid.key' not found" in str(exc_info.value)

    @pytest.mark.parametrize("secret_path,expected_type", [
        ("api.public.key", str),
        ("database.port", int),
        ("aws.region", str),
    ])
    def test_config_value_types(self, secret_path, expected_type):
        """Test that config values have the expected types."""
        config_manager = ConfigManager('local_secrets.yaml', 'development')
        value = config_manager.get_secret(secret_path)
        assert isinstance(value, expected_type)


class TestCreateConfigManager:
    """Test cases for the create_config_manager function."""

    def test_create_config_manager(self):
        """Test creating a config manager using the factory function."""
        config_manager = create_config_manager(
            yaml_file_path='local_secrets.yaml',
            environment='development',
            aws_secret_name=None,
            aws_region=None
        )

        assert isinstance(config_manager, ConfigManager)
        assert config_manager.yaml_file_path == 'local_secrets.yaml'
        assert config_manager.environment == 'development'


class TestConfigManagerIntegration:
    """Test cases for ConfigManager integration with API client."""

    def test_api_client_integration(self):
        """Test creating API client with ConfigManager."""
        config_manager = ConfigManager('local_secrets.yaml', 'development')

        # Get API configuration
        api_key = config_manager.get_secret('api.public.key')
        api_url = config_manager.get_url('api.public', 'base_url')

        # Create API client
        client = APIClient(base_url=api_url)
        client.authenticate(api_key=api_key)

        # Verify client configuration
        assert client.base_url.endswith('/api/public/')
        assert 'Authorization' in client.session.headers
        assert client.session.headers['Authorization'] == f'Api-Key {api_key}'
        assert 'secret-header' in client.session.headers

    def test_comprehensive_config_access(self):
        """Test comprehensive access to all configuration types."""
        config_manager = ConfigManager('local_secrets.yaml', 'development')

        # Test all URL types
        urls_to_test = [
            ('api.public', 'base_url'),
            ('api.private', 'internal_url'),
            ('web_app', 'base_url'),
            ('web_app', 'admin_url')
        ]

        for service, url_type in urls_to_test:
            url = config_manager.get_url(service, url_type)
            assert url is not None
            assert url.startswith('https://')

        # Test all secret types
        secrets_to_test = [
            'api.public.key',
            'api.private.admin_key',
            'database.host',
            'database.port',
            'aws.region',
            'aws.access_key'
        ]

        for secret_path in secrets_to_test:
            secret = config_manager.get_secret(secret_path)
            assert secret is not None

        # Test complete configurations
        api_config = config_manager.get_api_config()
        web_config = config_manager.get_web_app_config()
        db_config = config_manager.get_database_config()
        aws_config = config_manager.get_aws_config()

        assert api_config is not None
        assert web_config is not None
        assert db_config is not None
        assert aws_config is not None


class TestConfigManagerWithFixture:
    """Test cases for ConfigManager using the pytest fixture."""

    def test_config_manager_fixture(self, config_manager):
        """Test the config_manager fixture."""
        # Test basic functionality
        api_key = config_manager.get_secret('api.public.key')
        api_url = config_manager.get_url('api.public', 'base_url')

        assert api_key is not None
        assert api_url is not None

    def test_config_manager_with_aws_fallback(self, config_manager):
        """Test that config_manager works with AWS fallback logic."""
        # Get a value that should exist in our YAML file
        api_key = config_manager.get_secret('api.public.key')
        assert api_key is not None
        assert isinstance(api_key, str)

    def test_config_manager_missing_key_raises_error(self, config_manager):
        """Test that accessing missing config keys raises appropriate error."""
        with pytest.raises(KeyError) as exc_info:
            config_manager.get_secret('nonexistent.key')

        assert "Key path 'nonexistent.key' not found" in str(exc_info.value)

    def test_config_manager_api_integration(self, config_manager):
        """Test a realistic API integration scenario."""
        # Simulate a real API integration test
        api_key = config_manager.get_secret('api.public.key')
        base_url = config_manager.get_url('api.public', 'base_url')

        # Create client (in real scenario, you might make actual API calls)
        client = APIClient(base_url=base_url)
        client.authenticate(api_key=api_key)

        # Verify client is properly configured for API calls
        assert client.base_url is not None
        assert client.session.headers['Authorization'] == f'Api-Key {api_key}'


class TestConfigManagerCommandLineOptions:
    """Test the config_manager fixture with different command-line options."""

    def test_config_with_custom_yaml_path(self, config_manager):
        """Test config_manager fixture with custom YAML path (would be set via --yaml-config)."""
        # This test would be run with: pytest --yaml-config=custom_secrets.yaml
        api_key = config_manager.get_secret('api.public.key')
        assert api_key is not None

    def test_config_with_aws_secret(self, config_manager):
        """Test config_manager fixture with AWS secret (would be set via --aws-secret)."""
        # This test would be run with: pytest --aws-secret=my-app-secrets
        api_key = config_manager.get_secret('api.public.key')
        assert api_key is not None

    def test_config_with_aws_region(self, config_manager):
        """Test config_manager fixture with AWS region (would be set via --aws-region)."""
        # This test would be run with: pytest --aws-region=us-west-2
        api_key = config_manager.get_secret('api.public.key')
        assert api_key is not None