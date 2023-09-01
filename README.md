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
We also provide a report from a sample run of DB-SM and DB-RSM protocols for n=10000 ciphertexts and m=4 mix-servers at `sample-reports/report-db-sm-rsm-n10000-m4`

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
