#!/usr/bin/env bash

# Configure BASH ...
shopt -s dotglob
shopt -s expand_aliases
shopt -s extglob
export HISTCONTROL="erasedups"

# Set default programs ...
export EDITOR="vim"
export PAGER="more"

# Set paths ...
export BASH_ENV="$HOME/.bashrc"
export CARTOPY_USER_BACKGROUNDS="/path/to/NaturalEarthBackgroundImages"
export GEM_HOME="$HOME/.gem"
export GOPATH="$HOME/gocode"
export PATH="/sbin:/bin:/usr/sbin:/usr/bin:/usr/games:/usr/local/sbin:/usr/local/bin:/usr/local/mpi/openmpi/bin:/opt/local/bin:$HOME/bin:$HOME/gocode/bin:$HOME/Library/Python/3.9/bin"
export PYTHONPATH="/path/to/Repositories:/path/to/modules"
export TMPDIR="/tmp"

# Set variables ...
# NOTE: https://superuser.com/a/1277375
export LANG="en_GB.UTF-8"
export NCURSES_NO_UTF8_ACS="1"
export PINENTRY_USER_DATA="USE_CURSES=1"
export PYTHONIOENCODING="UTF-8"
export PYTHONUNBUFFERED="true"

# Check what OS it is ...
case $(uname) in
    "Darwin" )
        # Set variables ...
        export JAVA_HOME="/Library/Java/JavaVirtualMachines/openjdk17/Contents/Home"
        export MAIL="/var/mail/$USER"

        # Set aliases ...
        alias ls="ls -AGT"
        alias mktemp="mktemp -t tmp"
        alias rsync="/opt/local/bin/rsync --exclude .DS_Store --iconv=utf-8-mac,utf-8 --outbuf=line --timeout=300"
        ;;
    "FreeBSD" )
        # Set variables ...
        export JAVA_HOME="/usr/local/openjdk11"
        export MAIL="/var/mail/$USER"

        # Set aliases ...
        alias ls="ls -AG -D \"%Y-%m-%d %H:%M:%S\""
        alias mktemp="mktemp -t tmp"
        alias rsync="rsync --outbuf=line --timeout=300"
        ;;
    "Linux" )
        # Set variables ...
        export MAIL="/var/spool/mail/$USER"

        # Set aliases ...
        alias chcon="chcon --preserve-root"
        alias chgrp="chgrp --preserve-root"
        alias chmod="chmod --preserve-root"
        alias chown="chown --preserve-root"
        alias ls="ls --almost-all --color=auto --time-style=long-iso -N"
        alias mktemp="mktemp --tmpdir tmpXXXXXX"
        alias rsync="rsync --outbuf=line --timeout=300"
        alias shred="shred --iterations=25 --random-source=/dev/random --zero"
        ;;
esac

# Set aliases ...
alias cp="cp -p"
alias generate_password="python3 -c \"import pyguymer3; print(pyguymer3.generate_password())\""
alias generate_random_stub="python3 -c \"import pyguymer3; print(pyguymer3.generate_random_stub())\""
alias gpg="gpg --cipher-algo AES256"
alias lsof="lsof +w"
alias mkdir="mkdir -p"
alias scp="scp -p"
alias wget="wget --dns-timeout 5 --connect-timeout 5"

# Define function ...
checkip() {
    # NOTE: https://unix.stackexchange.com/a/111852
    rx='([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
    if [[ $1 =~ ^$rx\.$rx\.$rx\.$rx$ ]]; then
        return 0
    else
        return 1
    fi
}

# Define function ...
getbtime() {
    case $(uname) in
        "Darwin" | "FreeBSD" )
            stat -f %B "$1"
            ;;
        "Linux" )
            echo -n "ERROR: \"birthtime\" is not provided by the stat command on Linux"
            ;;
    esac
}

# Define function ...
getmd5() {
    case $(uname) in
        "Darwin" | "FreeBSD" )
            md5 -r "$1" | grep -o -E "^[a-z0-9]+"
            ;;
        "Linux" )
            md5sum "$1" | grep -o -E "^[a-z0-9]+"
            ;;
    esac
}

# Define function ...
getmtime() {
    case $(uname) in
        "Darwin" | "FreeBSD" )
            stat -f %m "$1"
            ;;
        "Linux" )
            stat -c %Y "$1"
            ;;
    esac
}

# Define function ...
getsize() {
    case $(uname) in
        "Darwin" | "FreeBSD" )
            stat -f %z "$1"
            ;;
        "Linux" )
            stat -c %s "$1"
            ;;
    esac
}

# Define function ...
trim() {
    # NOTE: https://stackoverflow.com/a/3352015
    local var="$*"
    var="${var#"${var%%[![:space:]]*}"}"
    var="${var%"${var##*[![:space:]]}"}"
    echo -n "$var"
}

# Define function ...
urldecode() {
    # NOTE: https://unix.stackexchange.com/a/187256
    local url_encoded="${1//+/ }"
    printf '%b' "${url_encoded//%/\\x}"
}
