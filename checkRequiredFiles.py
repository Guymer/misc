#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.12/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import argparse
    import glob
    import os
    import shutil
    import subprocess

    # Import my modules ...
    try:
        import pyguymer3
    except:
        raise Exception("\"pyguymer3\" is not installed; run \"pip install --user PyGuymer3\"") from None

    # **************************************************************************

    # Create argument parser and parse the arguments ...
    parser = argparse.ArgumentParser(
           allow_abbrev = False,
            description = "Add required files to GitHub repositories.",
        formatter_class = argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--timeout",
        default = 60.0,
           help = "the timeout for any requests/subprocess calls (in seconds)",
           type = float,
    )
    args = parser.parse_args()

    # **************************************************************************

    # Loop over Git repositories ...
    for gName in sorted(glob.glob("*/.git")):
        # Skip this Git repository if it is a submodule ...
        if not os.path.isdir(gName):
            continue

        # Create short-hands ...
        dName = os.path.dirname(gName)
        onGist = pyguymer3.git_remote(
            dName,
            timeout = args.timeout,
        ).startswith("git@gist.github.com:")
        onGitHub = pyguymer3.git_remote(
            dName,
            timeout = args.timeout,
        ).startswith("git@github.com:")

        # Find all files in the Git repository ...
        gFiles = pyguymer3.git_files(
            dName,
            timeout = args.timeout,
        )

        # Check that the basic required files are present ...
        requiredFiles = [
            ".editorconfig",
            ".gitignore",
            ".mypy.ini",
            ".pylint.ini",
            ".shellcheckrc",
            "README.md",
            "requirements.txt",
        ]
        if onGist or onGitHub:
            requiredFiles += [
                ".github/FUNDING.yml",
                "LICENCE.txt",
            ]
        for gFile in requiredFiles:
            if gFile in gFiles:
                continue
            if onGist and "/" in gFile: # NOTE: Gist cannot handle sub-folders.
                continue
            print(f"\"{dName}/{gFile}\" is missing.")
            shutil.copy(
                f"{os.path.dirname(os.path.realpath(__file__))}/{gFile}",
                f"{dName}/{gFile}",
            )
            subprocess.run(
                ["git", "add", "--intent-to-add", gFile],
                   check = True,
                     cwd = dName,
                encoding = "utf-8",
                  stderr = subprocess.DEVNULL,
                  stdout = subprocess.DEVNULL,
                 timeout = args.timeout,
            )

        # Skip Git repository if it is not published on GitHub ...
        if not onGitHub:
            continue

        # Determine if it has any BASH scripts and check that the required
        # GitHub Action workflow YAML file is present ...
        hasBash = False
        for gFile in gFiles:
            if gFile.endswith(".sh"):
                hasBash = True
                break
        if hasBash and ".github/workflows/shellcheck.yaml" not in gFiles:
            print(f"\"{dName}/.github/workflows/shellcheck.yaml\" is missing.")
            shutil.copy(
                f"{os.path.dirname(os.path.realpath(__file__))}/.github/workflows/shellcheck.yaml",
                f"{dName}/.github/workflows/shellcheck.yaml",
            )
            subprocess.run(
                ["git", "add", "--intent-to-add", ".github/workflows/shellcheck.yaml"],
                   check = True,
                     cwd = dName,
                encoding = "utf-8",
                  stderr = subprocess.DEVNULL,
                  stdout = subprocess.DEVNULL,
                 timeout = args.timeout,
            )
        if not hasBash and ".github/workflows/shellcheck.yaml" in gFiles:
            print(f"\"{dName}/.github/workflows/shellcheck.yaml\" is present but shouldn't be.")

        # Determine if it has any FORTRAN programs and check that the required
        # GitHub Action workflow YAML file is present ...
        hasFortran = False
        for gFile in gFiles:
            if gFile.endswith(".f90") or gFile.endswith(".F90"):
                hasFortran = True
                break
        if hasFortran and ".github/workflows/gmake.yaml" not in gFiles:
            print(f"\"{dName}/.github/workflows/gmake.yaml\" is missing.")
            shutil.copy(
                f"{os.path.dirname(os.path.realpath(__file__))}/.github/workflows/gmake.yaml",
                f"{dName}/.github/workflows/gmake.yaml",
            )
            subprocess.run(
                ["git", "add", "--intent-to-add", ".github/workflows/gmake.yaml"],
                   check = True,
                     cwd = dName,
                encoding = "utf-8",
                  stderr = subprocess.DEVNULL,
                  stdout = subprocess.DEVNULL,
                 timeout = args.timeout,
            )
        if not hasFortran and ".github/workflows/gmake.yaml" in gFiles:
            print(f"\"{dName}/.github/workflows/gmake.yaml\" is present but shouldn't be.")

        # Determine if it has any Python scripts and check that the required
        # GitHub Action workflow YAML file is present ...
        hasPython = False
        for gFile in gFiles:
            if gFile.endswith(".py"):
                hasPython = True
                break
        if hasPython and ".github/workflows/mypy.yaml" not in gFiles:
            print(f"\"{dName}/.github/workflows/mypy.yaml\" is missing.")
            shutil.copy(
                f"{os.path.dirname(os.path.realpath(__file__))}/.github/workflows/mypy.yaml",
                f"{dName}/.github/workflows/mypy.yaml",
            )
            subprocess.run(
                ["git", "add", "--intent-to-add", ".github/workflows/mypy.yaml"],
                   check = True,
                     cwd = dName,
                encoding = "utf-8",
                  stderr = subprocess.DEVNULL,
                  stdout = subprocess.DEVNULL,
                 timeout = args.timeout,
            )
        if not hasPython and ".github/workflows/mypy.yaml" in gFiles:
            print(f"\"{dName}/.github/workflows/mypy.yaml\" is present but shouldn't be.")

        # Determine if it has any Python scripts and check that the required
        # GitHub Action workflow YAML file is present ...
        hasPython = False
        for gFile in gFiles:
            if gFile.endswith(".py"):
                hasPython = True
                break
        if hasPython and ".github/workflows/pylint.yaml" not in gFiles:
            print(f"\"{dName}/.github/workflows/pylint.yaml\" is missing.")
            shutil.copy(
                f"{os.path.dirname(os.path.realpath(__file__))}/.github/workflows/pylint.yaml",
                f"{dName}/.github/workflows/pylint.yaml",
            )
            subprocess.run(
                ["git", "add", "--intent-to-add", ".github/workflows/pylint.yaml"],
                   check = True,
                     cwd = dName,
                encoding = "utf-8",
                  stderr = subprocess.DEVNULL,
                  stdout = subprocess.DEVNULL,
                 timeout = args.timeout,
            )
        if not hasPython and ".github/workflows/pylint.yaml" in gFiles:
            print(f"\"{dName}/.github/workflows/pylint.yaml\" is present but shouldn't be.")
