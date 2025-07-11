#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.12/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import argparse
    import glob
    import json
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
            description = "Check that all README.md files have all the required links to a project's used Python modules.",
        formatter_class = argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--debug",
        action = "store_true",
          help = "print debug messages",
    )
    args = parser.parse_args()

    # **************************************************************************

    # Load list of standard Python modules ...
    with open(f"{os.path.dirname(os.path.realpath(__file__, strict = True))}/Python 3.12 Standard Modules.json", "rt", encoding = "utf-8") as fObj:
        standardModules = json.load(fObj)

    # Append common non-standard Python modules that I do not want to be warned
    # about ...
    standardModules.append("f90")
    standardModules.append("funcs")
    standardModules.append("web_mod")

    # Define a list of Python modules which are not published on Pip ...
    unpublishedModules = [
        "sphinx_fortran",
    ]

    # Define a dictionary mapping Python module import names to Pip package
    # installation names ...
    python2pip = {
        "matplotlib" : "matplotlib >= 3.5.0",                                   # "labels" was added to "matplotlib.axes.Axes.set_xticks()".
               "PIL" : "pillow >= 8.0.0",                                       # "anchor" was implemented in "PIL.ImageDraw.text()".
         "pyguymer3" : "pyguymer3 >= 0.0.10",                                   # "fov" was added to "pyguymer3.geo.add_NE_map_underlay()".
         "shapefile" : "pyshp",
    }

    # Loop over READMEs ...
    for rname in sorted(glob.glob("*/README.md")):
        print(f"Checking \"{rname}\" ...")

        # Deduce directory name ...
        dname = os.path.dirname(rname)

        # **********************************************************************

        # Initialize list of sub-paths to ignore ...
        ipaths = [
            f"{dname}/.git",
            f"{dname}/build",
        ]

        # Deduce .gitmodules file name, check if it exists and populate list
        # with paths to ignore if it does ...
        mname = f"{dname}/.gitmodules"
        if os.path.exists(mname):
            with open(mname, "rt", encoding = "utf-8") as fObj:
                for line in fObj:
                    if not line.strip().startswith("path = "):
                        continue
                    ipaths.append(f'{dname}/{"=".join(line.strip().split("=")[1:]).strip()}')

        # **********************************************************************

        # Initialize list of imported non-standard modules ...
        modules = []

        # Loop over files in directory ...
        for pname in pyguymer3.return_file_list(
            dname,
                allowHidden = True,
                      debug = args.debug,
            follow_symlinks = False,
            return_symlinks = False,
        ):
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

            # Find all the non-standard modules which are imported and append
            # the missing ones to the list ...
            with open(pname, "rt", encoding = "utf-8") as fObj:
                for line in fObj:
                    if not line.strip().startswith("import "):
                        continue
                    module = line.strip().split(" ")[1].split(".")[0]
                    if module == dname:
                        continue
                    if module in standardModules:
                        continue
                    if module in modules:
                        continue
                    modules.append(module)

        # Skip this README if the repository does not import any non-standard
        # modules ...
        if len(modules) == 0:
            continue

        # As Sphinx is not imported it is easy for this script to miss Sphinx
        # requirements, so make sure that Sphinx is there is the Sphinx theme is
        # imported ...
        if "sphinx_rtd_theme" in modules:
            if "sphinx" not in modules:
                modules.append("sphinx")
        if "sphinx" in modules:
            if "sphinx_fortran" not in modules:
                modules.append("sphinx_fortran")

        # It is unclear if NumPy always pulls in Meson/Ninja to allow f2py
        # builds, so manually add them just in case ...
        if "numpy" in modules:
            if "meson" not in modules:
                modules.append("meson")
            if "ninja" not in modules:
                modules.append("ninja")

        # **********************************************************************

        # Open Pip requirements file for writing ...
        with open(f"{dname}/requirements.txt", "wt", encoding = "utf-8") as fObj:
            # Write header ...
            fObj.write("# This Pip requirements file was automatically generated by the\n")
            fObj.write("# \"check_READMEs.py\" script from \"https://github.com/Guymer/misc\".\n")
            fObj.write("\n")

            # Write imported non-standard modules ...
            for module in sorted(modules):
                if module in unpublishedModules:
                    continue
                if module in [
                    "meson",
                    "ninja",
                ]:
                    fObj.write(f"{python2pip.get(module, module)} # Required so that NumPy can use an up-to-date version (not the old\n")
                    fObj.write("      # version that came with your system) when running \"f2py\".\n")
                else:
                    fObj.write(f"{python2pip.get(module, module)}\n")

        # **********************************************************************

        # Load README ...
        with open(rname, "rt", encoding = "utf-8") as fObj:
            lines = fObj.readlines()

        # Loop over imported non-standard modules ...
        for module in sorted(modules):
            if module in [
                "meson",
                "ninja",
            ]:
                continue
            linked = False
            for line in lines:
                if line.strip().startswith(f"* [{module}]("):
                    linked = True
                    break
            if linked:
                continue
            print(f"  ... needs a link adding for \"{module}\"")
