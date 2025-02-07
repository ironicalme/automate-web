import subprocess
import sys


def install_pip_tools():
    """Ensures pip-tools is installed before dependency management."""
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip-tools"], check=True)


def install_requirements():
    """Installs dependencies from pyproject.toml (requires pip-tools for parsing)."""
    print("Installing other dependencies from pyproject.toml...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)


if __name__ == "__main__":
    install_pip_tools()
    install_requirements()
