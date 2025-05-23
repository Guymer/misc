#!/usr/bin/env bash

# Check that non-standard programs are installed. "standard" programs are
# anything that is specified in the POSIX.1-2008 standard (and the IEEE Std
# 1003.1 standard) or that is a BASH builtin command. Therefore, "non-standard"
# programs are anything that does not appear on the following two lists:
#   * https://pubs.opengroup.org/onlinepubs/9699919799/idx/utilities.html
#   * https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html

# Change directory ...
cd "${HOME}/Repositories" || exit 1

# Loop over repositories ...
for d in */.git; do
    # Clear the terminal and then run grep ...
    clear
    readarray -t fnames < <(find "$(dirname "${d}")" -type f 2> /dev/null | grep -v -F -e doc/ -e openflights/ -e ourairports-data/ -e stations/ -e validator/ -e .git/ -e build/ -e .png -e .bak -e .bin -e .jpg -e .pyc -e .o -e .mod -e .pdf -e .ppm -e .pgm -e .pbm -e .csv -e .zip -e DS_Store | sort)
    grep --color -n "http://" "${fnames[@]}" 2> /dev/null

    # Wait for the user to be ready to proceed and then clear the terminal again ...
    # shellcheck disable=SC2162
    read -p "Press enter to continue ..."
    clear
done
