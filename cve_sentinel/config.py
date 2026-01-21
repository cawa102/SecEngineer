"""Configuration management for CVE Sentinel."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml


class ConfigError(Exception):
    """Configuration error."""

    pass


class ConfigValidationError(ConfigError):
    """Configuration validation error."""

    pass


@dataclass
class Config:
    """CVE Sentinel configuration.

    Attributes:
        target_path: Directory to scan for dependencies.
        exclude: List of path patterns to exclude from scanning.
        analysis_level: Depth of analysis (1-3).
            1: Direct dependencies from manifest files
            2: Transitive dependencies from lock files
            3: Import statement scanning in source code
        auto_scan_on_startup: Whether to automatically scan on startup.
        cache_ttl_hours: Cache time-to-live in hours.
        nvd_api_key: NVD API key for vulnerability data.
    """

    target_path: Path = field(default_factory=lambda: Path("."))
    exclude: list[str] = field(
        default_factory=lambda: ["node_modules/", "vendor/", ".git/", "__pycache__/", "venv/"]
    )
    analysis_level: int = 3
    auto_scan_on_startup: bool = True
    cache_ttl_hours: int = 24
    nvd_api_key: Optional[str] = None

    def __post_init__(self) -> None:
        """Convert target_path to Path if string."""
        if isinstance(self.target_path, str):
            self.target_path = Path(self.target_path)


def _find_config_file(base_path: Path) -> Optional[Path]:
    """Find configuration file in the given directory.

    Searches for .cve-sentinel.yaml first, then .cve-sentinel.yml.

    Args:
        base_path: Directory to search in.

    Returns:
        Path to config file if found, None otherwise.
    """
    yaml_path = base_path / ".cve-sentinel.yaml"
    if yaml_path.exists():
        return yaml_path

    yml_path = base_path / ".cve-sentinel.yml"
    if yml_path.exists():
        return yml_path

    return None


def _load_yaml_config(config_path: Path) -> dict[str, Any]:
    """Load configuration from YAML file.

    Args:
        config_path: Path to the YAML config file.

    Returns:
        Dictionary with configuration values.

    Raises:
        ConfigError: If file cannot be read or parsed.
    """
    try:
        with open(config_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if data is not None else {}
    except yaml.YAMLError as e:
        raise ConfigError(f"Failed to parse YAML config file: {e}") from e
    except OSError as e:
        raise ConfigError(f"Failed to read config file: {e}") from e


def _load_env_vars() -> dict[str, Any]:
    """Load configuration from environment variables.

    Supported environment variables:
        - CVE_SENTINEL_NVD_API_KEY: NVD API key
        - CVE_SENTINEL_CONFIG_PATH: Custom config file path

    Returns:
        Dictionary with configuration values from environment.
    """
    env_config: dict[str, Any] = {}

    nvd_api_key = os.environ.get("CVE_SENTINEL_NVD_API_KEY")
    if nvd_api_key:
        env_config["nvd_api_key"] = nvd_api_key

    return env_config


def _get_config_path_from_env() -> Optional[Path]:
    """Get custom config file path from environment variable.

    Returns:
        Path to config file if CVE_SENTINEL_CONFIG_PATH is set, None otherwise.
    """
    config_path_str = os.environ.get("CVE_SENTINEL_CONFIG_PATH")
    if config_path_str:
        return Path(config_path_str)
    return None


def _validate_config(config: Config) -> None:
    """Validate configuration values.

    Args:
        config: Configuration to validate.

    Raises:
        ConfigValidationError: If validation fails.
    """
    errors: list[str] = []

    # Validate analysis_level (1-3)
    if not 1 <= config.analysis_level <= 3:
        errors.append(f"analysis_level must be between 1 and 3, got {config.analysis_level}")

    # Validate cache_ttl_hours (positive integer)
    if config.cache_ttl_hours <= 0:
        errors.append(f"cache_ttl_hours must be positive, got {config.cache_ttl_hours}")

    # Validate target_path exists
    if not config.target_path.exists():
        errors.append(f"target_path does not exist: {config.target_path}")

    # NVD API key is required for full functionality
    if not config.nvd_api_key:
        errors.append(
            "nvd_api_key is required. Set CVE_SENTINEL_NVD_API_KEY environment variable "
            "or add nvd_api_key to .cve-sentinel.yaml"
        )

    if errors:
        raise ConfigValidationError("\n".join(errors))


def load_config(
    base_path: Optional[Path] = None,
    validate: bool = True,
    require_api_key: bool = True,
    cli_overrides: Optional[dict[str, Any]] = None,
) -> Config:
    """Load configuration from file, environment variables, and CLI arguments.

    Configuration is loaded in the following order (later values override earlier):
    1. Default values
    2. YAML config file (.cve-sentinel.yaml or .cve-sentinel.yml)
    3. Environment variables
    4. CLI arguments (highest priority)

    Args:
        base_path: Base directory to search for config file.
            Defaults to current working directory.
        validate: Whether to validate the configuration.
        require_api_key: Whether to require NVD API key in validation.
        cli_overrides: Dictionary of CLI argument overrides (highest priority).

    Returns:
        Loaded and optionally validated Config object.

    Raises:
        ConfigError: If config file cannot be read or parsed.
        ConfigValidationError: If validation is enabled and fails.
    """
    if base_path is None:
        base_path = Path.cwd()

    # Start with defaults
    config_data: dict[str, Any] = {}

    # Check for custom config path from environment
    env_config_path = _get_config_path_from_env()
    if env_config_path:
        if env_config_path.exists():
            config_data.update(_load_yaml_config(env_config_path))
        else:
            raise ConfigError(
                f"Config file specified by CVE_SENTINEL_CONFIG_PATH does not exist: "
                f"{env_config_path}"
            )
    else:
        # Find config file in base_path
        config_path = _find_config_file(base_path)
        if config_path:
            config_data.update(_load_yaml_config(config_path))

    # Override with environment variables
    config_data.update(_load_env_vars())

    # Override with CLI arguments (highest priority)
    if cli_overrides:
        config_data.update(cli_overrides)

    # Convert target_path to absolute path relative to base_path
    if "target_path" in config_data:
        target = Path(config_data["target_path"])
        if not target.is_absolute():
            config_data["target_path"] = base_path / target
    else:
        config_data["target_path"] = base_path

    # Create Config object
    config = Config(**config_data)

    # Validate if requested
    if validate:
        if not require_api_key and not config.nvd_api_key:
            # Skip API key validation but validate other fields
            errors: list[str] = []
            if not 1 <= config.analysis_level <= 3:
                errors.append(
                    f"analysis_level must be between 1 and 3, got {config.analysis_level}"
                )
            if config.cache_ttl_hours <= 0:
                errors.append(f"cache_ttl_hours must be positive, got {config.cache_ttl_hours}")
            if not config.target_path.exists():
                errors.append(f"target_path does not exist: {config.target_path}")
            if errors:
                raise ConfigValidationError("\n".join(errors))
        else:
            _validate_config(config)

    return config


def get_default_config() -> Config:
    """Get default configuration without loading from file.

    Returns:
        Config object with default values.
    """
    return Config()
