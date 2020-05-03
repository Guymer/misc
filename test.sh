#!/usr/bin/env bash

# Define binaries and check that they exist ...
python="python3.7"
pylint="pylint-3.7"
pylintexit="${HOME}/Library/Python/3.7/bin/pylint-exit"
if ! type "$python" &> /dev/null; then
    echo "ERROR: the binary defined in \$python does not exist" >&2
    exit 1
fi
if ! type "$pylint" &> /dev/null; then
    echo "ERROR: the binary defined in \$pylint does not exist" >&2
    exit 1
fi
if ! type "$pylintexit" &> /dev/null; then
    echo "ERROR: the binary defined in \$pylintexit does not exist" >&2
    echo "       try running \"pip-3.7 install --user pylint-exit\"" >&2
    exit 1
fi

# Change directory ...
cd "$HOME/Repositories" || exit 1

# Loop over directories ...
for d in *; do
    # Skip ones that do not exist ...
    [[ ! -d $d ]] && continue

    # Skip ones that are not Python modules ...
    [[ ! -f $d/__init__.py ]] && continue

    # Print warning if there isn't a PyLint configuration file ...
    if [[ ! -f $d/.pylintrc ]]; then
        echo "WARNING: $d is missing a PyLint configuration file"
        continue
    fi

    # Assume this module is Python 3.x but if it appears that there is a
    # separate explicit Python 3.x version of this module then assume that this
    # module is in fact Python 2.x and skip it ...
    if [[ -d ${d}3 ]]; then
        continue
    fi

    echo -n "Testing $d: "

    # Clean then import the module ...
    rm -f "$d"/*.pyc "$d"/*/*.pyc
    rm -rf "$d/__pycache__"
    $python -c "import $d" &> /dev/null
    if [[ $? -ne 0 ]]; then
        echo ""
        echo "ERROR: Failed to import \"$d\"" >&2
        exit 1
    fi

    # Run PyLint on the module ...
    $pylint --rcfile="$d/.pylintrc" "$d" &> "$d/pylint.log" || $pylintexit $? &> /dev/null
    if [[ $? -ne 0 ]]; then
        echo ""
        echo "ERROR: Failed to lint \"$d\"" >&2
        exit 1
    fi

    grep "Your code has been rated at" "$d/pylint.log" | cut -c 29-
done
