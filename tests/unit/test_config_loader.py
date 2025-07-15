import os
import tempfile
from unittest.mock import patch

import pytest

from automate_ui.common.utils.config_loader import get_nested_value
from automate_ui.common.utils.config_loader import get_nested_value_safe
from automate_ui.common.utils.config_loader import load_yaml_config


class TestConfigLoader:
    """Test cases for the config loader functionality."""

    def test_load_yaml_config_success(self):
        """Test successful loading of YAML configuration."""
        yaml_content = """
        api:
          public:
            key: "test-api-key"
            base_url: "https://api.example.com"
        database:
          host: "localhost"
          port: 5432
        """

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            temp_file = f.name

        try:
            config = load_yaml_config(temp_file)
            assert config["api"]["public"]["key"] == "test-api-key"
            assert config["api"]["public"]["base_url"] == "https://api.example.com"
            assert config["database"]["host"] == "localhost"
            assert config["database"]["port"] == 5432
        finally:
            os.unlink(temp_file)

    def test_load_yaml_config_file_not_found(self):
        """Test error handling when YAML file doesn't exist."""
        with pytest.raises(FileNotFoundError) as exc_info:
            load_yaml_config("nonexistent_file.yaml")

        assert "Configuration file not found" in str(exc_info.value)
        assert "Please ensure the file exists" in str(exc_info.value)

    def test_load_yaml_config_invalid_yaml(self):
        """Test error handling when YAML file is malformed."""
        invalid_yaml = """
        api:
          public:
            key: "test-api-key"
            base_url: "https://api.example.com"
        database:
          host: "localhost"
          port: 5432
        invalid: yaml: content: here
        """

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(invalid_yaml)
            temp_file = f.name

        try:
            with pytest.raises(Exception) as exc_info:
                load_yaml_config(temp_file)
            assert "Error parsing YAML file" in str(exc_info.value)
        finally:
            os.unlink(temp_file)

    def test_load_yaml_config_permission_error(self):
        """Test error handling when file access is denied."""
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError) as exc_info:
                load_yaml_config("test.yaml")
            assert "Permission denied accessing configuration file" in str(
                exc_info.value
            )

    def test_get_nested_value_success(self):
        """Test successful retrieval of nested values."""
        config = {
            "api": {
                "public": {
                    "key": "test-api-key",
                    "base_url": "https://api.example.com",
                },
                "private": {"admin_key": "admin-key"},
            },
            "database": {"host": "localhost", "port": 5432},
        }

        assert get_nested_value(config, "api.public.key") == "test-api-key"
        assert (
            get_nested_value(config, "api.public.base_url") == "https://api.example.com"
        )
        assert get_nested_value(config, "api.private.admin_key") == "admin-key"
        assert get_nested_value(config, "database.host") == "localhost"
        assert get_nested_value(config, "database.port") == 5432

    def test_get_nested_value_key_not_found(self):
        """Test error handling when nested key doesn't exist."""
        config = {"api": {"public": {"key": "test-api-key"}}}

        with pytest.raises(KeyError) as exc_info:
            get_nested_value(config, "api.public.nonexistent")
        assert "Key path 'api.public.nonexistent' not found" in str(exc_info.value)

        with pytest.raises(KeyError) as exc_info:
            get_nested_value(config, "nonexistent.key")
        assert "Key path 'nonexistent.key' not found" in str(exc_info.value)

    def test_get_nested_value_partial_path(self):
        """Test error handling when partial path exists but final key doesn't."""
        config = {"api": {"public": {"key": "test-api-key"}}}

        with pytest.raises(KeyError) as exc_info:
            get_nested_value(config, "api.public.key.nonexistent")
        assert "Key path 'api.public.key.nonexistent' not found" in str(exc_info.value)

    def test_get_nested_value_safe_success(self):
        """Test successful retrieval using safe method."""
        config = {"api": {"public": {"key": "test-api-key"}}}

        assert get_nested_value_safe(config, "api.public.key") == "test-api-key"

    def test_get_nested_value_safe_key_not_found(self):
        """Test error handling in safe method when key doesn't exist."""
        config = {"api": {"public": {"key": "test-api-key"}}}

        with pytest.raises(KeyError) as exc_info:
            get_nested_value_safe(config, "api.public.nonexistent")
        assert "Configuration key 'api.public.nonexistent' not found" in str(
            exc_info.value
        )
        assert "Please check your configuration file" in str(exc_info.value)

    def test_get_nested_value_with_empty_config(self):
        """Test behavior with empty configuration."""
        config = {}

        with pytest.raises(KeyError) as exc_info:
            get_nested_value(config, "any.key")
        assert "Key path 'any.key' not found" in str(exc_info.value)

    def test_get_nested_value_with_none_config(self):
        """Test behavior with None configuration."""
        config = None

        with pytest.raises(KeyError) as exc_info:
            get_nested_value(config, "any.key")
        assert "Key path 'any.key' not found" in str(exc_info.value)

    def test_get_nested_value_with_non_dict_intermediate(self):
        """Test behavior when intermediate value is not a dictionary."""
        config = {"api": {"public": "not-a-dict"}}

        with pytest.raises(KeyError) as exc_info:
            get_nested_value(config, "api.public.key")
        assert "Key path 'api.public.key' not found" in str(exc_info.value)
