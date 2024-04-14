"""
Shortcuts to develop and debug the package in a local test folder. Usage:

python conanrun.py [source|install|build|export|export-pkg|test]
"""

import os
import sys
import inspect
from argparse import ArgumentParser

from conan import ConanFile, conan_version

try:
    from conan.cli.cli import main as conan_main
except ImportError:
    from conans.conan import main as conan_main


sys.path.append(os.getcwd())

import conanfile
for _, ConanRecipe in inspect.getmembers(conanfile):
    if inspect.isclass(ConanRecipe) and ConanRecipe is not ConanFile and issubclass(ConanRecipe, ConanFile):
        break
else:
    raise Exception("No conan class found in conanfile found")


def run_conan(*args):

    parser = ArgumentParser()
    parser.add_argument("command", choices=("create", "source", "install", "build", "export", "export-pkg", "test"))
    parser.add_argument("--version", nargs="?", default=ConanRecipe.version)

    if conan_version.major < 2:
        parser.add_argument("--user", default=None)
        parser.add_argument("--channel", default=None)

    parsed_args, other_args = parser.parse_known_args(args)

    conan_args = [parsed_args.command]

    if parsed_args.command in ["create", "source", "install", "build", "export", "export-pkg"]:
        conan_args.append(".")

    if not parsed_args.version:
        raise Exception("No version specified")

    user_channel = f"{parsed_args.user}/{parsed_args.channel}" if (parsed_args.user and parsed_args.channel) else ""
    reference = f"{ConanRecipe.name}/{parsed_args.version}@{user_channel}"

    if conan_version.major >= 2:
        if parsed_args.command == "test":
            conan_args.extend([
                "test_package",
                reference
            ])
    else:
        if parsed_args.command in ["create", "install", "export", "export-pkg"]:
            conan_args.append(reference)
        elif parsed_args.command == "test":
            conan_args.extend(["test_package", reference])

    conan_args.extend(other_args)

    print(f"Executing `conan {' '.join(conan_args)}`")
    conan_main(conan_args)

if __name__ == '__main__':
    run_conan(*sys.argv[1:])
