# Benchmarks for Traceable Mixnets

This repository includes benchmarks for the PETS 2024 paper titled "Traceable mixnets" by Prashant Agrawal, Abhinav Nakarmi, Mahabir Prasad Jhanwar, Subodh Sharma and Subhashis Banerjee. Specifically, it contains the following items: 

- Source code for our implementation of the distributed zero-knowledge proofs (ZKPs) of set membership and reverse set membership (DB-SM and DB-RSM) shown respectively in Figures 8 and 9 of our paper. These ZKPs form the core building blocks of our traceable mixnet construction shown in Figure 7. 
- Source code for a zkSNARK implementation for set membership and reverse set membership in the single prover setting using Merkle accumulators. This is included to indirectly estimate the time required in producing distributed set membership and reverse set membership proofs via collaborative zkSNARKs [1]. In a collaborative zkSNARK, a set of provers each holding a share of the NP witness jointly prove knowledge of the witness. As per [1], a collaborative zkSNARK incurs a per-prover time that is roughly double the time taken by the corresponding single-prover zkSNARK. This thumbrule allows us to estimate the performance in a collaborative zkSNARK by implementing only a single-prover zkSNARK.
- Source code for the [official implementation](https://github.com/kobigurk/cpsnarks-set/tree/f8c7db66b7519b91dcda16caee6cb84949e8911b) of Benarroch et al.'s cpSNARK-Set [2] for set membership, with some minor changes. The cpSNARK-Set approach avoids the expensive hash computations inherent in a zkSNARK+Merkle accumulator based proof, but it works only for set membership and not reverse set membership. It also works only in the single-prover setting.

## Basic Requirements

### Hardware Requirements

The benchmarks were conducted on an Intel Xeon W-1270 machine with 3.40 GHz clock speed and 64 GB RAM, on a single core. Performance metrics reported here are specific to this configuration and may vary on different hardware. We recommend replicating these benchmarks on a similar hardware configuration for comparable timings, although the relative performance advantage of our approach over others should remain consistent across different hardware configurations. 

### Software Requirements

The host machine should be a Linux machine with git and docker installed. On a Ubuntu 22.04 machine, git can be installed by running `sudo apt install git`. Docker can be installed by following the official Docker Engine installation instructions [here](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository).

### Estimated Time and Storage Consumption

The expected overall time for all our experiments (experiments 1-3) is about 5 hours for our specific hardware setup. Storage and download requirements are approximately 4.2 GB for all our docker images combined. The experiments produce small plaintext reports on stdout and do not require any additional disk space.

## Environment

### Accessibility

The git tree contains source code for our DB-SM and DB-RSM proofs under directory `db-sm-rsm`, source code for the zkSNARK-based set membership and reverse set membership proofs under directory `zksnark-sm-rsm`, and source code for the cpSNARK-Set based set membership proof under directory `cpsnark-sm`. In addition, it contains sample reports containing our experiment outputs on our test hardware setup under directory `sample-reports` and Dockerfiles for each of our experiments at the top-level. We use these Dockerfiles to build the following Docker images and publish them on [Docker Hub](https://hub.docker.com/):

- image `tmpets/db-sm-rsm:v1` for experiment 1 (running our DB-SM and DB-RSM proofs) 
- image `tmpets/zksnark-sm-rsm:v1` for experiment 2 (running single-prover set membership and reverse set membership proofs using Merkle tree based zkSNARKs) 
- image `tmpets/cpsnark-sm:v1` for experiment 3 (running single-prover set membership proof based on Benarroch et al.'s cpSNARK-Set approach). 

*Structure of Docker images:* The `tmpets/db-sm-rsm:v1` image is built from the `Dockerfile_db_sm_rsm` file. It contains a copy of the source code directory `db-sm-rsm` at location `/app/db-sm-rsm` inside the image, which is the default working directory from which container commands are executed. Similar structure is followed for images `tmpets/zksnark-sm-rsm:v1` and `tmpets/cpsnark-sm:v1` too.

### Set up the environment via Docker (recommended)

Set up simply requires pulling our Docker images from Docker Hub. If you are behind a proxy server, this would require [additional proxy configuration](https://docs.docker.com/config/daemon/systemd/#httphttps-proxy) for the Docker daemon. The expected correct output for this step is the standard Docker output showing various layers of the Docker images being fetched. Once these images are pulled, no additional content needs to be downloaded. 

```bash
sudo docker pull tmpets/db-sm-rsm:v1  
sudo docker pull tmpets/zksnark-sm-rsm:v1
sudo docker pull tmpets/cpsnark-sm:v1
```

### Manual set up on the host environment (without Docker)

If you want to install the benchmarks on your local system without Docker, we also provide install scripts for Ubuntu. Each of `db-sm-rsm`, `zksnark-sm-rsm` and `cpsnark-sm` directories contain an `install.sh` script that sets up the dependencies for you. 

#### Setting up `db-sm-rsm`

Ensure that you have `python3.7` installed on your system and it is in the path. Verify the contents of the `db-sm-rsm/install.sh` file. The script installs GMP, PBC, OpenSSL and Charm libraries to `/usr/local/lib`. Modify as per your host system setup and run:

```bash
cd db-sm-rsm
./install.sh
```

After installation, place the following commands in an appropriate `.bashrc` file to ensure that the environment variables defined below are available whenever the `db-sm-rsm` benchmarks are run:

```bash
export LIBRARY_PATH=/usr/local/lib
export LD_LIBRARY_PATH=/usr/local/lib
export LIBRARY_INCLUDE_PATH=/usr/local/include
```

#### Setting up `zksnark-sm-rsm`

Ensure that you have `python3.7` installed on your system and it is in the path. Verify the contents of the `zksnark-sm-rsm/install.sh` file. The script installs ZoKrates. Modify as per your host system setup and run:

```bash
cd zksnark-sm-rsm
./install.sh
```

After installation, place the following commands in an appropriate `.bashrc` file to ensure that the PATH environment variable is updated to include the PATH to the ZoKrates installation directory.

```bash
export PATH="${HOME}/.zokrates/bin:${PATH}"
```

#### Setting up `cpsnark-sm`

Verify the contents of the `cpsnark-sm/install.sh` file. The script installs Rust and other dependencies for the Bennarroch et al. scheme. Modify as per your host system setup and run:

```bash
cd cpsnark-sm
./install.sh
```

After installation, place the following commands in an appropriate `.bashrc` file to ensure that the PATH environment variable is updated to include the PATH to the Rust build tool `cargo`.

```bash
source "$HOME/.cargo/env"
export PATH="${HOME}/.cargo/bin:${PATH}"
```

### Testing the Environment

The steps to test the environment for each of our experiments are detailed below. These steps should finish within a few seconds.

#### Test experiment 1

Test a basic DB-SM and DB-RSM proof where the set size is 10 and the mixnet consists of 2 mix-servers (the `precomputing=0` option skips precomputation steps that provide overall efficiency gains only for larger benchmarks): 
```bash
sudo docker run -it tmpets/db-sm-rsm:v1 /bin/bash # run in the host shell to launch a container shell
precomputing=0 python db_sm_rsm.py 10 2 # run in the container shell
# (type `exit` or `Ctrl+D` to exit out of the container shell)
```
Note: In case of a manual install on the host system, simply execute `precomputing=0 python db_sm_rsm.py 10 2` from the `db-sm-rsm` directory.

The expected outcome is an output detailing the verification status and time taken by various steps of the proofs, such that all `status_*` entries are `True`.

#### Test experiment 2

Test a basic single-prover set membership zkSNARK where the set size is 10 and the hash function used for computing the Merkle tree is the Poseidon hash function: 
```bash
sudo docker run -it tmpets/zksnark-sm-rsm:v1 /bin/bash # run in the host shell to launch a container shell
./run.sh sm 10 poseidon # run in the container shell
```
Note: In case of a manual install on the host system, simply execute `./run.sh sm 10 poseidon` from the `zksnark-sm-rsm` directory.

The expected outcome is an output containing a string `PASSED` under section `VERIFIER`.

#### Test experiment 3

Test whether the dependencies for experiment 3 are ready for use:
```bash
sudo docker run -it tmpets/cpsnark-sm:v1 /bin/bash # run in the host shell to launch a container shell
cargo bench --no-run --bench membership_hash # run in the container shell
```
Note: In case of a manual install on the host system, simply execute `cargo bench --no-run --bench membership_hash` from the `cpsnark-sm` directory.

The expected outcome is an output containing strings like `Finished bench [optimized] target(s) in 0.06s` and `Executable benches/membership_hash.rs (target/release/deps/membership_hash-3a2eac78eb554c7e)`.

## Artifact Evaluation

We now provide instructions to reproduce the results mentioned in the paper. Our instructions and reported numbers are specifically for the case of $n=10^$ ciphertexts in the mixnet input list and $m=4$ mix-servers (see Figure 10 - column for $m=4$ and $n=10^4$ in the top table and detailed breakdown in the bottom table). Values for other settings can be similarly obtained. 

### Main Results and Claims

#### Main Result 1: Our distributed set membership proof is faster than state-of-the-art collaborative zkSNARKs by ~86x 

The per-prover time in our distributed set membership proof for $10000$ ciphertexts against a set of $10000$ plaintexts is $500$ seconds (row "DB-SM - $M_k$"; supported by experiment 1), whereas the estimated per-prover time in a collaborative zkSNARK for $10000$ proofs is $43400$ seconds (row "collab-zkSNARK-SM"; supported by experiment 2). This makes our approach conservatively $43400/500=86\times$ faster than collaborative zkSNARKs (we do not count the time taken by collaborative zkSNARKs to generate and secret-share SNARK witnesses). Further, the estimated prover time in a single-prover cpSNARK-Set set membership proof is $2200$ seconds for $10000$ proofs --- without including the time taken to generate the membership witness (Section 6 - last para; supported by experiment 3).

#### Main Result 2: Our distributed reverse set membership proof is faster than state-of-the-art collaborative zkSNARKs by ~18x

The per-prover time in our distributed reverse set membership proof for $10000$ plaintexts against a set of $10000$ ciphertexts is $2400$ seconds (row "DB-RSM - $M_k$"; supported by experiment 1), whereas the estimated per-prover time in a collaborative zkSNARK for $10000$ proofs is $43400$ seconds (row "collab-zkSNARK-RSM"; supported by experiment 2). This makes our approach conservatively $43400/2400=18\times$ faster. The cpSNARK-Set approach of experiment 3 does not work for reverse set membership.

*Note:* The specific times mentioned above are corresponding to our test hardware setup and sample reports, but the relative performance advantage of our approach is expected to remain consistent across different hardware configurations.

### Experiments

#### Experiment 1: Running our DB-SM and DB-RSM proofs

*Experiment description:* The goal of this experiment is to estimate the runtime query performance of our $\mathsf{BTraceIn}$ and $\mathsf{BTraceOut}$ queries. Towards this end, we setup mixnet keys as per the $\mathsf{Keygen}$ protocol of Figure 7, create $n=10000$ ciphertexts as per the $\mathsf{Enc}$ algorithm, mix these ciphertexts as per the $\mathsf{Mix}$ protocol involving $m=4$ mix-servers, and then run $a)$ a worst-case DB-SM query with these mix-servers for all input ciphertexts against the set of all output plaintexts ($I=J=[n]$) and $b)$ a worst-case DB-RSM query for all output plaintexts against the set of all input ciphertexts ($I=J=[n]$). We also implement all the steps proposed in Appendix B to evaluate performance in the realistic malicious security model. As per Figure 7, the worst-case runtime performance for our $\mathsf{BTraceIn}$ and $\mathsf{BTraceOut}$ queries, without any additional optimizations, would be twice the performance of the DB-SM and DB-RSM queries respectively.

*Running the experiment:*
```bash 
sudo docker run -it tmpets/db-sm-rsm:v1 /bin/bash # run in the host shell to launch a container shell
python db_sm_rsm.py 10000 4 # run in the container shell
```

Since the above command is a long-running one, it may be desirable to run it in background and fetch the results later. This can be done by running the following commands on the host shell:
```bash
sudo docker run -dt tmpets/db-sm-rsm:v1 /bin/bash # start a fresh container process in background; note down the container-id printed as output.
sudo docker exec -dt <container-id> /bin/bash -c "python db_sm_rsm.py 10000 4 &> report-db-sm-rsm-n10000-m4.txt" # start the experiment process in background
sudo docker exec -it <container-id> /bin/bash -c "cat report-db-sm-rsm-n10000-m4.txt" # monitor the process output
sudo docker cp <container-id>:/app/db-sm-rsm/report-db-sm-rsm-n10000-m4.txt . # copy the output report from the container to the host machine
sudo docker container stop <container-id> # stop the container
```

*Expected duration:* ~5 hours

*Expected disk space:* 1.05 GB (size of image `tmpets/db-sm-rsm:v1`)

*Expected output:* A report containing detailed timing, sizing and verification status information for our DB-SM and DB-RSM protocols (sample report at `sample-reports/report-db-sm-rsm-n10000-m4` in the git tree). The output is divided into the following sections: `preprocessing` (for input-independent setup steps run by the mix-servers), `input preparation/checking inputs` (for creation of sender ciphertexts and verification by the mix-servers that the senders indeed created them), `mixing` (for the $\mathsf{Mix}$ protocol among the mix-servers), `forward set membership` (for the DB-SM protocol between the mix-servers and the verifier/querier) and `reverse set membership` (for the DB-RSM protocol between the mix-servers and the verifier/querier). Within each section, entries labelled `mixer X .... time` for any `X` = 0, 1, 2 or 3 (resp. `verifier ... time`) denote time taken by each mix-server (resp. verifier) in individual steps, entries labelled `mixer X total time` (resp. `verifier total time`) represent aggregation of these individual step times, and entries labelled `status_...` denote verification statuses of proofs such that value `True` means that the proof was accepted by the verifier. Entries labelled `size of ...` denote sizes of various published outputs.

*Steps to verify the claimed results:*

1. Verify that entry `forward set membership -> mixer X total time` matches the per-prover time in the row titled "DB-SM - $M_k$" in the top table of Figure 10 (here and henceforth, assume `X` = 0, 1, 2 or 3). This verification directly supports main result 1. Verify that entry `forward set membership -> verifier time` matches the verifier time reported in the row titled "DB-SM - $Q$" of the same table. 
2. Verify that entry `reverse set membership -> mixer X total time` matches the per-prover time in the row titled "DB-RSM - $M_k$". This verification directly supports main result 2. Verify that entry `reverse set membership -> verifier time` matches the verifier time reported in the row titled "DB-RSM - $Q$". 
3. Verify that entry `mixing -> mixer X total time` matches the mixing time reported in Figure 10.
4. Verify that the following entries in section `forward set membership` match the corresponding values reported in the DB-SM section of Figure 10: 

    | Entry in the experiment output | Entry in DB-SM section of Figure 10 |
    | ------------------------------ | ----------------------------------- |
    |`get_verfsigs -> verifier total time`  | $(Q)$ Generating $n$ BB signatures/encryptions |
    |`check_verfsigs -> mixer X total time` | $(M_k)$ Verifying $n$ BB signatures/encryptions | 
    |`get_blsigs -> re-encrypt and reverse permute BB signatures -> reencrypting encrypted BB signatures time` | $(M_k)$ Re-encryption of encrypted signatures | 
    |`get_blsigs -> re-encrypt and reverse permute BB signatures ->`  `creating proof of shuffle of encrypted BB signatures time` + `verifying others' proofs of shuffle of encrypted BB signatures time` | $(M_k)$ Proof-of-shuffle of encrypted signatures | 
    |`get_blsigs -> generate encrypted blinded BB signatures -> mixer X total time` | $(M_k)$ Homomorphic blinding of encrypted signatures |
    |`get_blsigs -> decrypt blinded signatures -> mixer X total time` | $(M_k)$ Threshold decryption of encrypted signatures |
    |`dpk_bbsig_nizkproofs -> mixer X total time`  | $(M_k)$ Generating $n$ DPK proofs for $p_{BB}$ |
    |`dpk_bbsig_nizkverifs -> verifier total time` | $(Q)$ Verifying $n$ DPK proofs for $p_{BB}$ |

5. Verify that the following entries in section `reverse set membership` match the corresponding values reported in the DB-RSM section of Figure 10: 

    | Entry in the experiment output | Entry in the DB-RSM section of Figure 10 |
    | ------------------------------ | ---------------------------------------- |
    |`pkcommverifs -> verifier total time` | $(Q)$ Verifying $n$ PoKs of commitments |
    |`get_verfsigs_rev -> verifier total time`  | $(Q)$ Generating $n$ BBS+ quasi-signatures | 
    |`check_verfsigs_rev -> mixer X total time` | $(M_k)$ Verifying $n$ BBS+ quasi-signatures/encryptions | 
    |`get_blsigs_rev -> re-encrypt and permute BBS+ signatures -> reencrypting encrypted BBS+ signatures time` | $(M_k)$ Re-encryption of encrypted signatures |
    |`get_blsigs_rev -> re-encrypt and permute BBS+ signatures ->` `creating proof of shuffle of encrypted BBS+ signatures time`+`verifying others' proofs of shuffle of encrypted BBS+ signatures time` | $(M_k)$ Proof-of-shuffle of encrypted signatures |
    |`get_blsigs_rev -> generate encrypted blinded BBS+ signatures -> mixer X total time` | $(M_k)$ Homomorphic blinding of encrypted signatures |
    |`get_blsigs_rev -> decryption of blinded BBS+ signatures -> mixer X total time` | $(M_k)$ Threshold decryption of encrypted signatures |
    |`dpk_bbsplussig_nizkproofs -> mixer X total time` | $(M_k)$ Generating $n$ DPK proofs for $p_{BBS+}$ |
    |`dpk_bbsplussig_nizkverifs -> verifier total time` | $(Q)$ Verifying $n$ DPK proofs for $p_{BBS+}$ |

6. Verify that the values of all `status_` entries are `True`, denoting that all proofs actually passed.
7. Verify that the values of the `size of ...` entries match the sizes reported in Figure 10.

*Additional notes:*

* In the honest-but-curious (HBC) case, the mix-servers do not need to perform any steps related to verification of signatures, or proving or verifying correctness of shuffles, knowledge of correct blinding factors and correctness of threshold decryption. The reported HBC numbers can be obtained by appropriately skipping these steps from the generated report.
* We do not report sender costs to create ciphertexts and mixnet costs to check them because these steps do not affect runtime query performance and can be executed as and when individual senders send their data. However, this information is available under the `input preparation` and `checking inputs` sections of the output.
* We also do not implement distributed key generation during $\mathsf{Keygen}$ because this is a one-time setup step that can be executed by the mix-servers ahead of time and does not affect runtime query performance. For the same reason, we do not report preprocessing time, but this information is available under the `preprocessing` section of the output.
* In our implementation, we run the steps executed by each mix-server sequentially one after the other. Thus, although the total runtime of our experiment incurs the per-mix-server cost 4 times, in a real deployment, most of the bulky steps like proofs of shuffle, homomorphic blinding, threshold decryption, and the DPKs of stage 2 would be executed by each mix-server in parallel and therefore per-mix-server times capture real-world latencies more accurately. The only sequential operation is re-encryption, whose time is a miniscule (~0.01) fraction of the time taken in these other steps (see entries `mixing -> mixer X: re-encryption time`, `forward set membership -> mixer X: reencrypting encrypted BB signatures time` and `reverse set membership -> mixer X: reencrypting encrypted BBS+ signatures time`).
* Although the verification times in our proofs are more than the very competitive verification times in zkSNARKs (see experiment 2), they are still a miniscule (<0.03) fraction of the zkSNARK prover times and thus our approach still offers drastic savings in overall latencies.
* We used the [BN254 elliptic curve](https://hackmd.io/@jpw/bn254) in our experiments. Since [recent attacks](https://eprint.iacr.org/2015/1027.pdf) have reduced the security of this curve to around 100-110 bits (as per [this](https://github.com/zcash/zcash/issues/2502) and [this](https://hackmd.io/@jpw/bn254) report), a popular secure alternative [providing an adequate 117-120 bit security is BLS12-381](https://hackmd.io/@benjaminion/bls12-381). However, our chosen [Charm cryptographic library](https://github.com/JHUISI/charm) does not support this curve. Nevertheless, given the extensive performance comparison between BN254 and BLS12-381 done [here](https://hackmd.io/@gnark/eccbench) and given that elliptic curve operations get involved only in our DPKs of stage 2, we expect that the performance impact of switching to BLS12-381 would be within 2x for these DPKs and thus ~1.3x for our overall per-prover times.

#### Experiment 2: Running zkSNARK-based single-prover set membership and reverse set membership proofs

*Experiment description:* The goal of this experiment is to estimate the performance of a set membership and reverse set membership proof using a Merkle accumulator-based zkSNARK. This is a single-prover proof, but the rationale for running this experiment is to indirectly estimate the performance of a collaborative zkSNARK by doubling the prover time in the single-prover zkSNARK. Towards this end, we created a set membership zkSNARK for statement $\rho_{SM-Acc}$ (see Section 1.2.4) by creating a Merkle tree for the set of plaintexts and a reverse set membership zkSNARK for statement $\rho_{RSM-Acc}$ by creating a Merkle tree for the set of ciphertexts (commitments). The latter requires proving arithmetic relationships about elements in the commitment space, for which we used the Baby Jubjub curve. The hash function for the Merkle tree was chosen as the Poseidon hash function, which is specially optimised for use in zkSNARKs. The experiment runs set membership proof for a single ciphertext against a set of $10000$ plaintexts and reverse set membership proof for a single plaintext against a set of $10000$ ciphertexts. All our zkSNARKs are created using the [ZoKrates toolchain](https://zokrates.github.io/) and the [Groth16 proof system](https://eprint.iacr.org/2016/260).

*Running the experiment:*
```bash
sudo docker run -it tmpets/zksnark-sm-rsm:v1 /bin/bash # run in the host shell to launch a container shell
./run.sh sm 10000 poseidon # run in the container shell - set membership proof
./run.sh rsm 10000 poseidon # run in the container shell - reverse set membership proof
```

*Expected duration:* ~1 minute for each of the two proofs

*Expected disk space:* 240 MB (size of image `tmpets/zksnark-sm-rsm:v1`)

*Expected output:* A report detailing the timings in various stages of both set membership and reverse set membership zkSNARKs (sample reports at `sample-reports/report-zksnark-sm-n10000-groth16-poseidon` and `sample-reports/report-zksnark-rsm-n10000-groth16-poseidon` in the git tree). In each zkSNARK, the output is divided into the following sections: `COMPUTATION` (prover steps required to create a Merkle tree and find the Merkle path to the claimed member), `TRUSTED SETUP` (trusted setup steps specific to the ZK circuit), `PROVER` (prover steps for generating the noninteractive zkSNARK proof) and `VERIFIER` (verifier steps for verifying the proof). 

*Steps to verify the claimed results:*

1. Verify that the prover time printed against the `user` entry in the `PROVER` section is around 2.17 seconds, both for set membership and reverse set membership. When scaled to proofs for 10000 ciphertexts (for set membership) and 10000 plaintexts (for reverse set membership), this results in a total prover time of 21700 seconds. Such direct scaling is sufficient to estimate the performance for $n$ proofs for these generic proof systems. Thus, as per [1], the time taken by collaborative zkSNARKs is estimated to be $2*21700=43400$ seconds, which matches the row titled ``collab-zkSNARK-SM''. This verification thus directly supports main results 1 and 2.
2. Verify that the verifier time printed against the `user` entry in the `VERIFIER` section is around 0.005 seconds, both for set membership and reverse set membership. When scaled to proofs for 10000 ciphertexts/plaintexts, this results in a total verifier time of 50 seconds, which match the verifier times reported in the text of Section 6 - ``Comparison''.
3. Verify that the string `PASSED` is printed in the `VERIFIER` section, denoting that the proofs actually passed.

*Additional notes:*

* When we scale the above proofs for $n$ ciphertexts/plaintexts against the same set, the `Time __init__` cost under `COMPUTATION` (representing the cost to create the Merkle tree) gets added as a one-time cost and the `Time get_auth_path` costs (representing the cost to find the Merkle path) gets multiplied by $n$. This results in a small ~35 seconds overhead over 21700 seconds, which we ignore. The cost under the `TRUSTED SETUP` section only depends on the ZK circuit and not on the inputs, so we ignore this too. 

#### Experiment 3: Running cpSNARK-Set based single-prover set membership proofs

*Experiment description:* The goal of this experiment is to estimate the time taken by Benarroch et al.'s cpSNARK-Set scheme. This scheme is also a single-prover scheme but it only allows proving set membership and not reverse set membership. For this experiment, we use the scheme's [official implementation](https://github.com/kobigurk/cpsnarks-set/tree/f8c7db66b7519b91dcda16caee6cb84949e8911b) that provides a benchmark to estimate the prover and verifier times in a single set membership proof. The scheme is based on RSA accumulators where the prover and verifier times are independent of the size of the set; therefore this benchmark only estimates these times for a dummy set of 3 elements. 

Additionally, the benchmark only estimates the time taken by the prover to compute the proof *given a membership witness*, but it does not include the time taken to generate such a witness. We, therefore, add an additional benchmark to this implementation to estimate the time taken by the prover to generate a single membership witness for a set of size 10000. 

*Running the experiment:*
```bash
sudo docker run -it tmpets/cpsnark-sm:v1 /bin/bash # run in the host shell to launch a container shell
cargo bench --bench membership_hash # run in the container shell - set membership proof
```

*Expected duration:* ~2-3 minutes

*Expected disk space:* 2.74 GB (size of image `tmpets/cpsnark-sm:v1`)

*Expected output:* A report detailing the results of all the benchmarks (sample report at `sample-reports/report-benarroch-cpsnark-sm-n10000` in the git tree). The output is divided into three sections: `membership_hash protocol proving` benchmarking the prover time in generating the proof given a membership witness, `membership_hash protocol verification` benchmarking the verifier time in verifying the proof, and `membership_hash creating witness` benchmarking the prover time in generating the membership witness. The timing in each section is reported in entries like `time:   [224.50 ms 225.77 ms 227.38 ms]` where the middle entry denotes the mean value over about a 100 sample runs and the other entries together denote its variance.

*Steps to verify the claimed results:*

1. Verify that the mean prover time in section `membership_hash protocol proving` is around 220 ms. This supports main result 1 since the prover time when scaled to 10000 ciphertexts is 2200 s.
2. Verify that the mean verifier time in section `membership_hash protocol verification` is around 31 ms. When scaled to 10000 ciphertexts, this would be 310 s, which is still higher than our 210 s (row ``DB-SM - $Q$'') for the distributed case.
3. Verify that the mean prover time in section `membership_hash creating witness` is around 783 ms. This reflects the $O(n)$ witness computation operation in RSA accumulators, where $n$ is the size of the set (see the additional benchmark `membership_hash creating witness` in file `cpsnark-sm/benches/membership_hash.rs`). Although we do not report this, this witness generation time when scaled to 10000 ciphertexts results in an overhead of 7830 s, which combined with the proof generation time in step 1 results in a total prover time of 10030 seconds in comparison to our 500 seconds (a 20x improvement) for the distributed case.

*Additional notes:*

* We ignore the cost of creating the accumulator and of hashing set values to prime numbers in this approach, since these are one-time costs.
* We do not run the `membership_prime` benchmark also provided in the official implementation, because this is for the special case when set elements are prime numbers and is not applicable for our general use-case.
* In addition to the additional benchmark for measuring witness creation time, we also include some minor bugfixes to the official implementation, as detailed in `cpsnark-sm/README.md`.

## References

- [1] Ozdemir and Boneh, *Experimenting with Collaborative zk-SNARKs: Zero-Knowledge Proofs for Distributed Secrets*, https://eprint.iacr.org/2021/1530.pdf
- [2] Benarroch, Campanelli, Fiore, Gurkan and Kolonelos, *Zero-Knowledge Proofs for Set Membership: Efficient, Succinct, Modular*, https://eprint.iacr.org/2019/1255.pdf 
- [3] Damgard and Koprowski, *Practical Threshold RSA Signatures Without a Trusted Dealer*, https://iacr.org/archive/eurocrypt2001/20450151.pdf
