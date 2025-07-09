import json
import os
import tempfile
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import NoRegionError
import pytest

from automate_ui.common.utils.aws_secrets import check_aws_credentials
from automate_ui.common.utils.aws_secrets import get_config_with_aws_fallback
from automate_ui.common.utils.aws_secrets import get_nested_config_value
from automate_ui.common.utils.aws_secrets import get_secret_from_aws


class TestAWSCredentials:
    """Test cases for AWS credentials checking."""

    @patch('automate_ui.common.utils.aws_secrets.boto3.Session')
    def test_check_aws_credentials_success(self, mock_session: MagicMock):
        """Test successful AWS credentials check."""
        # Mock successful AWS session
        mock_session_instance = Mock()
        mock_sts_client = Mock()
        mock_sts_client.get_caller_identity.return_value = {'Account': '123456789012'}
        mock_session_instance.client.return_value = mock_sts_client
        mock_session.return_value = mock_session_instance

        assert check_aws_credentials() is True

    @patch('automate_ui.common.utils.aws_secrets.boto3.Session')
    def test_check_aws_credentials_no_credentials(self, mock_session: MagicMock):
        """Test AWS credentials check when no credentials are available."""
        mock_session.side_effect = NoCredentialsError()

        assert check_aws_credentials() is False

    @patch('automate_ui.common.utils.aws_secrets.boto3.Session')
    def test_check_aws_credentials_no_region(self, mock_session: MagicMock):
        """Test AWS credentials check when no region is configured."""
        mock_session.side_effect = NoRegionError()

        assert check_aws_credentials() is False

    @patch('automate_ui.common.utils.aws_secrets.boto3.Session')
    def test_check_aws_credentials_client_error(self, mock_session: MagicMock):
        """Test AWS credentials check when client error occurs."""
        mock_session_instance = Mock()
        mock_sts_client = Mock()
        mock_sts_client.get_caller_identity.side_effect = ClientError(
            {'Error': {'Code': 'AccessDenied', 'Message': 'Access Denied'}},
            'GetCallerIdentity'
        )
        mock_session_instance.client.return_value = mock_sts_client
        mock_session.return_value = mock_session_instance

        assert check_aws_credentials() is False


class TestAWSSecrets:
    """Test cases for AWS Secrets Manager functionality."""

    @patch('automate_ui.common.utils.aws_secrets.boto3.client')
    def test_get_secret_from_aws_success(self, mock_boto_client: MagicMock):
        """Test successful secret retrieval from AWS."""
        # Mock AWS Secrets Manager response
        mock_response = {
            'SecretString': json.dumps({
                'api': {
                    'public': {
                        'key': 'aws-api-key',
                        'base_url': 'https://aws-api.example.com'
                    }
                }
            })
        }

        mock_client = Mock()
        mock_client.get_secret_value.return_value = mock_response
        mock_boto_client.return_value = mock_client

        result = get_secret_from_aws('test-secret')

        assert result['api']['public']['key'] == 'aws-api-key'
        assert result['api']['public']['base_url'] == 'https://aws-api.example.com'
        mock_client.get_secret_value.assert_called_once_with(SecretId='test-secret')

    @patch('automate_ui.common.utils.aws_secrets.boto3.session.Session')
    def test_get_secret_from_aws_with_region(self, mock_session: MagicMock):
        """Test secret retrieval from AWS with specific region."""
        mock_response = {'SecretString': json.dumps({'test': 'value'})}
        mock_client = Mock()
        mock_client.get_secret_value.return_value = mock_response

        mock_session_instance = Mock()
        mock_session_instance.client.return_value = mock_client
        mock_session.return_value = mock_session_instance

        result = get_secret_from_aws('test-secret', 'us-east-1')

        # Verify the session was created and client was called
        mock_session.assert_called_once()
        mock_session_instance.client.assert_called_once_with(
            service_name='secretsmanager',
            region_name='us-east-1'
        )
        assert result == {'test': 'value'}

    @patch('automate_ui.common.utils.aws_secrets.boto3.client')
    def test_get_secret_from_aws_not_found(self, mock_boto_client: MagicMock):
        """Test secret retrieval when secret doesn't exist."""
        mock_client = Mock()
        mock_client.get_secret_value.side_effect = ClientError(
            {'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Secret not found'}},
            'GetSecretValue'
        )
        mock_boto_client.return_value = mock_client

        result = get_secret_from_aws('nonexistent-secret')

        assert result is None

    @patch('automate_ui.common.utils.aws_secrets.boto3.client')
    def test_get_secret_from_aws_access_denied(self, mock_boto_client: MagicMock):
        """Test secret retrieval when access is denied."""
        mock_client = Mock()
        mock_client.get_secret_value.side_effect = ClientError(
            {'Error': {'Code': 'AccessDeniedException', 'Message': 'Access denied'}},
            'GetSecretValue'
        )
        mock_boto_client.return_value = mock_client

        result = get_secret_from_aws('protected-secret')

        assert result is None

    @patch('automate_ui.common.utils.aws_secrets.boto3.client')
    def test_get_secret_from_aws_invalid_json(self, mock_boto_client: MagicMock):
        """Test secret retrieval when secret contains invalid JSON."""
        mock_response = {'SecretString': 'invalid-json-content'}
        mock_client = Mock()
        mock_client.get_secret_value.return_value = mock_response
        mock_boto_client.return_value = mock_client

        result = get_secret_from_aws('invalid-json-secret')

        assert result is None

    @patch('automate_ui.common.utils.aws_secrets.boto3.client')
    def test_get_secret_from_aws_binary_secret(self, mock_boto_client: MagicMock):
        """Test secret retrieval when secret is binary."""
        mock_response = {'SecretBinary': b'binary-secret-data'}
        mock_client = Mock()
        mock_client.get_secret_value.return_value = mock_response
        mock_boto_client.return_value = mock_client

        result = get_secret_from_aws('binary-secret')

        assert result == {'binary_secret': b'binary-secret-data'}


class TestConfigWithAWSFallback:
    """Test cases for configuration with AWS fallback."""

    def test_get_config_with_aws_fallback_aws_success(self):
        """Test successful configuration retrieval from AWS."""
        aws_config = {
            'api': {
                'public': {
                    'key': 'aws-api-key',
                    'base_url': 'https://aws-api.example.com'
                }
            }
        }

        with patch('automate_ui.common.utils.aws_secrets.check_aws_credentials', return_value=True), \
             patch('automate_ui.common.utils.aws_secrets.get_secret_from_aws', return_value=aws_config):

            result = get_config_with_aws_fallback('local_secrets.yaml', 'test-secret')

            assert result == aws_config

    def test_get_config_with_aws_fallback_yaml_fallback(self):
        """Test fallback to YAML file when AWS fails."""
        yaml_content = """
        api:
          public:
            key: "yaml-api-key"
            base_url: "https://yaml-api.example.com"
        """

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_file = f.name

        try:
            with patch('automate_ui.common.utils.aws_secrets.check_aws_credentials', return_value=True), \
                 patch('automate_ui.common.utils.aws_secrets.get_secret_from_aws', return_value=None):

                result = get_config_with_aws_fallback(temp_file, 'test-secret')

                assert result['api']['public']['key'] == 'yaml-api-key'
                assert result['api']['public']['base_url'] == 'https://yaml-api.example.com'
        finally:
            os.unlink(temp_file)

    def test_get_config_with_aws_fallback_no_aws_credentials(self):
        """Test fallback to YAML when AWS credentials not available."""
        yaml_content = """
        api:
          public:
            key: "yaml-api-key"
        """

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_file = f.name

        try:
            with patch('automate_ui.common.utils.aws_secrets.check_aws_credentials', return_value=False):
                result = get_config_with_aws_fallback(temp_file, 'test-secret')

                assert result['api']['public']['key'] == 'yaml-api-key'
        finally:
            os.unlink(temp_file)

    def test_get_config_with_aws_fallback_no_aws_secret_name(self):
        """Test fallback to YAML when no AWS secret name provided."""
        yaml_content = """
        api:
          public:
            key: "yaml-api-key"
        """

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_file = f.name

        try:
            with patch('automate_ui.common.utils.aws_secrets.check_aws_credentials', return_value=True):
                result = get_config_with_aws_fallback(temp_file)  # No AWS secret name

                assert result['api']['public']['key'] == 'yaml-api-key'
        finally:
            os.unlink(temp_file)

    def test_get_config_with_aws_fallback_both_fail(self):
        """Test error handling when both AWS and YAML fail."""
        with patch('automate_ui.common.utils.aws_secrets.check_aws_credentials', return_value=True), \
             patch('automate_ui.common.utils.aws_secrets.get_secret_from_aws', return_value=None):

            with pytest.raises(FileNotFoundError) as exc_info:
                get_config_with_aws_fallback('nonexistent.yaml', 'test-secret')

            assert "Configuration not available from AWS Secrets Manager or YAML file" in str(exc_info.value)


class TestNestedConfigValue:
    """Test cases for nested configuration value retrieval."""

    def test_get_nested_config_value_aws_success(self):
        """Test successful nested value retrieval from AWS."""
        aws_config = {
            'api': {
                'public': {
                    'key': 'aws-api-key'
                }
            }
        }

        with patch('automate_ui.common.utils.aws_secrets.get_config_with_aws_fallback', return_value=aws_config):
            result = get_nested_config_value('local_secrets.yaml', 'api.public.key', 'test-secret')

            assert result == 'aws-api-key'

    def test_get_nested_config_value_yaml_fallback(self):
        """Test nested value retrieval from YAML fallback."""
        yaml_content = """
        api:
          public:
            key: "yaml-api-key"
        """

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_file = f.name

        try:
            with patch('automate_ui.common.utils.aws_secrets.get_config_with_aws_fallback') as mock_get_config:
                mock_get_config.return_value = {'api': {'public': {'key': 'yaml-api-key'}}}

                result = get_nested_config_value(temp_file, 'api.public.key', 'test-secret')

                assert result == 'yaml-api-key'
        finally:
            os.unlink(temp_file)

    def test_get_nested_config_value_key_not_found(self):
        """Test error handling when nested key doesn't exist."""
        config = {'api': {'public': {'key': 'test-key'}}}

        with patch('automate_ui.common.utils.aws_secrets.get_config_with_aws_fallback', return_value=config):
            with pytest.raises(KeyError) as exc_info:
                get_nested_config_value('local_secrets.yaml', 'api.public.nonexistent', 'test-secret')

            assert "Key path 'api.public.nonexistent' not found" in str(exc_info.value)