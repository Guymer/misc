#!/usr/bin/env python3

# Define function ...
def checkAddArgument(nodeIn, fnameIn, /):
    """
    Check that all "parser.add_argument()" calls specify the type.
    """

    # Skip this node if it is not a function call (or if it is not an attribute
    # call) ...
    if not isinstance(nodeIn, ast.Call):
        return
    if not isinstance(nodeIn.func, ast.Attribute):
        return

    # Skip this node if it is not a "parser.add_argument()" call ...
    if nodeIn.func.attr != "add_argument":
        return
    if nodeIn.func.value.id != "parser":
        return

    # Skip this node if it is a Boolean flag ...
    skip = False
    for keyword in nodeIn.keywords:
        if keyword.arg == "action":
            if keyword.value.value in ["store_false", "store_true"]:
                skip = True
                break
    if skip:
        return

    # Skip this node if it sets the argument type ...
    skip = False
    for keyword in nodeIn.keywords:
        if keyword.arg == "type":
            skip = True
            break
    if skip:
        return

    # Print ...
    print(f"\"{fnameIn}\" adds the argument \"{nodeIn.args[0].value}\" without specifying the type.")

# Define function ...
def checkLegend(nodeIn, fnameIn, /):
    """
    Check that all "ax*.legend()" calls specify the location.
    """

    # Skip this node if it is not a function call (or if it is not an attribute
    # call) ...
    if not isinstance(nodeIn, ast.Call):
        return
    if not isinstance(nodeIn.func, ast.Attribute):
        return

    # Skip this node if it is not a "ax.legend()" call ...
    if nodeIn.func.attr != "legend":
        return
    if not nodeIn.func.value.id.startswith("ax"):
        return

    # Skip this node if it sets the location ...
    skip = False
    for keyword in nodeIn.keywords:
        if keyword.arg == "loc":
            skip = True
            break
    if skip:
        return

    # Print ...
    print(f"\"{fnameIn}\" adds a legend to \"{nodeIn.func.value.id}\" without specifying the location.")

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.11/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import argparse
    import ast

    # Import my modules ...
    try:
        import pyguymer3
    except:
        raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

    # **************************************************************************

    # Create argument parser and parse the arguments ...
    parser = argparse.ArgumentParser(
           allow_abbrev = False,
            description = "Check command line arguments in Python scripts.",
        formatter_class = argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "dname",
        help = "the folder to check",
        type = str,
    )
    args = parser.parse_args()

    # **************************************************************************

    # Initialize database ...
    funcs = {}

    # Loop over files in folder ...
    for fname in pyguymer3.return_file_list(args.dname):
        # Skip files which are not Python scripts ...
        if not fname.endswith(".py"):
            continue

        # Skip Python scripts which are known Git submodules ...
        if "/openflights/" in fname:
            continue
        if "/stations/" in fname:
            continue
        if "/validator/" in fname:
            continue

        # Load the Python script ...
        with open(fname, "rt", encoding = "utf-8") as fObj:
            src = fObj.read()

        # Parse the Python script ...
        tree = ast.parse(src)

        # Loop over bodies ...
        for body in tree.body:
            # Loop over nodes in the body ...
            for node in ast.walk(body):
                # Check everything ...
                checkAddArgument(node, fname)
                checkLegend(node, fname)
