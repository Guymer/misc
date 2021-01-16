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
export CARTOPY_USER_BACKGROUNDS="/path/to/NaturalEarthBackgroundImages"
export GEM_HOME="$HOME/.gem"
export GOPATH="$HOME/gocode"
export PATH="/sbin:/bin:/usr/sbin:/usr/bin:/usr/games:/usr/local/sbin:/usr/local/bin:/usr/local/mpi/openmpi/bin:/opt/local/bin:$HOME/bin:$HOME/gocode/bin:$HOME/Library/Python/3.8/bin"
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
        export JAVA_HOME="/Library/Java/JavaVirtualMachines/openjdk13/Contents/Home"
        export MAIL="/var/mail/$USER"

        # Set aliases ...
        alias ls="ls -AGT"
        alias mktemp="mktemp -t tmp"
        alias rsync="rsync --exclude .DS_Store --iconv=utf-8-mac,utf-8 --outbuf=line --timeout=300"
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
alias youtube-dl="youtube-dl -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"
