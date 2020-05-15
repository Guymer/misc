#!/usr/bin/env bash

# Check that non-standard programs are installed. "standard" programs are
# anything that is specified in the POSIX.1-2008 standard (and the IEEE Std
# 1003.1 standard) or that is a BASH builtin command. Therefore, "non-standard"
# programs are anything that does not appear on the following two lists:
#   * https://pubs.opengroup.org/onlinepubs/9699919799/idx/utilities.html
#   * https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html
if ! type mktemp &> /dev/null; then
    echo "ERROR: \"mktemp\" is not installed." >&2
    exit 1
fi

# Define binaries and check that they exist ...
pip="/opt/local/bin/pip-3.7"
pylint="/opt/local/bin/pylint-3.7"
python="/opt/local/bin/python3.7"
if ! type "$pip" &> /dev/null; then
    echo "ERROR: the binary defined in \$pip does not exist" >&2
    exit 1
fi
if ! type "$pylint" &> /dev/null; then
    echo "ERROR: the binary defined in \$pylint does not exist" >&2
    exit 1
fi
if ! type "$python" &> /dev/null; then
    echo "ERROR: the binary defined in \$python does not exist" >&2
    exit 1
fi

# Define derived binaries and check that they exist ...
pylintexit="$($pip show --files pylint-exit | grep -E "^Location:" | cut -d : -f 2- | tr -d " ")/$($pip show --files pylint-exit | grep -E "bin/pylint-exit\$" | tr -d " ")"
if ! type "$pylintexit" &> /dev/null; then
    echo "ERROR: the binary defined in \$pylintexit does not exist" >&2
    echo "       try running \"$pip install --user pylint-exit\"" >&2
    exit 1
fi

# Change directory ...
cd "$HOME/Repositories" || exit 1

# Loop over directories ...
for d in *; do
    # Skip ones that do not exist ...
    [[ ! -d $d ]] && continue

    # Print warning if there isn't a PyLint configuration file ...
    if [[ ! -f $d/.pylintrc ]]; then
        echo "WARNING: $d is missing a PyLint configuration file"
        continue
    fi

    # Check if it is a Python module or if it is just a directory of Python
    # scripts ...
    if [[ -f $d/__init__.py ]]; then
        # Assume this module is Python 3.x but if it appears that there is a
        # separate explicit Python 3.x version of this module then assume that
        # this module is in fact Python 2.x and skip it ...
        if [[ -d ${d}3 ]]; then
            continue
        fi

        echo -n "Testing $d (as a module): "

        # Clean then import the Python module ...
        find "$d" -type f -name "*.pyc" -delete
        find "$d" -type d -name "__pycache__" -delete
        $python -c "import $d" &> /dev/null
        if [[ $? -ne 0 ]]; then
            echo ""
            echo "ERROR: Failed to import \"$d\"" >&2
            exit 1
        fi

        # Run PyLint on the Python module ...
        $pylint --rcfile="$d/.pylintrc" "$d" &> "$d/pylint.log" || $pylintexit $? &> /dev/null
        if [[ $? -ne 0 ]]; then
            echo ""
            echo "ERROR: Failed to lint \"$d\"" >&2
            exit 1
        fi

        grep "Your code has been rated at" "$d/pylint.log" | cut -c 29-
    else
        # Try to find all of the Python scripts that are not part of Git
        # submodules ...
        tmp1="$(mktemp)"
        tmp2="$(mktemp)"
        find "$d" -type f -name "*.py" | grep -v "/build/" | sort > "$tmp1"
        if [[ -f $d/.gitmodules ]]; then
            for m in $(grep "path = " "$d/.gitmodules" | cut -d "=" -f 2); do
                grep -v -E "^$d/$m" "$tmp1" > "$tmp2"
                cp "$tmp2" "$tmp1"
            done
        fi

        # Skip this directory if it does not contain any Python scripts ...
        if [[ $(wc -l < "$tmp1") -eq 0 ]]; then
            rm "$tmp1" "$tmp2"
            continue
        fi

        echo -n "Testing $d (as a directory): "

        # Run PyLint on the Python directory ...
        $pylint --rcfile="$d/.pylintrc" $(cat "$tmp1") &> "$d/pylint.log" || $pylintexit $? &> /dev/null
        if [[ $? -ne 0 ]]; then
            echo ""
            echo "ERROR: Failed to lint \"$d\"" >&2
            exit 1
        fi

        grep "Your code has been rated at" "$d/pylint.log" | cut -c 29-

        # Clean up ...
        rm "$tmp1" "$tmp2"
    fi
done
