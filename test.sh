#!/usr/bin/env bash

# Check that non-standard programs are installed. "standard" programs are
# anything that is specified in the POSIX.1-2008 standard (and the IEEE Std
# 1003.1 standard) or that is a BASH builtin command. Therefore, "non-standard"
# programs are anything that does not appear on the following two lists:
#   * https://pubs.opengroup.org/onlinepubs/9699919799/idx/utilities.html
#   * https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html

# Define binaries and check that they exist ...
pip="/opt/local/bin/pip-3.7"
pylint="/opt/local/bin/pylint-3.7"
python="/opt/local/bin/python3.7"
if ! type "$pip" &> /dev/null; then
    echo "ERROR: the binary defined in \$pip does not exist" >&2
    exit 1
fi
if ! type "$python" &> /dev/null; then
    echo "ERROR: the binary defined in \$python does not exist" >&2
    exit 1
fi
if ! type "$pylint" &> /dev/null; then
    echo "ERROR: the binary defined in \$pylint does not exist" >&2
    exit 1
fi

# Define derived binaries and check that they exist ...
pylintexit="$($pip show --files pylint-exit | grep -E "^Location:" | cut -d : -f 2- | tr -d " ")/$($pip show --files pylint-exit | grep -E "bin/pylint-exit\$" | tr -d " ")"
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
