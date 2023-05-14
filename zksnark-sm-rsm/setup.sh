#!/bin/bash

# Generate the circuit for the computation.
zokrates compile -i $1 -o build/circuit -s build/abi.json -r build/circuit.r1cs --debug

# Generate proving and verification keys
zokrates setup -i build/circuit --verification-key-path build/verification.key --proving-key-path build/proving.key


