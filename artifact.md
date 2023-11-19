# Artifact Appendix

Paper title: **Traceable Mixnets** <!--**Enter the title of your paper here**-->

Artifacts HotCRP Id: **#7** <!--**#Enter your HotCRP Id here**-->

Requested Badge: **Reproducible** <!--Either **Available** or **Reproducible**-->

## Description
<!--A short description of your artifact and how it links to your paper.-->

This artifact includes the following items: 

- Source code for our implementation of the distributed zero-knowledge proofs (ZKPs) of set membership and reverse set membership (DB-SM and DB-RSM) shown respectively in Figures 8 and 9 of our paper. These ZKPs form the core building blocks of our traceable mixnet construction shown in Figure 6. 
- Source code for a zkSNARK implementation for set membership and reverse set membership in the single prover setting using Merkle accumulators. This is included to indirectly estimate the time required in producing distributed set membership and reverse set membership proofs via collaborative zkSNARKs [1]. In a collaborative zkSNARK, a set of provers each holding a share of the NP witness jointly prove knowledge of the witness. As per [1], a collaborative zkSNARK incurs a per-prover time that is roughly double the time taken by the corresponding single-prover zkSNARK.
- Source code for the [official implementation](https://github.com/kobigurk/cpsnarks-set/tree/f8c7db66b7519b91dcda16caee6cb84949e8911b) of Benarroch et al.'s cpSNARK-Set [2] for set membership, with minor import fixes. This approach avoids the expensive hash computations inherent in a zkSNARK+Merkle tree based proof, but it works only for set membership and not reverse set membership. It also works only in the single-prover setting.


<!-- We actually also include mixing and encryption phases. Also emphasise that this implementation includes the malicious security steps mentioned in the paper. -->

<!-- Goal of this document: how our experiment corroborates the claims made in the paper. Non-goals: why the claims made in the paper are sensible. -->

### Security/Privacy Issues and Ethical Concerns
<!--If your artifacts hold any risk to the security or privacy of the reviewer's machine, specify them here, e.g., if your artifacts require a specific security mechanism, like the firewall, ASLR, or another thing, to be disabled for its execution.
Also, emphasize if your artifacts contain malware samples, or something similar, to be analyzed.
In addition, you must highlight any ethical concerns regarding your artifacts here.-->

For simplicity, our instructions below are written such that Docker needs to be run as a superuser. 

<!-- If you do not wish to run Docker as a superuser, follow the instructions [here](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user). -->

## Basic Requirements
<!--Describe the minimal hardware and software requirements of your artifacts and estimate the compute time and storage required to run the artifacts.-->

### Hardware Requirements
<!--If your artifacts require specific hardware to be executed, mention that here.
Provide instructions on how a reviewer can gain access to that hardware through remote access, buying or renting, or even emulating the hardware.
Make sure to preserve the anonymity of the reviewer at any time.-->

The benchmarks should be run on an Intel x86-based machine (we have tested on a local Intel Xeon W-1270 machine with clock speed 3.40 GHz and 64 GB RAM). A single core is sufficient. 

### Software Requirements
<!--Describe the OS and software packages required to evaluate your artifact.
This description is essential if you rely on proprietary software or software that might not be easily accessible for other reasons.
Describe how the reviewer can obtain and install all third-party software, data sets, and models.-->

The host machine should be a Linux machine with git and docker installed. On a Ubuntu 22.04 machine, git can be installed by running `sudo apt install git`. Docker can be installed by following the official Docker Engine installation instructions [here](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository).

### Estimated Time and Storage Consumption
<!--Provide an estimated value for the time the evaluation will take and the space on the disk it will consume. 
This helps reviewers to schedule the evaluation in their time plan and to see if everything is running as intended.
More specifically, a reviewer, who knows that the evaluation might take 10 hours, does not expect an error if,  after 1 hour, the computer is still calculating things.-->

The expected overall time for all our experiments (experiments 1-3) is about 5 hours. Storage and download requirements are about 4.2 GB for all our docker images. The experiments produce small plaintext reports on stdout and do not require any additional disk space.

## Environment
<!--In the following, describe how to access your artifact and all related and necessary data and software components.
Afterward, describe how to set up everything and how to verify that everything is set up correctly.-->

### Accessibility
<!--Describe how to access your artifacts via persistent sources.
Valid hosting options are institutional and third-party digital repositories.
Do not use personal web pages.
For repositories that evolve over time (e.g., Git Repositories ), specify a specific commit-id or tag to be evaluated.
In case your repository changes during the evaluation to address the reviewer's feedback, please provide an updated link (or commit-id / tag) in a comment.-->

Get the artifact source code from git:

```bash
git clone https://github.com/agrawalprash/traceable-mixnets.git
cd traceable-mixnets
```

We have published the following Docker images on [Docker Hub](https://hub.docker.com/): 

- image `tmpets/db-sm-rsm` for experiment 1 (running our DB-SM and DB-RSM proofs) 
- image `tmpets/zksnark-sm` for experiment 2 (running single-prover set membership and reverse set membership proofs using Merkle tree based zkSNARKs) 
- image `tmpets/cpsnark-sm` for experiment 3 (running single-prover set membership proof based on Benarroch et al.'s cpSNARK-Set approach). 

### Set up the environment
<!--Describe how the reviewers should set up the environment for your artifacts, including download and install dependencies and the installation of the artifact itself.
Be as specific as possible here.
If possible, use code segments to simply the workflow, e.g.,

```bash
git clone git@my_awesome_artifact.com/repo
apt install libxxx xxx
```

Describe the expected results where it makes sense to do so.-->

Set up simply requires pulling our Docker images from Docker Hub. If you are behind a proxy server, this would require [additional proxy configuration](https://docs.docker.com/config/daemon/systemd/#httphttps-proxy) for the Docker daemon. Once these images are pulled, no additional content needs to be downloaded. 

```bash
sudo docker pull tmpets/db-sm-rsm  
sudo docker pull tmpets/zksnark-sm-rsm
sudo docker pull tmpets/cpsnark-sm
```

Note that the `tmpets/db-sm-rsm` image is built from the `Dockerfile_db_sm_rsm` file at the top-level of the git tree. It contains a copy of the source code directory `db-sm-rsm` at location `/app/db-sm-rsm` inside the image, which is the default working directory from which container commands are executed. Similar structure is followed for images `tmpets/zksnark-sm-rsm` and `tmpets/cpsnark-sm` too.


### Testing the Environment
<!--Describe the basic functionality tests to check if the environment is set up correctly.
These tests could be unit tests, training an ML model on very low training data, etc.
If these tests succeed, all required software should be functioning correctly.
Include the expected output for unambiguous outputs of tests.
Use code segments to simplify the workflow, e.g.,
```bash
python envtest.py
```-->

The steps to test the environment for each of the experiments are detailed below. These steps should finish within a few seconds.

#### Test experiment 1

Test a basic DB-SM and DB-RSM proof where the set size is 10 and the mixnet consists of 2 mix-servers (the `precomputing=0` option skips precomputation steps that provide overall efficiency gains only for larger benchmarks): 
```bash
sudo docker run -it tmpets/db-sm-rsm /bin/bash # run in the host shell to launch a container shell
precomputing=0 python db_sm_rsm.py 10 2 # run in the container shell
# (type `exit` or `Ctrl+D` to exit out of the container shell)
```
The expected outcome is an output detailing the verification status and time taken by various steps of the proofs, such that all `status_*` entries are `True`.

#### Test experiment 2

Test a basic single-prover set membership zkSNARK where the set size is 10 and the hash function used for computing the Merkle tree is the Poseidon hash function: 
```bash
sudo docker run -it tmpets/zksnark-sm-rsm /bin/bash # run in the host shell to launch a container shell
./run.sh sm 10 poseidon # run in the container shell
```
The expected outcome is an output containing a string `PASSED` under section `VERIFIER`.

#### Test experiment 3

Test whether the dependencies for experiment 3 are ready and available:
```bash
sudo docker run -it tmpets/cpsnark-sm /bin/bash # run in the host shell to launch a container shell
cargo bench --no-run --bench membership_hash # run in the container shell
```
The expected outcome is an output containing strings like `Finished bench [optimized] target(s) in 0.06s` and `Executable benches/membership_hash.rs (target/release/deps/membership_hash-3a2eac78eb554c7e)`.

## Artifact Evaluation
<!--This section includes all the steps required to evaluate your artifact's functionality and validate your paper's key results and claims.
Therefore, highlight your paper's main results and claims in the first subsection. And describe the experiments that support your claims in the subsection after that.-->

### Main Results and Claims
<!--List all your paper's main results and claims that are supported by your submitted artifacts.-->

#### Main Result 1: Our distributed set membership proof is faster than state-of-the-art collaborative zkSNARKs by ~86x 
<!--Describe the results in 1 to 3 sentences.
Refer to the related sections in your paper and reference the experiments that support this result/claim.-->
The per-prover time in our distributed set membership proof for $10000$ ciphertexts against a set of $10000$ plaintexts is $500$ seconds (Figure 11 row 1; supported by experiment 1), whereas the prover time in a single-prover set membership zkSNARK for $10000$ proofs is $21700$ seconds (Figure 11 row 2; supported by experiment 2). This allows us to estimate the corresponding per-prover time in a collaborative zkSNARK as $2\times 21700 = 43400$ seconds without including the time taken to generate and secret-share the SNARK witness among the provers, which makes our approach conservatively $43400/500=83\times$ faster (Section 6.2 - para 3). Further, the estimated prover time in a single-prover set membership proof using cpSNARK-Set is $2200$ seconds for $10000$ proofs, without including the time taken to generate the membership witness (Section 6.2 - para 4; supported by experiment 3).



<!-- prover time in a single-prover zkSNARK set membership proof for $1$ ciphertext against a set of $10000$ plaintexts is 2.17 seconds, which scales to $21700$ seconds for $10000$ ciphertexts (experiment 2; Figure 11 row 2). Since it is claimed in [1] that the per-prover time in a *distributed* ("collaborative") zkSNARK is roughly twice the prover time in a single-prover zkSNARK for the same statement, the estimated per-prover time in proving set membership of $10000$ ciphertexts via collaborative zkSNARKs is $43400$ seconds, which makes our implementation roughly $43400/500 = 86\times$ faster than collaborative zkSNARKs (Section 6.2 - para 3). This estimate is conservative, because we do not count the time taken to generate the secret shares of the prover's witness in the collaborative zkSNARK approach. -->

<!-- Further, the prover time in a single-prover cpSNARK-Set approach is $0.221$ seconds for $1$ ciphertext and a set of $10000$ plaintexts, which scales to $2210$ seconds for $10000$ ciphertexts (Section 6.2 - para 4). This number assumes the membership witness is given to the prover and does not count the time taken for *generating* the witness, which is an $O(n)$ operation in itself, and therefore this timing is not directly comparable to our scheme. -->

#### Main Result 2: Our distributed reverse set membership proof is faster than state-of-the-art collaborative zkSNARKs by ~18x
<!--...-->

The per-prover time in our distributed reverse set membership proof for $10000$ plaintexts against a set of $10000$ ciphertexts is $2400$ seconds (Figure 11 row 3; supported by experiment 1), whereas the prover time in a single-prover reverser set membership zkSNARK is $21700$ seconds (Figure 11 row 4; supported by experiment 2). This allows us to estimate the corresponding per-prover time in a collaborative zkSNARK as $2\times 21700 = 43400$ seconds similar to above, which makes our approach conservatively $43400/2400=18\times$ faster (Section 6.2 - para 3). The cpSNARK-Set approach of experiment 3 does not work for reverse set membership.

<!-- mention that verifier time is negligible. mention how doubling is okay and mention that this estimate is conservative as it does not include cost of witness generation. -->

<!-- prover time in a single-prover zkSNARK reverse set membership proof for $1$ plaintext against a set of $10000$ ciphertexts is 2.17 seconds, which scales to 21700 seconds for $10000$ plaintexts (experiment 2; Figure 11 row 4). Thus, the estimated per-prover time in a collaborative zkSNARK approach is $43400$ seconds, which makes our implementation roughly $43400/2400 = 18\times$ faster than collaborative zkSNARKs. The cpSNARK-Set approach does not work for reverse set membership.  -->

### Experiments
<!--List each experiment the reviewer has to execute. Describe:
 - How to execute it in detailed steps.
 - What the expected result is.
 - How long it takes and how much space it consumes on disk. (approximately)
 - Which claim and results does it support, and how.-->

#### Experiment 1: Running our DB-SM and DB-RSM proofs
<!--Provide a short explanation of the experiment and expected results.
Describe thoroughly the steps to perform the experiment and to collect and organize the results as expected from your paper.
Use code segments to support the reviewers, e.g.,
```bash
python experiment_1.py
```-->

*Experiment description:* The goal of this experiment is to estimate the runtime query performance of our $\mathsf{BTraceIn}$ and $\mathsf{BTraceOut}$ queries. Towards this end, we setup mixnet keys as per the $\mathsf{Keygen}$ algorithm of Figure 6, create $n=10000$ ciphertexts as per the $\mathsf{Enc}$ algorithm, mix these ciphertexts as per the $\mathsf{Mix}$ protocol involving $m=4$ mix-servers, and then run $a)$ a worst-case DB-SM query for all input ciphertexts against the set of all output plaintexts ($I=J=[n]$) and $b)$ a worst-case DB-RSM query for all output plaintexts against the set of all input ciphertexts ($I=J=[n]$). We also implement all the steps proposed in Appendix B to evaluate performance in the realistic malicious security model. As per Figure 6, the worst-case runtime performance for our $\mathsf{BTraceIn}$ and $\mathsf{BTraceOut}$ queries, without any additional optimizations, would be twice the performance of the DB-SM and DB-RSM queries respectively.

*Running the experiment:*
```bash 
sudo docker run -it /bin/bash # run in the host shell to launch a container shell
python db_sm_rsm.py 10000 4 # run in the container shell
```

*Expected duration:* 5 hours

*Expected disk space:* 1.05 GB (size of image `tmpets/db-sm-rsm`)

*Expected output:* A report containing detailed timing, sizing and verification status information for our DB-SM and DB-RSM protocols (sample report at `sample-reports/report-db-sm-rsm-n10000-m4` in the git tree). The output is divided into the following sections: `preprocessing` (for input-independent setup steps run by the mix-servers), `input preparation/checking inputs` (for creating sender ciphertexts and verification by the mix-servers that the senders indeed created them), `mixing` (for the $\mathsf{Mix}$ protocol among the mix-servers), `forward set membership` (for the DB-SM protocol between the mix-servers and the verifier/querier) and `reverse set membership` (for the DB-RSM protocol between the mix-servers and the verifier/querier). Within each section, entries labelled `mixer X .... time` for any `X` = 0, 1, 2 or 3 (resp. `verifier ... time`) denote time taken by each mix-server (resp. verifier) in individual steps, entries labelled `mixer X total time` (resp. `verifier total time`) represent aggregation of these individual step times, and entries labelled `status_...` denote verification statuses of proofs such that value `True` means that the proof was accepted by the verifier. Entries labelled `size of ...` denote sizes of various produced outputs.

*Steps to verify the claimed results:*

1. Verify that entry `mixer X total time` in section `forward set membership` matches the per-prover time in row 1 of Figure 11 (here and henceforth, assume `X` = 0, 1, 2 or 3). This verification directly supports main result 1. Verify that entry `verifier time` matches the verifier time reported in row 1 of Figure 11. 
2. Verify that entry `mixer X total time` in section `reverse set membership` matches the per-prover time in row 3 of Figure 11. This verification directly supports main result 2. Verify that entry `verifier time` matches the verifier time reported in row 3 of Figure 11. 
3. Verify that entry `mixer X total time` in section `mixing` matches the mixing time reported in Figure 10. 
4. Verify that the following entries in section `forward set membership` match the corresponding values reported in the DB-SM section of Figure 10: 

    | Entry in the experiment output | Entry in DB-SM section of Figure 10 |
    | ------------------------------ | ----------------------------------- |
    |`verifier total time` in `get_verfsigs` | $(Q)$ Generating $n$ BB signatures/encryptions |
    |`mixer X total time` in `check_verfsigs` | $(M_k)$ Verifying $n$ BB signatures/encryptions | 
    |`mixer X total time` in `re-encrypt and reverse permute BB signatures` | $(M_k)$ Re-encryption+proof-of-shuffle of encrypted sigs | 
    |`mixer X total time` in `generate encrypted blinded BB signatures` | $(M_k)$ Homomorphic blinding of encrypted signatures |
    |`mixer X total time` in `decrypt blinded signatures` | $(M_k)$ Threshold decryption of encrypted signatures |
    |`mixer X total time` in `dpk_bbsig_nizkproofs` | $(M_k)$ Generating $n$ DPK proofs for $p_{BB}$ |
    |`verifier total time` in `dpk_bbsig_nizkverifs` | $(Q)$ Verifying $n$ DPK proofs for $p_{BB}$ |

5. Verify that the following entries in section `reverse set membership` match the corresponding values reported in the DB-RSM section of Figure 10: 

    | Entry in the experiment output | Entry in the DB-RSM section of Figure 10 |
    | ------------------------------ | ---------------------------------------- |
    |`verifier total time` in `pkcommverifs` | $(Q)$ Verifying $n$ PoKs of commitments |
    |`verifier total time` in `get_verfsigs_rev` | $(Q)$ Generating $n$ BBS+ quasi-signatures | 
    |`mixer X total time` in `check_verfsigs_rev` | $(M_k)$ Verifying $n$ BBS+ quasi-signatures/encryptions | <!-- club the step of homomorphically adding the r component to the re-encryption step  -->
    |`mixer X total time` in `re-encrypt and permute BBS+ signatures` | $(M_k)$ Re-encryption+proof-of-shuffle of encrypted sigs |
    |`mixer X total time` in `generate encrypted blinded BBS+ signatures` | $(M_k)$ Homomorphic blinding of encrypted signatures |
    |`mixer X total time` in `decryption of blinded BBS+ signatures` | $(M_k)$ Threshold decryption of encrypted signatures |
    |`mixer X total time` in `dpk_bbsplussig_nizkproofs` | $(M_k)$ Generating $n$ DPK proofs for $p_{BBS+}$ |
    |`verifier total time` in `dpk_bbsplussig_nizkverifs` | $(Q)$ Verifying $n$ DPK proofs for $p_{BBS+}$ |

6. Verify that the values of all `status_` entries are `True`, denoting that all proofs actually passed.
7. Verify that the values of the `size of ...` entries match the sizes reported in Figure 10.

*Additional notes:*

* We do not report sender costs to create ciphertexts and mixnet costs to check them because these steps do not affect runtime query performance and can be executed as and when individual senders send their data. However, this information is available under the `input preparation` and `checking inputs` sections.
* We also do not implement distributed key generation during $\mathsf{Keygen}$ because this is a one-time setup step that can be executed by the mix-servers ahead of time and does not affect runtime query performance (see Section 6.1). For the same reason, we do not report preprocessing time, but this information is available under the `preprocessing` section.
* In our implementation, we run the steps executed by each mix-server sequentially one after the other. Thus, although the total runtime of our experiment incurs the per-mix-server cost 4 times, in a real deployment, most of the bulky steps like proofs of shuffle, homomorphic blinding, threshold decryption, and the DPKs of stage 2 would be executed by each independent mix-server in parallel and therefore per-mix-server times capture real-world latencies more accurately (see Section 6.1). The only sequential operation is re-encryption, whose time is a miniscule fraction of these other steps (see entries `mixer X: re-encryption time` under `mixing`, `mixer X: reencrypting encrypted BB signatures time` under `forward set membership`, and `mixer X: reencrypting encrypted BBS+ signatures time` under `reverse set membership`).
* Although the verification times in our proofs are more than the very competitive verification times in zkSNARKs, the verifier time is a small fraction of the total time and thus overall latencies are still largely dominated by per-prover times.

#### Experiment 2: Running zkSNARK-based single-prover set membership and reverse set membership proofs
<!--...-->

*Experiment description:* The goal of this experiment is to estimate the performance of a set membership and reverse set membership proof using a Merkle accumulator-based zkSNARK. This is a single-prover proof, but the rationale for running this experiment is to indirectly estimate the performance of a collaborative zkSNARK by doubling the prover time in the single-prover zkSNARK. Towards this end, we created a set membership zkSNARK for statement $\rho_{SM-Acc}$ by creating a Merkle tree for the set of plaintexts and a reverse set membership zkSNARK for statement $\rho_{RSM-Acc}$ by creating a Merkle tree for the set of ciphertexts (commitments) (see Section 1.2.3B). The latter requires proving arithmetic relationships about elements in the commitment space, for which we used the Baby Jubjub curve. The hash function for the Merkle tree was chosen as the Poseidon hash function, which is specially optimised for use in zkSNARKs. The experiment runs set membership proof for a single ciphertext against a set of $10000$ plaintexts and reverse set membership proof for a single plaintext against a set of $10000$ ciphertexts. All our zkSNARKs are created using the ZoKrates toolchain and the Groth16 proof system.

*Running the experiment:*
```bash
sudo docker run -it tmpets/zksnark-sm-rsm /bin/bash # run in the host shell to launch a container shell
./run.sh sm 10000 poseidon # run in the container shell - set membership proof
./run.sh rsm 10000 poseidon # run in the container shell - reverse set membership proof
```

*Expected duration:* ~1 minute for each of the two proofs

*Expected disk space:* 240 MB (size of image `tmpets/zksnark-sm-rsm`)

*Expected output:* A report detailing the timings in various stages of both set membership and reverse set membership zkSNARKs (sample reports at `sample-reports/report-zksnark-sm-n10000-groth16-poseidon` and `sample-reports/report-zksnark-rsm-n10000-groth16-poseidon`). In each zkSNARK, the output is divided into the following sections: `COMPUTATION` (prover steps required to create a Merkle tree and find the Merkle path to the claimed member), `TRUSTED SETUP` (trusted setup steps specific to the ZK circuit), `PROVER` (prover steps for generating the noninteractive zkSNARK proof) and `VERIFIER` (verifier steps for verifying the proof). 

*Steps to verify the claimed results:*

1. Verify that the prover time printed against the `real` entry in the `PROVER` section is around 2.17 seconds, both for set membership and reverse set membership. When scaled to proofs for 10000 ciphertexts (for set membership) and 10000 plaintexts (for reverse set membership), this results in a total prover time of 21700 seconds, which match the per-prover time reported in rows 2 and 4 of Figure 11. Such direct scaling is sufficient to estimate the performance for $n$ proofs for these generic proof systems. This verification thus directly supports main result 1.
2. Verify that the verifier time printed against the `real` entry in the `VERIFIER` section is around 0.005 seconds, both for set membership and reverse set membership. When scaled to proofs for 10000 ciphertexts/plaintexts, this results in a total verifier time of 50 seconds, which match the verifier time reported in rows 2 and 4 of Figure 11.
3. Verify that the string `PASSED` is printed in the `VERIFIER` section, denoting that the proofs actually passed.

*Additional notes:*

* When we scale the above proofs for $n$ ciphertexts/plaintexts against the same set, the `Time __init__` cost under `COMPUTATION` (representing the cost to create the Merkle tree) gets added as a one-time cost and the `Time get_auth_path` costs (representing the cost to find the Merkle path) gets multiplied by $n$. This results in a small ~35 seconds overhead over 21700 seconds, which we ignore. The cost under the `TRUSTED SETUP` section only depends on the ZK circuit and not on the inputs, so we ignore this too. 

#### Experiment 3: Running cpSNARK-Set based single-prover set membership proofs
<!--...-->

*Experiment description:* The goal of this experiment is to estimate the time taken by Benarroch et al.'s set membership scheme. This scheme is also a single-prover scheme but it only implements set membership and not reverse set membership. For this experiment, we use the scheme's [official implementation](https://github.com/kobigurk/cpsnarks-set/tree/f8c7db66b7519b91dcda16caee6cb84949e8911b) that provides a benchmark to estimate the prover and verifier time in a single set membership proof. The scheme is based on RSA accumulators where the prover and verifier times are independent of the size of the set; therefore this benchmark only estimates these times for a dummy set of 3 elements. Additionally, the benchmark only estimates the time taken by the prover to compute the proof *given a membership witness*, but it does not include the time taken to generate the witness itself. We, therefore, add an additional benchmark to estimate the time taken by the prover to generate a single membership witness for a set of size 10000. 

*Running the experiment:*
```bash
sudo docker run -it tmpets/cpsnark-sm /bin/bash # run in the host shell to launch a container shell
cargo bench --bench membership_hash # run in the container shell - set membership proof
```

*Expected duration:* ~2-3 minutes

*Expected disk space:* 2.74 GB (size of image `tmpets/cpsnark-sm`)

*Expected output:* A report detailing the results of all the benchmarks (sample report at `sample-reports/report-benarroch-cpsnark-sm-n10000`). The output is divided into three sections: `membership_hash protocol proving` benchmarking the prover time in generating the proof given a membership witness, `membership_hash protocol verification` benchmarking the verifier time in verifying the proof, and `membership_hash creating witness` benchmarking the prover time in generating the membership witness. The timings of each section are reported in entries like `time:   [224.50 ms 225.77 ms 227.38 ms]` where the middle entry denotes the mean value over about a 100 samples and the other entries denote its variance.

*Steps to verify the claimed results:*

1. Verify that the prover time in section `membership_hash protocol proving` is around 220 ms. This supports main result 1 since the prover time when scaled to 10000 ciphertexts is 2200 s.
2. Verify that the verifier time in section `membership_hash protocol verification` is around 31 ms. When scaled to 10000 ciphertexts, this would be 310 s, which is still higher than our 210 s (row 1; Figure 11) for the distributed case.
3. Verify that the prover time in section `membership_hash creating witness` is around 783 ms. This reflects the $O(n)$ RSA witness computation operation, where $n$ is the size of the set (see benchmark `membership_hash creating witness` in file `cpsnark-sm/benches/membership_hash.rs`). Although we do not report this, this witness generation time when scaled to 10000 ciphertexts results in an overhead of 7830 s, which combined with the proof generation time in step 1 results in a total prover time of 10030 seconds in comparison to our 500 seconds (a 20x improvement) for the distributed case.

*Additional notes:*

* We ignore the cost of creating the accumulator and of hashing set values to prime numbers in this approach, since these are one-time costs.
* We do not include the benchmark for the special case when set elements are prime numbers, since this specialisation is not applicable for our general use-case.

## Limitations
<!--Describe which tables and results are not reproducible with the provided artifacts.
Provide an argument why this is not included/possible.-->

All the figures and numbers reported in Section 6 of the paper are reproducible with the above benchmarks. However, we are still in the shepherding phase and are in the process of making some requested presentation-related changes in this section, which are not included in the above experiments. These changes mainly entail:

* Adding the benchmarks for multiple values of $n$ and $m$ and for multiple samples in each setting in Figure 11, as opposed to only for $n=10000$ and $m=4$. These benchmarks can be generated by running `python db_sm_rsm.py n m` in experiment 1 with appropriate values of $n$ and $m$.
* Indicating the time taken in distributed key generation and ciphertext creation by the senders. For distributed key generation, we will cite the numbers reported in [3], which is an efficient MPC protocol for distributed key generation for the threshold Paillier cryptosystem we use. For sender costs, we will include the times reported under sections `input preparation` and `checking inputs` of experiment 1 output. 

<!-- ## Notes on Reusability -->
<!--First, this section might not apply to your artifacts.
Use it to share information on how your artifact can be used beyond your research paper, e.g., as a general framework.
The overall goal of artifact evaluation is not only to reproduce and verify your research but also to help other researchers to re-use and improve on your artifacts.
Please describe how your artifacts can be adapted to other settings, e.g., more input dimensions, other datasets, and other behavior, through replacing individual modules and functionality or running more iterations of a specific part.-->

## References

- [1] Ozdemir and Boneh, *Experimenting with Collaborative zk-SNARKs: Zero-Knowledge Proofs for Distributed Secrets*, https://eprint.iacr.org/2021/1530.pdf
- [2] Benarroch, Campanelli, Fiore, Gurkan and Kolonelos, *Zero-Knowledge Proofs for Set Membership: Efficient, Succinct, Modular*, https://eprint.iacr.org/2019/1255.pdf 
- [3] Damgard and Koprowski, *Practical Threshold RSA Signatures Without a Trusted Dealer*, https://iacr.org/archive/eurocrypt2001/20450151.pdf
