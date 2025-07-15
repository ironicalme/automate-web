from typing import Any, Dict

import yaml


def load_yaml_config(file_path: str) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.

    Args:
        file_path: Path to the YAML configuration file

    Returns:
        Dictionary containing the configuration data

    Raises:
        FileNotFoundError: If the YAML file doesn't exist
        yaml.YAMLError: If the YAML file is malformed
    """
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file not found: {file_path}. "
            f"Please ensure the file exists and is accessible. "
            f"For local development, create a '{file_path}' file with your configuration."
        )
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file {file_path}: {e}")
    except PermissionError:
        raise PermissionError(
            f"Permission denied accessing configuration file: {file_path}"
        )
    except Exception as e:
        raise Exception(f"Unexpected error loading configuration file {file_path}: {e}")


def get_nested_value(config: Dict[str, Any], key_path: str) -> Any:
    """
    Get a nested value from a configuration dictionary using dot notation.

    Args:
        config: Configuration dictionary
        key_path: Dot-separated path to the value (e.g., 'api.public.key')

    Returns:
        The value at the specified path

    Raises:
        KeyError: If the key path doesn't exist in the configuration
    """
    keys = key_path.split(".")
    current = config

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            raise KeyError(f"Key path '{key_path}' not found in configuration")

    return current


def get_nested_value_safe(config: Dict[str, Any], key_path: str) -> Any:
    """
    Get a nested value from a configuration dictionary using dot notation with appropriate error handling.

    Args:
        config: Configuration dictionary
        key_path: Dot-separated path to the value (e.g., 'api.public.key')

    Returns:
        The value at the specified path

    Raises:
        KeyError: If the key path doesn't exist in the configuration with a descriptive message
    """
    try:
        return get_nested_value(config, key_path)
    except KeyError:
        raise KeyError(
            f"Configuration key '{key_path}' not found. Please check your configuration file."
        )
