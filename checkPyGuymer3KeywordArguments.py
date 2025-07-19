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
        raise Exception("\"pyguymer3\" is not installed; run \"pip install --user PyGuymer3\"") from None

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
            "exiftoolPath",
            "gifsiclePath",
            "gitPath",
            "jpegtranPath",
            "lsdvdPath",
            "metaflacPath",
            "mp4filePath",
            "mp4tagsPath",
            "mplayerPath",
            "optipngPath",
            "pkgPath",
            "portPath",
            "tarPath",
            "xzPath",
            "zypperPath",

            "angConv",                  # pyguymer3.geo.find_min_max_dist_bearing()
            "background",               # Lots of functions.
            "calcAdaptive",             # Lots of functions.
            "calcAverage",              # Lots of functions.
            "calcNone",                 # Lots of functions.
            "calcPaeth",                # Lots of functions.
            "calcSub",                  # Lots of functions.
            "calcUp",                   # Lots of functions.
            "chunksize",                # Lots of functions.
            "coastlines_edgecolor",     # pyguymer3.geo.add_axis()
            "coastlines_facecolor",     # pyguymer3.geo.add_axis()
            "coastlines_levels",        # pyguymer3.geo.add_axis()
            "coastlines_linestyle",     # pyguymer3.geo.add_axis()
            "coastlines_linewidth",     # pyguymer3.geo.add_axis()
            "coastlines_resolution",    # pyguymer3.geo.add_axis()
            "coastlines_zorder",        # pyguymer3.geo.add_axis()
            "cookies",                  # Lots of functions.
            "crf",                      # pyguymer3.media.images2mp4()
            "ensureNFC",                # Lots of functions.
            "eps",                      # Lots of functions.
            "extent",                   # pyguymer3.geo.add_map_background()
            "form",                     # pyguymer3.media.images2mp4()
            "gridlines_int",            # pyguymer3.geo.add_axis()
            "gridlines_linecolor",      # pyguymer3.geo.add_axis()
            "gridlines_linestyle",      # pyguymer3.geo.add_axis()
            "gridlines_linewidth",      # pyguymer3.geo.add_axis()
            "gridlines_zorder",         # pyguymer3.geo.add_axis()
            "headers",                  # Lots of functions.
            "ignorableFiles",           # pyguymer3.remove_almost_empty_directories()
            "level",                    # pyguymer3.media.images2mp4()
            "lossless",                 # Lots of functions.
            "method",                   # Lots of functions.
            "minimize_size",            # Lots of functions.
            "name",                     # pyguymer3.geo.add_map_background()
            "physical",                 # pyguymer3.geo.add_NE_map_underlay()
            "pool",                     # Lots of functions.
            "prefix",                   # Lots of functions.
            "progressive",              # Lots of functions.
            "profile",                  # pyguymer3.media.images2mp4()
            "quality",                  # Lots of functions.
            "ramLimit",                 # Lots of functions.
            "setModificationTime",      # Lots of functions.
            "strict",                   # pyguymer3.geo.getRecordAttribute()
            "tol",                      # Lots of functions.
            "useSciPy",                 # pyguymer3.geo.find_middle_of_locs()

            "gs",                       # A MatPlotLib subplot arrangement.

            "nrows",                    # A MatPlotLib subplot arrangement.
            "ncols",                    # A MatPlotLib subplot arrangement.
            "index",                    # A MatPlotLib subplot arrangement.
        ],
           dest = "unImpKwArgs",
           help = "the \"un-important\" keyword-only arguments to not check for if \"--lite\"",
          nargs = "+",
           type = str,
    )
    args = parser.parse_args()

    # **************************************************************************

    # Initialize database ...
    funcs : dict[str, list[str]] = {}

    # Loop over files in folder ...
    for fname in pyguymer3.return_file_list(
        pyguymer3.__path__[0],
            allowHidden = True,
                  debug = args.debug,
        follow_symlinks = False,
        return_symlinks = False,
    ):
        # Skip files which are not Python scripts ...
        if not fname.endswith(".py"):
            continue

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
    for fname in pyguymer3.return_file_list(
        args.dname,
            allowHidden = True,
                  debug = args.debug,
        follow_symlinks = False,
        return_symlinks = False,
    ):
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
                        raise Exception(f"{fname} » {srcGuess} » \"{keyword.arg}\" is specified but it is not a recognised keyword")
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
                        raise Exception(f"{fname} » {srcGuess} » \"{keyword.arg}\" is specified but it is not a recognised keyword")
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
                        raise Exception(f"{fname} » {srcGuess} » \"{keyword.arg}\" is specified but it is not a recognised keyword")
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
