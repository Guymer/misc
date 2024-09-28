#!/usr/bin/env bash

# Check that non-standard programs are installed. "standard" programs are
# anything that is specified in the POSIX.1-2008 standard (and the IEEE Std
# 1003.1 standard) or that is a BASH builtin command. Therefore, "non-standard"
# programs are anything that does not appear on the following two lists:
#   * https://pubs.opengroup.org/onlinepubs/9699919799/idx/utilities.html
#   * https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html
if ! type git &> /dev/null; then
    echo "ERROR: \"git\" is not installed." >&2
    exit 1
fi

# Change directory ...
cd "${HOME}/Repositories" || exit 1

# Loop over repositories ...
for d in */.git; do
    echo "Checking \"$(dirname "${d}")\" ..."

    # Change directory ...
    cd "$(dirname "${d}")" || exit 1

    # Commit everything ...
    git commit -a

    # Change directory ...
    cd "${HOME}/Repositories" || exit 1
done
