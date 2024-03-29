#!/usr/bin/env zsh

# Configure ZSH ...
setopt HIST_FIND_NO_DUPS
setopt HIST_REDUCE_BLANKS
setopt HIST_SAVE_NO_DUPS

# Set default programs ...
export EDITOR="vim"
export PAGER="more"

# Stop $PATH taking duplicated values ...
typeset -U path

# Set $PATH ...
path+=/sbin
path+=/bin
path+=/usr/sbin
path+=/usr/bin
path+=/usr/games
path+=/usr/local/sbin
path+=/usr/local/bin
path+=/usr/local/mpi/openmpi/bin
path+=/opt/local/bin
path+=${HOME}/bin
path+=${HOME}/gocode/bin
path+=${HOME}/Library/Python/3.11/bin
path+=${HOME}/.local/bin

# Set paths ...
export BASH_ENV="$HOME/.bashrc"
export CARTOPY_USER_BACKGROUNDS="/path/to/NaturalEarthBackgroundImages"
export GEM_HOME="$HOME/.gem"
export GOPATH="$HOME/gocode"
export PYTHONPATH="/path/to/Repositories:/path/to/modules"
export TMPDIR="/tmp"

# Set variables ...
# NOTE: https://superuser.com/a/1277375
export CRYPTOGRAPHY_OPENSSL_NO_LEGACY="1"
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
