#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.12/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import argparse
    import ast
    import os

    # Import my modules ...
    try:
        import pyguymer3
    except:
        raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

    # **************************************************************************

    # Create argument parser and parse the arguments ...
    parser = argparse.ArgumentParser(
           allow_abbrev = False,
            description = "Check PyGuymer3 keyword-only arguments in Python functions.",
        formatter_class = argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "dname",
        help = "the folder to check",
        type = str,
    )
    parser.add_argument(
        "--debug",
        action = "store_true",
          help = "print debug messages",
    )
    parser.add_argument(
        "--lite",
        action = "store_true",
          help = "don't check for \"un-important\" keyword-only arguments (see \"--un-important-keyword-arguments\")",
    )
    parser.add_argument(
        "--un-important-keyword-arguments",
        default = [
            "atomicParsleyPath",
            "chunksize",
            "coastlines_edgecolor",
            "coastlines_facecolor",
            "coastlines_levels",
            "coastlines_linestyle",
            "coastlines_linewidth",
            "coastlines_resolution",
            "coastlines_zorder",
            "cookies",
            "eps",
            "exiftoolPath",
            "gifsiclePath",
            "gitPath",
            "gridlines_int",
            "gridlines_linecolor",
            "gridlines_linestyle",
            "gridlines_linewidth",
            "gridlines_zorder",
            "headers",
            "ignorableFiles",
            "jpegtranPath",
            "lsdvdPath",
            "metaflacPath",
            "mp4filePath",
            "mp4tagsPath",
            "mplayerPath",
            "nIter",
            "optipngPath",
            "pkgPath",
            "portPath",
            "prefix",
            "progressive",
            "ramLimit",
            "tarPath",
            "tol",
            "xzPath",
            "zypperPath",
        ],
           dest = "unImpKwArgs",
           help = "the \"un-important\" keyword-only arguments to not check for if \"--lite\"",
          nargs = "+",
           type = str,
    )
    args = parser.parse_args()

    # **************************************************************************

    # Initialize database ...
    funcs = {}

    # Loop over files in folder ...
    for fname in pyguymer3.return_file_list(pyguymer3.__path__[0]):
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
            # Skip bodies which are not function definitions ...
            if not isinstance(body, ast.FunctionDef):
                continue

            # Find out how many keyword-only arguments there are ...
            nKwArgs = len(body.args.kwonlyargs)

            # Skip if there aren't any keyword-only arguments ...
            if nKwArgs == 0:
                continue

            # Determine key ...
            key = f'pyguymer3{os.path.dirname(fname).removeprefix(f"{pyguymer3.__path__[0]}").replace("/", ".")}.{body.name}'

            # Add this function to the database ...
            if key not in funcs:
                funcs[key] = []

            # Loop over keyword-only arguments ...
            for iKwArg in range(nKwArgs):
                # Append this keyword-only argument to the database ...
                funcs[key].append(body.args.kwonlyargs[iKwArg].arg)

    # **************************************************************************

    # Initialize log ...
    log = []

    # Loop over files in folder ...
    for fname in pyguymer3.return_file_list(args.dname):
        # Skip files which are not Python scripts ...
        if not fname.endswith(".py"):
            continue

        print(f"Checking \"{fname}\" ...")

        # Skip Python scripts which are known Git submodules ...
        if "/openflights/" in fname:
            continue
        if "/ourairports-data/" in fname:
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
                # Skip this node if it is not a function call ...
                if not isinstance(node, ast.Call):
                    continue

                # Skip this function call if the function is not an attribute ...
                if not isinstance(node.func, ast.Attribute):
                    continue

                # Make a guess at recreating the source code, and skip if it
                # isn't from PyGuymer3 ...
                srcGuess = ast.unparse(node)
                if not srcGuess.startswith("pyguymer3."):
                    continue

                print(f"  Found \"{srcGuess}\".")

                # Determine key and skip if this PyGuymer3 function doesn't have
                # keywords ...
                key = srcGuess.split("(", maxsplit = 1)[0].split("[", maxsplit = 1)[0]
                if key not in funcs:
                    print(f"    \"{key}\" doesn't have any keywords.")
                    continue

                # Make a dictionary of flags ...
                flags = {}
                for keyword in funcs[key]:
                    flags[keyword] = False

                # Handle PyGuymer3 attributes ...
                if isinstance(node.func.value, ast.Attribute):
                    for keyword in node.keywords:
                        if keyword.arg in funcs[key]:
                            flags[keyword.arg] = True
                            continue
                        raise Exception(f"\"{keyword.arg}\" is specified but it is not a recognised keyword")
                    for keyword, flag in flags.items():
                        if flag:
                            if args.lite and keyword in args.unImpKwArgs:
                                log.append(f"ERROR: {fname} » {srcGuess} » \"{keyword}\" is specified but it shouldn't be")
                            continue
                        if not args.lite or keyword not in args.unImpKwArgs:
                            print(f"    \"{keyword}\" isn't specified.")
                            log.append(f"LOG: {fname} » {srcGuess} » \"{keyword}\" isn't specified")
                    continue

                # Handle PyGuymer3 calls ...
                if isinstance(node.func.value, ast.Call):
                    for keyword in node.func.value.keywords:
                        if keyword.arg in funcs[key]:
                            flags[keyword.arg] = True
                            continue
                        raise Exception(f"\"{keyword.arg}\" is specified but it is not a recognised keyword")
                    for keyword, flag in flags.items():
                        if flag:
                            if args.lite and keyword in args.unImpKwArgs:
                                log.append(f"ERROR: {fname} » {srcGuess} » \"{keyword}\" is specified but it shouldn't be")
                            continue
                        if not args.lite or keyword not in args.unImpKwArgs:
                            print(f"    \"{keyword}\" isn't specified.")
                            log.append(f"LOG: {fname} » {srcGuess} » \"{keyword}\" isn't specified")
                    continue

                # Handle PyGuymer3 names ...
                if isinstance(node.func.value, ast.Name):
                    for keyword in node.keywords:
                        if keyword.arg in funcs[key]:
                            flags[keyword.arg] = True
                            continue
                        raise Exception(f"\"{keyword.arg}\" is specified but it is not a recognised keyword")
                    for keyword, flag in flags.items():
                        if flag:
                            if args.lite and keyword in args.unImpKwArgs:
                                log.append(f"ERROR: {fname} » {srcGuess} » \"{keyword}\" is specified but it shouldn't be")
                            continue
                        if not args.lite or keyword not in args.unImpKwArgs:
                            print(f"    \"{keyword}\" isn't specified.")
                            log.append(f"LOG: {fname} » {srcGuess} » \"{keyword}\" isn't specified")
                    continue

                # Catch unexpected types ...
                print(f"WARNING: Unable to ascertain the keywords specified as \"node.func.value\" is a \"{type(node.func.value)}\".")
                if args.debug:
                    print(ast.dump(node, indent = 4))

    # Print log ...
    print(80 * "*")
    print("\n".join(log))
