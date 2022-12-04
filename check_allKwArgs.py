#!/usr/bin/env python3

# Import standard modules ...
import argparse
import ast

# Import my modules ...
try:
    import pyguymer3
except:
    raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

# ******************************************************************************

# Create argument parser and parse the arguments ...
parser = argparse.ArgumentParser(
       allow_abbrev = False,
        description = "Check keyword arguments in Python functions.",
    formatter_class = argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "dname",
    help = "the folder to check",
)
args = parser.parse_args()

# ******************************************************************************

# Initialize database ...
funcs = {}

# Loop over files in folder ...
for fname in pyguymer3.return_file_list(args.dname):
    # Skip files which are not Python scripts ...
    if not fname.endswith(".py"):
        continue

    # Load the Python script ...
    with open(fname, "rt", encoding = "utf-8") as fObj:
        src = fObj.read()

    # Parse the Python script ...
    tree = ast.parse(src)

    # Loop over bodies ...
    for body in tree.body:
        # Skip bodies which are not function definitions ...
        if not isinstance(body, ast.FunctionDef):
            continue

        # Find out how many positional and keyword arguments there are, and skip
        # if there aren't any ...
        nPosArgs = len(body.args.args)
        nKwArgs = len(body.args.defaults)
        if nPosArgs == 0:
            continue
        if nKwArgs == 0:
            continue

        # Loop over keyword arguments ...
        for iKwArg in range(nKwArgs):
            # Deduce index to positional argument ...
            iPosArg = nPosArgs - nKwArgs + iKwArg

            # Skip if this keyword argument is the positional argument check ...
            if body.args.args[iPosArg].arg in ("kwArgCheck",):
                continue

            # Add this function to the database ...
            if body.name not in funcs:
                funcs[body.name] = []

            # Append this keyword argument to the database ...
            funcs[body.name].append(body.args.args[iPosArg].arg)

# ******************************************************************************

# Loop over files in folder ...
for fname in pyguymer3.return_file_list(args.dname):
    # Skip files which are not Python scripts ...
    if not fname.endswith(".py"):
        continue

    # Load the Python script ...
    with open(fname, "rt", encoding = "utf-8") as fObj:
        src = fObj.read()

    # Parse the Python script ...
    tree = ast.parse(src)

    # Loop over bodies ...
    for body in tree.body:
        # Skip bodies which are not function definitions ...
        if not isinstance(body, ast.FunctionDef):
            continue

        # Loop over nodes in the body ...
        for node in ast.walk(body):
            # Skip this node if it is not a function call (or if it is a member
            # of a module) ...
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name):
                continue

            # Skip this function call if it is not in the database ...
            if node.func.id not in funcs:
                continue

            # Find all the keyword arguments that are passed ...
            keywords = []
            for keyword in node.keywords:
                keywords.append(keyword.arg)

            # Loop over keyword arguments that *should* be passed ...
            for keyword in funcs[node.func.id]:
                # Skip this keyword argument if it is passed ...
                if keyword in keywords:
                    continue

                # Print ...
                print(f"\"{fname}\" calls \"{node.func.id}()\" but does not pass \"{keyword}\"")
