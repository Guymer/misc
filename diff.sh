#!/usr/bin/env bash

# Change directory ...
cd "$HOME/Repositories" || exit 1

# Loop over repositories ...
for d in */.git; do
    # Change directory ...
    cd "$(dirname "$d")" || exit 1

    # Clear the terminal and then print the difference ...
    clear
    git diff

    # Wait for the user to be ready to proceed and then clear the terminal again ...
    read -p "Press enter to continue ..."
    clear

    # Change directory ...
    cd ../
done
