#!/usr/bin/env python3

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

        # Load the Python script ...
        with open(fname, "rt", encoding = "utf-8") as fObj:
            src = fObj.read()

        # Parse the Python script ...
        tree = ast.parse(src)

        # Loop over bodies ...
        for body in tree.body:
            # Loop over nodes in the body ...
            for node in ast.walk(body):
                # Skip this node if it is not a function call (or if it is not
                # an attribute call) ...
                if not isinstance(node, ast.Call):
                    continue
                if not isinstance(node.func, ast.Attribute):
                    continue

                # Skip this node if it is not a "parser.add_argument()" call ...
                if node.func.attr != "add_argument":
                    continue
                if node.func.value.id != "parser":
                    continue

                # Skip this node if it is a Boolean flag ...
                skip = False
                for keyword in node.keywords:
                    if keyword.arg == "action":
                        if keyword.value.value in ["store_false", "store_true"]:
                            skip = True
                            break
                if skip:
                    continue

                # Skip this node if it sets the argument type ...
                skip = False
                for keyword in node.keywords:
                    if keyword.arg == "type":
                        skip = True
                        break
                if skip:
                    continue

                # Print ...
                print(f"\"{fname}\" adds the argument \"{node.args[0].value}\" without specifying the type.")
