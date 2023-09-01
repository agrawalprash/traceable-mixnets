Requirement: Docker (https://www.docker.com) (note that the benchmarks have been tested on Intel x86 chips and may not work on Apple ARM chips)

A) To benchmark the DB-SM and DB-RSM protocols of our traceable mixnet construction, follow these steps:
        
        #1. Create the docker container from the given docker file:
        docker build -f Dockerfile_db_sm_rsm -t db-sm-rsm .

        #2. Open a shell inside the docker container:
        docker run -i -t db-sm-rsm sh

        #3. Execute our code. Replace 'n' with number of ciphertexts and 'm' with number of mix-servers. 
        #     Note that in the code, we indicate 'm' with 'alpha'.
        python db_sm_rsm.py n m

        # Note: The above will take some constant time initially for precomputing powers of bases for fast modular exponentiation later, so if you want to 
        # switch off these precomputation steps, you can run the following command instead:
        precomputing=0 python db_sm_rsm.py n m 

Our complete implementation source code is available at the `db-sm-rsm` directory.
We also provide a report from a sample run of DB-SM and DB-RSM protocols for n=10000 ciphertexts and m=4 mix-servers at `sample-reports/report-db-sm-rsm-n10000-m4`, reproduced below:

         main
             number of entries: 10000
             number of mix-servers: 4
         main
             preprocessing
                     precomputing...
                 pai_th_keygen time: 44 s
                     precomputing...
                 pai_keygen time: 19 s
                     precomputing...
                 pai_keygen time: 19 s
                     precomputing...
                 pai_keygen time: 19 s
                     precomputing...
                 pai_keygen time: 19 s
                 gen_beaver_triples time: 2.5 s
                 creating proof of knowledge of permutation commitment opening time: 160 s
                 status_permcomm: True
             preprocessing time: 280 s
             input preparation time: 1100 s
             checking inputs
                 check_encs
                     mixer 0: checking proofs of knowledge of input ciphertexts time: 390 s
                     mixer 1: checking proofs of knowledge of input ciphertexts time: 390 s
                     mixer 2: checking proofs of knowledge of input ciphertexts time: 390 s
                     mixer 3: checking proofs of knowledge of input ciphertexts time: 390 s
                     mixer 0 total time: 390 s
                     mixer 1 total time: 390 s
                     mixer 2 total time: 390 s
                     mixer 3 total time: 390 s
                 check_encs time: 1600 s
                 status_encs: True
             checking inputs time: 1600 s
             mixing
                 re-encryption and permutation
                     mixer 0: re-encryption time: 4.5 s
                     mixer 0: creating proof of correct shuffle time: 30 s
                     mixer 1: re-encryption time: 4.5 s
                     mixer 1: creating proof of correct shuffle time: 30 s
                     mixer 2: re-encryption time: 4.5 s
                     mixer 2: creating proof of correct shuffle time: 30 s
                     mixer 3: re-encryption time: 4.5 s
                     mixer 3: creating proof of correct shuffle time: 30 s
                     mixer 0: verifying others' proofs of shuffle time: 75 s
                     mixer 1: verifying others' proofs of shuffle time: 75 s
                     mixer 2: verifying others' proofs of shuffle time: 74 s
                     mixer 3: verifying others' proofs of shuffle time: 75 s
                     status_shuffle: True
                     mixer 0 total time: 110 s
                     mixer 1 total time: 110 s
                     mixer 2 total time: 110 s
                     mixer 3 total time: 110 s
                 re-encryption and permutation time: 440 s
                 decryption of output messages
                     mixer 0: threshold decryption time: 190 s
                     mixer 1: threshold decryption time: 190 s
                     mixer 2: threshold decryption time: 190 s
                     mixer 3: threshold decryption time: 190 s
                     mixer 0: verifying others' decryption shares (batched) time: 24 s
                     mixer 1: verifying others' decryption shares (batched) time: 24 s
                     mixer 2: verifying others' decryption shares (batched) time: 24 s
                     mixer 3: verifying others' decryption shares (batched) time: 24 s
                     mixer 0: combining decryption shares time: 0.17 s
                     mixer 1: combining decryption shares time: 0.17 s
                     mixer 2: combining decryption shares time: 0.17 s
                     mixer 3: combining decryption shares time: 0.17 s
                     status_decshares: True
                     mixer 0 total time: 210 s
                     mixer 1 total time: 210 s
                     mixer 2 total time: 210 s
                     mixer 3 total time: 210 s
                 decryption of output messages time: 840 s
                 decryption of individual message/randomness shares
                     mixer 0: decryption of individual message/randomness shares time: 22 s
                     mixer 1: decryption of individual message/randomness shares time: 22 s
                     mixer 2: decryption of individual message/randomness shares time: 22 s
                     mixer 3: decryption of individual message/randomness shares time: 22 s
                     mixer 0 total time: 22 s
                     mixer 1 total time: 22 s
                     mixer 2 total time: 22 s
                     mixer 3 total time: 22 s
                 decryption of individual message/randomness shares time: 90 s
                 mixer 0 total time: 340 s
                 mixer 1 total time: 340 s
                 mixer 2 total time: 340 s
                 mixer 3 total time: 340 s
             mixing time: 1400 s
             forward set membership
                 get_verfsigs
                     verifier: creating BB signatures and encryptions time: 8.3 s
                     verifier total time: 8.3 s
                 get_verfsigs time: 8.3 s
                 check_verfsigs
                     mixer 0: checking verifier's signatures and encryptions time: 15 s
                     mixer 1: checking verifier's signatures and encryptions time: 15 s
                     mixer 2: checking verifier's signatures and encryptions time: 15 s
                     mixer 3: checking verifier's signatures and encryptions time: 15 s
                     mixer 0 total time: 15 s
                     mixer 1 total time: 15 s
                     mixer 2 total time: 15 s
                     mixer 3 total time: 15 s
                 check_verfsigs time: 61 s
                 status_verfsigs: True
                 get_blsigs
                     re-encrypt and reverse-permute BB signatures
                         mixer 3: reencrypting encrypted BB signatures time: 8.5 s
                         mixer 3: creating proof of shuffle of encrypted BB signatures time: 28 s
                         mixer 2: reencrypting encrypted BB signatures time: 8.6 s
                         mixer 2: creating proof of shuffle of encrypted BB signatures time: 29 s
                         mixer 1: reencrypting encrypted BB signatures time: 8.6 s
                         mixer 1: creating proof of shuffle of encrypted BB signatures time: 29 s
                         mixer 0: reencrypting encrypted BB signatures time: 8.6 s
                         mixer 0: creating proof of shuffle of encrypted BB signatures time: 29 s
                         mixer 0: verifying others' proofs of shuffle of encrypted BB signatures time: 110 s
                         mixer 1: verifying others' proofs of shuffle of encrypted BB signatures time: 110 s
                         mixer 2: verifying others' proofs of shuffle of encrypted BB signatures time: 110 s
                         mixer 3: verifying others' proofs of shuffle of encrypted BB signatures time: 110 s
                         status_shuffle_blsigs: True
                         mixer 0 total time: 150 s
                         mixer 1 total time: 150 s
                         mixer 2 total time: 150 s
                         mixer 3 total time: 150 s
                     re-encrypt and reverse-permute BB signatures time: 600 s
                     generate encrypted blinded BB signatures
                         mixer 0: generate encrypted blinded BB signatures and proofs of knowledge of blinding factors time: 39 s
                         mixer 1: generate encrypted blinded BB signatures and proofs of knowledge of blinding factors time: 39 s
                         mixer 2: generate encrypted blinded BB signatures and proofs of knowledge of blinding factors time: 39 s
                         mixer 3: generate encrypted blinded BB signatures and proofs of knowledge of blinding factors time: 39 s
                         mixer 0: verifying others' proofs of knowledge of blinding factors time: 93 s
                         mixer 1: verifying others' proofs of knowledge of blinding factors time: 93 s
                         mixer 2: verifying others' proofs of knowledge of blinding factors time: 93 s
                         mixer 3: verifying others' proofs of knowledge of blinding factors time: 93 s
                         status_pk_bl: True
                         mixer 0: generate encrypted blinded BB signatures time: 0.0092 s
                         mixer 1: generate encrypted blinded BB signatures time: 0.044 s
                         mixer 2: generate encrypted blinded BB signatures time: 0.042 s
                         mixer 3: generate encrypted blinded BB signatures time: 0.042 s
                         mixer 0 total time: 130 s
                         mixer 1 total time: 130 s
                         mixer 2 total time: 130 s
                         mixer 3 total time: 130 s
                     generate encrypted blinded BB signatures time: 530 s
                     decrypt blinded signatures
                         mixer 0: obtain decryption shares time: 10 s
                         mixer 1: obtain decryption shares time: 10 s
                         mixer 2: obtain decryption shares time: 10 s
                         mixer 3: obtain decryption shares time: 10 s
                         mixer 0: verifying others' decryption shares time: 12 s
                         mixer 1: verifying others' decryption shares time: 12 s
                         mixer 2: verifying others' decryption shares time: 12 s
                         mixer 3: verifying others' decryption shares time: 12 s
                         mixer 0: combine decryption shares time: 0.12 s
                         mixer 1: combine decryption shares time: 0.09 s
                         mixer 2: combine decryption shares time: 0.09 s
                         mixer 3: combine decryption shares time: 0.089 s
                         status_decshares_blsigs: True
                         mixer 0 total time: 22 s
                         mixer 1 total time: 22 s
                         mixer 2 total time: 22 s
                         mixer 3 total time: 22 s
                     decrypt blinded signatures time: 88 s
                     mixer 0 total time: 300 s
                     mixer 1 total time: 300 s
                     mixer 2 total time: 300 s
                     mixer 3 total time: 300 s
                 get_blsigs time: 1200 s
                 dpk_bbsig_nizkproofs
                     mixer 0: creating dpk_bbsig commit message time: 180 s
                     mixer 1: creating dpk_bbsig commit message time: 180 s
                     mixer 2: creating dpk_bbsig commit message time: 180 s
                     mixer 3: creating dpk_bbsig commit message time: 180 s
                     mixer 0: creating dpk_bbsig challenge time: 0.087 s
                     mixer 1: creating dpk_bbsig challenge time: 0.088 s
                     mixer 2: creating dpk_bbsig challenge time: 0.09 s
                     mixer 3: creating dpk_bbsig challenge time: 0.091 s
                     mixer 0: creating dpk_bbsig response message time: 0.013 s
                     mixer 1: creating dpk_bbsig response message time: 0.01 s
                     mixer 2: creating dpk_bbsig response message time: 0.0099 s
                     mixer 3: creating dpk_bbsig response message time: 0.0099 s
                     mixer 0 total time: 180 s
                     mixer 1 total time: 180 s
                     mixer 2 total time: 180 s
                     mixer 3 total time: 180 s
                 dpk_bbsig_nizkproofs time: 720 s
                 dpk_bbsig_nizkverifs
                     verifier: verifying dpk_bbsig proof time: 200 s
                     verifier total time: 200 s
                 dpk_bbsig_nizkverifs time: 200 s
                 status_dpk_bbsig: True
                 status_forward_set_membership: True
                 mixer 0 total time: 500 s
                 mixer 1 total time: 500 s
                 mixer 2 total time: 500 s
                 mixer 3 total time: 500 s
                 verifier total time: 210 s
             forward set membership time: 2200 s
             reverse set membership
                 pkcommverifs
                     verifier: verifying proof of knowledge of commitment openings time: 7.8 s
                     verifier total time: 7.8 s
                 pkcommverifs time: 7.8 s
                 status_pkcomms True
                 get_verfsigs_rev
                     verifier: creating BBS+ signatures and encryptions time: 23 s
                     verifier total time: 23 s
                 get_verfsigs_rev time: 23 s
                 check_verfsigs_rev
                     mixer 0: checking verifier's signatures and encryptions time: 27 s
                     mixer 1: checking verifier's signatures and encryptions time: 27 s
                     mixer 2: checking verifier's signatures and encryptions time: 27 s
                     mixer 3: checking verifier's signatures and encryptions time: 27 s
                     mixer 0 total time: 27 s
                     mixer 1 total time: 27 s
                     mixer 2 total time: 27 s
                     mixer 3 total time: 27 s
                 check_verfsigs_rev time: 110 s
                 status_verfsigs_rev: True
                 get_blsigs_rev
                     homomorphically obtain the r component of BBS+ signatures
                         mixer 0: homomorphically obtain the r component of BBS+ sig time: 0.05 s
                         mixer 1: homomorphically obtain the r component of BBS+ sig time: 0.05 s
                         mixer 2: homomorphically obtain the r component of BBS+ sig time: 0.051 s
                         mixer 3: homomorphically obtain the r component of BBS+ sig time: 0.05 s
                         mixer 0 total time: 0.05 s
                         mixer 1 total time: 0.05 s
                         mixer 2 total time: 0.051 s
                         mixer 3 total time: 0.05 s
                     homomorphically obtain the r component of BBS+ signatures time: 0.2 s
                     re-encrypt and permute BBS+ signatures
                         mixer 0: reencrypting encrypted BBS+ signatures time: 17 s
                         mixer 0: creating proof of shuffle of encrypted BBS+ signatures time: 89 s
                         mixer 1: reencrypting encrypted BBS+ signatures time: 18 s
                         mixer 1: creating proof of shuffle of encrypted BBS+ signatures time: 88 s
                         mixer 2: reencrypting encrypted BBS+ signatures time: 18 s
                         mixer 2: creating proof of shuffle of encrypted BBS+ signatures time: 88 s
                         mixer 3: reencrypting encrypted BBS+ signatures time: 18 s
                         mixer 3: creating proof of shuffle of encrypted BBS+ signatures time: 88 s
                         mixer 0: verifying others' proofs of shuffle of encrypted BBS+ signatures time: 260 s
                         mixer 1: verifying others' proofs of shuffle of encrypted BBS+ signatures time: 260 s
                         mixer 2: verifying others' proofs of shuffle of encrypted BBS+ signatures time: 260 s
                         mixer 3: verifying others' proofs of shuffle of encrypted BBS+ signatures time: 260 s
                         status_shuffle_blsigs_rev: True
                         mixer 0 total time: 370 s
                         mixer 1 total time: 370 s
                         mixer 2 total time: 370 s
                         mixer 3 total time: 370 s
                     re-encrypt and permute BBS+ signatures time: 1500 s
                     generate encrypted blinded BBS+ signatures
                         mixer 0: generate encrypted blinding factors and proofs of knowledge of blinding factors time: 220 s
                         mixer 1: generate encrypted blinding factors and proofs of knowledge of blinding factors time: 220 s
                         mixer 2: generate encrypted blinding factors and proofs of knowledge of blinding factors time: 220 s
                         mixer 3: generate encrypted blinding factors and proofs of knowledge of blinding factors time: 220 s
                         mixer 0: verifying others' proofs of knowledge of blinding factors time: 660 s
                         mixer 1: verifying others' proofs of knowledge of blinding factors time: 660 s
                         mixer 2: verifying others' proofs of knowledge of blinding factors time: 660 s
                         mixer 3: verifying others' proofs of knowledge of blinding factors time: 660 s
                         status_pk_blrev: True
                         mixer 0: generate encrypted blinded BBS+ signatures time: 0.15 s
                         mixer 1: generate encrypted blinded BBS+ signatures time: 0.15 s
                         mixer 2: generate encrypted blinded BBS+ signatures time: 0.14 s
                         mixer 3: generate encrypted blinded BBS+ signatures time: 0.14 s
                         mixer 0 total time: 870 s
                         mixer 1 total time: 870 s
                         mixer 2 total time: 870 s
                         mixer 3 total time: 870 s
                     generate encrypted blinded BBS+ signatures time: 3500 s
                     decryption of blinded BBS+ signatures
                         mixer 0: obtain decryption shares time: 380 s
                         mixer 1: obtain decryption shares time: 380 s
                         mixer 2: obtain decryption shares time: 380 s
                         mixer 3: obtain decryption shares time: 380 s
                         mixer 0: verifying others' decryption shares time: 60 s
                         mixer 1: verifying others' decryption shares time: 60 s
                         mixer 2: verifying others' decryption shares time: 60 s
                         mixer 3: verifying others' decryption shares time: 60 s
                         mixer 0: combining decryption shares time: 0.44 s
                         mixer 1: combining decryption shares time: 0.47 s
                         mixer 2: combining decryption shares time: 0.43 s
                         mixer 3: combining decryption shares time: 0.44 s
                         status_decshares_blsigs_rev True
                         mixer 0 total time: 440 s
                         mixer 1 total time: 440 s
                         mixer 2 total time: 440 s
                         mixer 3 total time: 440 s
                     decryption of blinded BBS+ signatures time: 1800 s
                     mixer 0 total time: 1700 s
                     mixer 1 total time: 1700 s
                     mixer 2 total time: 1700 s
                     mixer 3 total time: 1700 s
                 get_blsigs_rev time: 6700 s
                 dpk_bbsplussig_nizkproofs
                     mixer 0: creating additive shares for delta0 time: 0.12 s
                     mixer 1: creating additive shares for delta0 time: 0.11 s
                     mixer 2: creating additive shares for delta0 time: 0.11 s
                     mixer 3: creating additive shares for delta0 time: 0.11 s
                     mixer 0: creating multiplicative shares for delta1 step 1 time: 0.0069 s
                     mixer 1: creating multiplicative shares for delta1 step 1 time: 0.0052 s
                     mixer 2: creating multiplicative shares for delta1 step 1 time: 0.0052 s
                     mixer 3: creating multiplicative shares for delta1 step 1 time: 0.0053 s
                     mixer 0: creating multiplicative shares for delta1 step 2 time: 0.027 s
                     mixer 1: creating multiplicative shares for delta1 step 2 time: 0.025 s
                     mixer 2: creating multiplicative shares for delta1 step 2 time: 0.024 s
                     mixer 3: creating multiplicative shares for delta1 step 2 time: 0.025 s
                     mixer 0: creating multiplicative shares for delta2 step 1 time: 0.0075 s
                     mixer 1: creating multiplicative shares for delta2 step 1 time: 0.0055 s
                     mixer 2: creating multiplicative shares for delta2 step 1 time: 0.0056 s
                     mixer 3: creating multiplicative shares for delta2 step 1 time: 0.0055 s
                     mixer 0: creating multiplicative shares for delta2 step 2 time: 0.027 s
                     mixer 1: creating multiplicative shares for delta2 step 2 time: 0.024 s
                     mixer 2: creating multiplicative shares for delta2 step 2 time: 0.024 s
                     mixer 3: creating multiplicative shares for delta2 step 2 time: 0.024 s
                     mixer 0: computing shares of z1 and proof of knowledge of their openings time: 27 s
                     mixer 1: computing shares of z1 and proof of knowledge of their openings time: 26 s
                     mixer 2: computing shares of z1 and proof of knowledge of their openings time: 26 s
                     mixer 3: computing shares of z1 and proof of knowledge of their openings time: 25 s
                     mixer 0: verifying others' proof of knowledge of openings of shares of z1 time: 150 s
                     mixer 1: verifying others' proof of knowledge of openings of shares of z1 time: 150 s
                     mixer 2: verifying others' proof of knowledge of openings of shares of z1 time: 150 s
                     mixer 3: verifying others' proof of knowledge of openings of shares of z1 time: 150 s
                     status_pk_z1: True
                     mixer 0: computing generators time: 360 s
                     mixer 1: computing generators time: 360 s
                     mixer 2: computing generators time: 360 s
                     mixer 3: computing generators time: 360 s
                     mixer 0: creating dpk_bbsplussig commit message time: 190 s
                     mixer 1: creating dpk_bbsplussig commit message time: 190 s
                     mixer 2: creating dpk_bbsplussig commit message time: 190 s
                     mixer 3: creating dpk_bbsplussig commit message time: 190 s
                     mixer 0: creating dpk_bbsplussig challenge time: 0.24 s
                     mixer 1: creating dpk_bbsplussig challenge time: 0.24 s
                     mixer 2: creating dpk_bbsplussig challenge time: 0.24 s
                     mixer 3: creating dpk_bbsplussig challenge time: 0.27 s
                     mixer 0: creating dpk_bbsplussig response message time: 0.021 s
                     mixer 1: creating dpk_bbsplussig response message time: 0.017 s
                     mixer 2: creating dpk_bbsplussig response message time: 0.018 s
                     mixer 3: creating dpk_bbsplussig response message time: 0.018 s
                     mixer 0 total time: 730 s
                     mixer 1 total time: 730 s
                     mixer 2 total time: 730 s
                     mixer 3 total time: 720 s
                 dpk_bbsplussig_nizkproofs time: 2900 s
                 dpk_bbsplussig_nizkverifs
                     verifier: verifying dpk_bbsplussig proofs time: 630 s
                     verifier total time: 630 s
                 dpk_bbsplussig_nizkverifs time: 630 s
                 status_dpk_bbsplussig: True
                 status_reverse_set_membership: True
                 mixer 0 total time: 2400 s
                 mixer 1 total time: 2400 s
                 mixer 2 total time: 2400 s
                 mixer 3 total time: 2400 s
                 verifier total time: 660 s
             reverse set membership time: 10000 s
             size of sender-uploaded input ciphertexts: 49.811601638793945 MB
             size of verifier-uploaded BB signatures: 0.30517578125 MB
             size of DPK_BBsig proofs: 3.8433074951171875 MB
             size of verifier-uploaded BBS+ signatures: 0.896453857421875 MB
             size of DPK_BBSPlusSig proofs: 11.043548583984375 MB
         main time: 17000 s
        ******** Worker 0 **********
        ---------------------------

##################################################################################################

B) To benchmark zksnarks-based set membership and reverse set membership proofs (in the single-prover setting), follow these steps:
        
        #1. Create the docker container from the given docker file:
        docker build -f Dockerfile_zksnark_sm_rsm -t zksnark-sm-rsm .

        #2. Open a shell inside the docker container:
        docker run -i -t zksnark-sm-rsm sh

        #3. Execute the code:
           # 0) Run this before running steps 1 and 2:
                PATH="/root/.zokrates/bin:${PATH}"
                
           # 1) For proving set-membership of a single commitment against a set of 10000 values 
           #    (This should report proving time in the range of about 2 seconds, which when scaled for 10000 proofs, takes about 20000 seconds.)
                ./run.sh sm 10000 poseidon
                
           # 2) For proving reverse set-membership of a single value against a set of 10000 commitments
           #    (This should report proving time in the range of about 2 seconds, which when scaled for 10000 proofs, takes about 20000 seconds.)
                ./run.sh rsm 10000 poseidon
           #
           # Note: You can also run the above set membership and reverse set membership proofs against the sha256 system as follows, which results
           # in much slower proving times (e.g., for a set of size 10, it takes about 1 minute to generate a single proof):
                ./run.sh sm 10 sha256
                ./run.sh rsm 10 sha256

The source code of our zksnark implementation is available at the `zksnark-sm-rsm` directory.
Sample reports using the Poseidon hash function are available at:
     set-membership: `sample-reports/report-groth16zksnark-poseidon-sm-n10000` (generating 1 proof against a set of size 10000)
     reverse set-membership: `sample-reports/report-groth16zksnark-poseidon-rsm-n10000` (generating 1 proof against a set of size 10000)

##################################################################################################

C) To benchmark cpsnark (Benarroch et al's scheme) for set membership (in the single-prover setting), follow these steps:
        
        #1. Create the docker container from the given docker file (note that this might take upwards of 600 seconds):
        docker build -f Dockerfile_cpsnark_sm -t cpsnark-sm .

        #2. Open a shell inside the docker container:
        docker run -i -t cpsnark-sm sh

        #3. Execute the code:
        cargo bench --bench membership_hash

The source code for this scheme is available at the `cpsnark-sm` directory (note that this is cloned from https://github.com/kobigurk/cpsnarks-set/ with a few minor arkworks import fixes).
A sample report is available at `sample-reports/report-benarroch-cpsnark-sm-n10000`. This shows a proving time of 221 ms for one set-membership proof, which when scaled to 10000 proofs, results in a total time of 2210 seconds, without including the time it takes to generate the RSA accumulator witness. 
