#!/bin/bash

set -o nounset
set -o pipefail

#
# setup tools
#
export PATH=$PATH:~/github/XLang/tools/cc65/bin:~/github/XLang/tools/x16emu


#
# compile the project
#
PROJECT=${1:-asm}

PROJECT_DIR=projects/$PROJECT

(cd $PROJECT_DIR && make ) || exit 1


#
# run the program
#

PROGRAM_FILE=$(find $PROJECT_DIR | grep "PRG$")

x16emu -scale 2 -prg $PROGRAM_FILE -run

