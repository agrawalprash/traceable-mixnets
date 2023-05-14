#!/bin/bash

# Compute witness (internal variables for the given prover input)
cat build/zok.inp | zokrates compute-witness -i build/circuit -s build/abi.json --circom-witness build/circuit.wtns -o build/witness --abi --stdin

# Generate proof for this malicious circuit
zokrates generate-proof -i build/circuit -w build/witness --proving-key-path build/proving.key --proof-path build/proof.json

