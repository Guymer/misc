#!/usr/bin/env bash

# Check that non-standard programs are installed. "standard" programs are
# anything that is specified in the POSIX.1-2008 standard (and the IEEE Std
# 1003.1 standard) or that is a BASH builtin command. Therefore, "non-standard"
# programs are anything that does not appear on the following two lists:
#   * https://pubs.opengroup.org/onlinepubs/9699919799/idx/utilities.html
#   * https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html
if ! type gcovr &> /dev/null; then
    echo "ERROR: \"gcovr\" is not installed." >&2
    exit 1
fi

echo "Running \"main\" ..."
./main

echo "Generating coverage report ..."
echo "NOTE: On MacOS these commands produce empty output when run in the BASH"
echo "      script but work fine if you run them in your terminal manually."
cd ..
rm -rf coverage-output
mkdir coverage-output
gcovr --gcov-ignore-parse-errors --html-details coverage-output/index.html
echo "# Created by run.sh" >> coverage-output/.gitignore
echo "*" >> coverage-output/.gitignore
