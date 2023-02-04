#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.10/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
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
            description = "Check keyword-only arguments in Python functions.",
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
            # Skip bodies which are not function definitions ...
            if not isinstance(body, ast.FunctionDef):
                continue

            # Find out how many arguments and keyword-only arguments there are ...
            nArgs = len(body.args.args)
            nKwArgs = len(body.args.kwonlyargs)

            # Check if there are any arguments which are not explicitly either
            # keyword-only arguments or positional-only arguments...
            if nArgs != 0:
                # Cry ...
                raise Exception(f"\"{fname}\" has ambiguous arguments") from None

            # Skip if there aren't any keyword-only arguments ...
            if nKwArgs == 0:
                continue

            # Add this function to the database ...
            if body.name not in funcs:
                funcs[body.name] = []

            # Loop over keyword-only arguments ...
            for iKwArg in range(nKwArgs):
                # Append this keyword-only argument to the database ...
                funcs[body.name].append(body.args.kwonlyargs[iKwArg].arg)

    # **************************************************************************

    # Loop over functions and their keyword-only arguments ...
    for func, keywords in funcs.items():
        # Skip this function if its keyword-only arguments are already sorted ...
        if keywords == sorted(keywords):
            continue

        # Print ...
        print(f"The keyword-only arguments of \"{func}()\" are not sorted.")

    # **************************************************************************

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
                # Skip this node if it is not a function call (or if it is a
                # member of a module) ...
                if not isinstance(node, ast.Call):
                    continue
                if not isinstance(node.func, ast.Name):
                    continue

                # Skip this function call if it is not in the database ...
                if node.func.id not in funcs:
                    continue

                # Find all the keyword-only arguments that are passed ...
                keywords = []
                for keyword in node.keywords:
                    keywords.append(keyword.arg)

                # Loop over keyword-only arguments that *should* be passed ...
                for keyword in funcs[node.func.id]:
                    # Skip this keyword-only argument if it is passed ...
                    if keyword in keywords:
                        continue

                    # Print ...
                    print(f"\"{body.name}()\" in \"{fname}\" calls \"{node.func.id}()\" but does not pass \"{keyword} = \".")
