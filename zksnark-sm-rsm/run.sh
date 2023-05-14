#!/bin/bash

rm -rf build
mkdir build
printf "COMPUTATION:\n"; time python3 $1.py ${@:2}
printf "\nTRUSTED SETUP:\n"; time ./setup.sh build/$1.zok
printf "\nPROVER:\n"; time ./prover.sh
printf "\nVERIFIER:\n"; time ./verifier.sh

