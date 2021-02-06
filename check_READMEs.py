#!/usr/bin/env python3

# Import standard modules ...
import glob
import json
import os

# Import my modules ...
try:
    import pyguymer3
except:
    raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

# Load list of standard modules ...
standardModules = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Python 3.7 Standard Modules.json"), "rt"))

# Append common non-standard modules that I do not want to be warned about ...
standardModules.append("funcs")
standardModules.append("web_mod")

# Loop over READMEs ...
for rname in sorted(glob.glob("*/README.md")):
    print(f"Checking \"{rname}\" ...")

    # Deduce directory name ...
    dname = os.path.dirname(rname)

    # **************************************************************************

    # Initialize list of sub-paths to ignore ...
    ipaths = [
        os.path.join(dname, ".git"),
        os.path.join(dname, "build"),
    ]

    # Deduce .gitmodules file name, check if it exists and populate list with
    # paths to ignore if it does ...
    mname = os.path.join(dname, ".gitmodules")
    if os.path.exists(mname):
        for line in open(mname, "rt"):
            if not line.strip().startswith("path = "):
                continue
            ipaths.append(os.path.join(dname, "=".join(line.strip().split("=")[1:]).strip()))

    # **************************************************************************

    # Initialize list of imported non-standard modules ...
    modules = []

    # Loop over files in directory ...
    for pname in pyguymer3.return_file_list(dname):
        # Skip if the file is not a Python script ...
        if not pname.endswith(".py"):
            continue

        # Skip if the file is in a directory which is to be ignored ...
        ignore = False
        for ipath in ipaths:
            if pname.startswith(ipath):
                ignore = True
                break
        if ignore:
            continue

        # Find all the non-standard modules which are imported and append the
        # missing ones to the list ...
        for line in open(pname, "rt"):
            if not line.strip().startswith("import "):
                continue
            module = line.strip().split(" ")[1].split(".")[0]
            if module in standardModules:
                continue
            if module in modules:
                continue
            modules.append(module)

    # Skip this README if the repository does not import any non-standard
    # modules ...
    if len(modules) == 0:
        continue

    # **************************************************************************

    # Load README ...
    lines = open(rname, "rt").readlines()

    # Loop over imported non-standard modules ...
    for module in sorted(modules):
        linked = False
        for line in lines:
            if line.strip().startswith(f"* [{module}]("):
                linked = True
                break
        if linked:
            continue
        print(f"  ... needs a link adding for \"{module}\"")
