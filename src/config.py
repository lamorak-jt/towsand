"""Credential and configuration management for Towsand.

Stores sensitive values (IB token, query IDs) in ~/.config/towsand/credentials
with restricted file permissions (0600). Supports environment variable overrides.

Lookup order for any key:
  1. Environment variable  TOWSAND_<UPPER_KEY>  (e.g. TOWSAND_IB_TOKEN)
  2. Credentials file      ~/.config/towsand/credentials
"""

import configparser
import os
import stat
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "towsand"
CREDENTIALS_FILE = CONFIG_DIR / "credentials"

ENV_PREFIX = "TOWSAND_"

# Known credential keys and their descriptions
KNOWN_KEYS = {
    "ib_token": "Interactive Brokers Flex Web Service token",
    "ib_query_id": "Interactive Brokers Flex Query ID",
}


def _ensure_config_dir() -> None:
    """Create the config directory if it doesn't exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def _read_credentials() -> configparser.ConfigParser:
    """Read the credentials file. Returns an empty config if file doesn't exist."""
    config = configparser.ConfigParser()
    if CREDENTIALS_FILE.exists():
        config.read(CREDENTIALS_FILE)
    if not config.has_section("credentials"):
        config.add_section("credentials")
    return config


def _write_credentials(config: configparser.ConfigParser) -> None:
    """Write the credentials file with restricted permissions (owner read/write only)."""
    _ensure_config_dir()
    with open(CREDENTIALS_FILE, "w") as f:
        config.write(f)
    CREDENTIALS_FILE.chmod(stat.S_IRUSR | stat.S_IWUSR)


def get(key: str) -> str | None:
    """Get a credential value. Checks env var first, then credentials file.

    Args:
        key: The credential key (e.g. 'ib_token').

    Returns:
        The value, or None if not set anywhere.
    """
    env_key = f"{ENV_PREFIX}{key.upper()}"
    env_val = os.environ.get(env_key)
    if env_val:
        return env_val

    config = _read_credentials()
    val = config.get("credentials", key, fallback=None)
    return val if val else None


def set_value(key: str, value: str) -> None:
    """Store a credential value in the credentials file."""
    config = _read_credentials()
    config.set("credentials", key, value)
    _write_credentials(config)


def delete(key: str) -> bool:
    """Remove a credential from the credentials file. Returns True if it existed."""
    config = _read_credentials()
    existed = config.remove_option("credentials", key)
    if existed:
        _write_credentials(config)
    return existed


def list_all() -> dict[str, str]:
    """List all stored credentials (from file only, not env vars).

    Returns dict of key → value (values are masked for display safety).
    """
    config = _read_credentials()
    return dict(config.items("credentials"))


def resolve_ib_token(cli_token: str | None = None) -> str | None:
    """Resolve the IB token from CLI flag → env var → credentials file."""
    if cli_token:
        return cli_token
    return get("ib_token")


def resolve_ib_query_id(cli_query_id: str | None = None) -> str | None:
    """Resolve the IB query ID from CLI flag → env var → credentials file."""
    if cli_query_id:
        return cli_query_id
    return get("ib_query_id")
