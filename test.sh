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

# NOTE: Currently, the following two PyLint checks are hard-coded to be disabled
#       (so that I can concentrate on fixing all the others first):
#         * C0209 - Formatting a regular string which could be a f-string
#         * R0801 - Similar lines in %s files

# Define binaries and check that they exist ...
pylint="/opt/local/bin/pylint-3.11"
python="/opt/local/bin/python3.11"
shellcheck="/opt/local/bin/shellcheck"
if ! type "${pylint}" &> /dev/null; then
    echo "WARNING: the binary defined in \$pylint does not exist (Python checks will be skipped)"
fi
if ! type "${python}" &> /dev/null; then
    echo "WARNING: the binary defined in \$python does not exist (Python checks will be skipped)"
fi
if ! type "${shellcheck}" &> /dev/null; then
    echo "WARNING: the binary defined in \$shellcheck does not exist (Shell checks will be skipped)"
fi

# Change directory ...
cd "${HOME}/Repositories" || exit 1

# Loop over directories ...
for d in *; do
    # Skip ones that do not exist ...
    [[ ! -d ${d} ]] && continue

    # Check if the user passed an argument ...
    if [[ -n ${1} ]]; then
        # Skip this directory if it is not the one the user passed ...
        if [[ ${d} != "${1}" ]]; then
            continue
        fi
    fi

    # **************************************************************************

    # Print warning if there isn't a PyLint configuration file ...
    if ! type "${pylint}" &> /dev/null; then
        false
    elif ! type "${python}" &> /dev/null; then
        false
    elif [[ ! -f ${d}/.pylintrc ]]; then
        echo "WARNING: \"${d}\" is missing a PyLint configuration file"
    else
        # Check if it is a Python module or if it is just a directory of Python
        # scripts ...
        if [[ -f ${d}/$(basename "${d}")/__init__.py ]]; then
            # Assume this module is Python 3.x but if it appears that there is a
            # separate explicit Python 3.x version of this module then assume
            # that this module is in fact Python 2.x and skip it ...
            if [[ -d ${d}3 ]]; then
                continue
            fi

            printf "%-80s : " "Testing \"${d}\" (as a Python module)"

            # Clean then import the Python module ...
            find "${d}" -type f -name "*.pyc" -delete
            find "${d}" -type d -name "__pycache__" -delete
            if ! ${python} -c "import ${d}" &> /dev/null; then
                echo ""
                echo "ERROR: Failed to import \"${d}\"" >&2
                exit 1
            fi

            # Run PyLint on the Python module ...
            ${pylint} --rcfile="${d}/.pylintrc" --disable=R0801 "${d}/${d}" &> "${d}/pylint.log"

            # Check if it is perfect ...
            if grep -F "Your code has been rated at 10.00/10" "${d}/pylint.log" &> /dev/null; then
                echo "perfect"
            else
                grep -F "Your code has been rated at" "${d}/pylint.log" | cut -c 29-
            fi
        else
            # Try to find all of the Python scripts that are not part of Git
            # submodules ...
            tmp1="$(mktemp)"
            tmp2="$(mktemp)"
            find "${d}" -type f -name "*.py" | grep -v -F "/build/" | sort > "${tmp1}"
            if [[ -f ${d}/.gitmodules ]]; then
                while IFS= read -r m; do
                    grep -v -E "^${d}/${m}" "${tmp1}" > "${tmp2}"
                    cp "${tmp2}" "${tmp1}"
                done < <(grep -F "path = " "${d}/.gitmodules" | cut -d "=" -f 2 | tr -d " ")
            fi

            # Check that there are some Python scripts ...
            if [[ $(wc -l < "${tmp1}") -gt 0 ]]; then
                printf "%-80s : " "Testing \"${d}\" (as a Python script directory)"

                # Run PyLint on the Python script directory ...
                ${pylint} --rcfile="${d}/.pylintrc" --disable=R0801 $(cat "${tmp1}") &> "${d}/pylint.log"

                # Check if it is perfect ...
                if grep -F "Your code has been rated at 10.00/10" "${d}/pylint.log" &> /dev/null; then
                    echo "perfect"
                else
                    grep -F "Your code has been rated at" "${d}/pylint.log" | cut -c 29-
                fi
            fi

            # Clean up ...
            rm "${tmp1}" "${tmp2}"
        fi
    fi

    # **************************************************************************

    # Print warning if there isn't a ShellCheck configuration file ...
    if ! type "${shellcheck}" &> /dev/null; then
        false
    elif [[ ! -f ${d}/.shellcheckrc ]]; then
        echo "WARNING: \"${d}\" is missing a ShellCheck configuration file"
    else
        # Try to find all of the Shell scripts that are not part of Git
        # submodules ...
        tmp1="$(mktemp)"
        tmp2="$(mktemp)"
        find "${d}" -type f -name "*.sh" | grep -v -F "/build/" | sort > "${tmp1}"
        if [[ -f ${d}/.gitmodules ]]; then
            while IFS= read -r m; do
                grep -v -E "^${d}/${m}" "${tmp1}" > "${tmp2}"
                cp "${tmp2}" "${tmp1}"
            done < <(grep -F "path = " "${d}/.gitmodules" | cut -d "=" -f 2 | tr -d " ")
        fi

        # Check that there are some Shell scripts ...
        if [[ $(wc -l < "${tmp1}") -gt 0 ]]; then
            printf "%-80s : " "Testing \"${d}\" (as a Shell script directory)"

            # Run ShellCheck on the Shell script directory ...
            ln -sf "${d}/.shellcheckrc" ".shellcheckrc"
            if ${shellcheck} -x $(cat "${tmp1}") &> "${d}/shellcheck.log"; then
                echo "perfect"
            else
                echo "has issues"
            fi
            rm ".shellcheckrc"
        fi

        # Clean up ...
        rm "${tmp1}" "${tmp2}"
    fi
done
