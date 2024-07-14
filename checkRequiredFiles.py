#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.11/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import glob
    import os

    # Import my modules ...
    try:
        import pyguymer3
    except:
        raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

    # **************************************************************************

    # Loop over Git repositories ...
    for gName in sorted(glob.glob("*/.git")):
        # Skip this Git repository if it is a submodule ...
        if not os.path.isdir(gName):
            continue

        # Create short-hand ...
        dName = os.path.dirname(gName)

        # Skip this Git repository if it isn't on GitHub ...
        if not pyguymer3.git_remote(dName).startswith("git@github.com:"):
            continue

        # Find all files in the Git repository ...
        gFiles = pyguymer3.git_files(dName)

        # Check that the basic required files are present ...
        for gFile in [
            ".editorconfig",
            ".github/FUNDING.yml",
            ".gitignore",
            ".pylintrc",
            ".shellcheckrc",
            ".vscode/settings.json",
            "LICENCE.txt",
            "README.md",
            "requirements.txt",
        ]:
            if gFile in gFiles:
                continue
            print(f"\"{dName}/{gFile}\" is missing.")

        # Determine if it has any BASH scripts and check that the required
        # GitHub Action workflow YAML file is present ...
        hasBash = False
        for gFile in gFiles:
            if gFile.endswith(".sh"):
                hasBash = True
                break
        if hasBash and ".github/workflows/shellcheck.yml" not in gFiles:
            print(f"\"{dName}/.github/workflows/shellcheck.yml\" is missing.")
        if not hasBash and ".github/workflows/shellcheck.yml" in gFiles:
            print(f"\"{dName}/.github/workflows/shellcheck.yml\" is present but shouldn't be.")

        # Determine if it has any FORTRAN programs and check that the required
        # GitHub Action workflow YAML file is present ...
        hasFortran = False
        for gFile in gFiles:
            if gFile.endswith(".f90") or gFile.endswith(".F90"):
                hasFortran = True
                break
        if hasFortran and ".github/workflows/gmake.yml" not in gFiles:
            print(f"\"{dName}/.github/workflows/gmake.yml\" is missing.")
        if not hasFortran and ".github/workflows/gmake.yml" in gFiles:
            print(f"\"{dName}/.github/workflows/gmake.yml\" is present but shouldn't be.")

        # Determine if it has any Python scripts and check that the required
        # GitHub Action workflow YAML file is present ...
        hasPython = False
        for gFile in gFiles:
            if gFile.endswith(".py"):
                hasPython = True
                break
        if hasPython and ".github/workflows/pylint.yml" not in gFiles:
            print(f"\"{dName}/.github/workflows/pylint.yml\" is missing.")
        if not hasPython and ".github/workflows/pylint.yml" in gFiles:
            print(f"\"{dName}/.github/workflows/pylint.yml\" is present but shouldn't be.")
