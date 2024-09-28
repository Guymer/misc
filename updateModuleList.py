#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.12/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import json
    import sys

    # **************************************************************************

    # Initialize the module list ...
    modules = []

    # Loop over modules ...
    for module in list(sys.builtin_module_names) + list(sys.stdlib_module_names):
        # Skip module if it would be hidden in Python ...
        if module.startswith("_"):
            continue

        # Append module to module list ...
        if module not in modules:
            modules.append(module)

    # Sort the module list ...
    modules.sort(key = str.lower)

    # Save the module list ...
    with open(f"Python {sys.version_info.major}.{sys.version_info.minor} Standard Modules.json", "wt", encoding = "utf-8") as fObj:
        json.dump(
            modules,
            fObj,
            ensure_ascii = False,
                  indent = 4,
               sort_keys = True,
        )
