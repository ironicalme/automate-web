#!/usr/bin/env python3
# type: ignore
# flake8: noqa
# pylint: disable=import-outside-toplevel  # Intentional for compatibility


import subprocess
import sys

SRC = "automate_ui"
TEST_SRC = "tests"


def is_platform_linux() -> bool:
    import platform

    return platform.system() in ("Linux", "Darwin")

def is_venv_present() -> bool:
    import pathlib

    if not pathlib.Path("venv").is_dir():
        print(
            "Virtual Environment not setup; please run `python make.py venv`",
            file=sys.stderr,
        )
        sys.exit(1)

def make_venv():
    if is_platform_linux():
        subprocess.run(["make", "venv"], check=True)
    else:
        import venv

        pip_install = [".\\venv\\Scripts\\python.exe", "-m", "pip", "install"]
        venv.main(["venv"])
        subprocess.run([*pip_install, "-U", "setuptools", "wheel", "pip==23.2.1"], check=True)
        subprocess.run([*pip_install, "-e", ".[dev]"], check=True)

def format():
    is_venv_present()
    if is_platform_linux():
        subprocess.run(["make", "format"], check=True)
    else:
        subprocess.run([".\\venv\\Scripts\\isort", SRC, TEST_SRC], check=True)
        subprocess.run([".\\venv\\Scripts\\black", SRC, TEST_SRC], check=True)

def lint():
    is_venv_present()
    if is_platform_linux():
        subprocess.run(["make", "lint"], check=True)
    else:
        subprocess.run([".\\venv\\Scripts\\mypy", SRC, TEST_SRC], check=True)
        subprocess.run([".\\venv\\Scripts\\flake8", SRC, TEST_SRC], check=True)
        subprocess.run([".\\venv\\Scripts\\pylint", SRC, TEST_SRC], check=True)
        subprocess.run(
            [".\\venv\\Scripts\\black", "--check", SRC, TEST_SRC], check=True
        )
        subprocess.run(
            [".\\venv\\Scripts\\isort", "--check", SRC, TEST_SRC], check=True
        )


def run_tests(pytest_args):
    is_venv_present()
    if pytest_args is None:
        pytest_args = []
    if is_platform_linux():
        subprocess.run(
            ["make", "test", f'TEST_ARGS="{" ".join(pytest_args)}"'], check=True
        )
    else:
        subprocess.run(
            [
                ".\\venv\\Scripts\\pytest",
                "-svv",
                TEST_SRC,
                *pytest_args,
            ],
            check=True,
        )

COMMANDS = {
    "venv": make_venv,
    "format": format,
    "lint": lint,
    "test": run_tests,
}

if __name__ == "__main__":
    import argparse

    version = sys.version_info[:3]
    if not ((3, 11, 0) <= version <= (3, 12, 0)):
        print(
            "This project requires Python 3.11 or 3.12 to run (currently {}".format(
                sys.version
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")
    venv_parser = subparsers.add_parser("venv")
    format_parser = subparsers.add_parser("format")
    lint_parser = subparsers.add_parser("lint")
    test_parser = subparsers.add_parser("test")
    test_parser.add_argument(
        "--pytest-args",
        nargs=argparse.REMAINDER,
        help="Additional arguments to pass to pytest",
    )

    args = parser.parse_args()
    dict_args = vars(args)

    if args.cmd is None:
        parser.print_help()
        sys.exit()

    COMMANDS[dict_args.pop("cmd")](**dict_args)
