CPSNARKs-Set
------------

## Note

This directory contains the [official implementation](https://github.com/kobigurk/cpsnarks-set/tree/f8c7db66b7519b91dcda16caee6cb84949e8911b) of Benarroch et al.'s cpSNARK-Set scheme [Zero-Knowledge Proofs for Set Membership: Efficient, Succinct, Modular](https://eprint.iacr.org/2019/1255.pdf), with the following minor bugfixes:
* Imports ```algebra::bls12_381``` have been replaced with ```ark_bls12_381``` and ```algebra::PrimeField``` have been replaced with ``ark_ff::PrimeField``.
* Dependency num-bigint in Cargo.lock has been upgraded from v0.3.2 to v0.3.3 to fix [this issue](https://github.com/rust-num/num-bigint/pull/219) (see [release notes for v0.3.3](https://github.com/rust-num/num-bigint/blob/num-bigint-0.3.3/RELEASES.md)).

In addition, we have added an additional benchmark under ```benches/membership_hash``` to compute the cost of creating a membership witness. This was not included in the original benchmark and we add it since this would count towards the prover time in a set membership proof.

The original project's README now follows.

## Overview

**The library is not ready for production use!**

Implements various RSA-based protocols from the [Zero-Knowledge Proofs for Set Membership:
Efficient, Succinct, Modular](https://eprint.iacr.org/2019/1255.pdf) paper.

It implements the following protocols:

* [CPMemRSA](src/protocols/membership) - RSA-based set membership.
* [CPNonMemRSA](src/protocols/nonmembership) - RSA-based set non-membership.

The protocols are composed out of the following subprotocols:

* [root](src/protocols/root) - shows a committed element exists in an accumulator.
* [coprime](src/protocols/coprime) - shows a committed element does not exist in an accumulator.
* [modeq](src/protocols/modeq) - shows an integer commitment and a Pedersen commitment contain the same value.
* [hash\_to\_prime](src/protocols/hash_to_prime) - a number of protocols that perform a range proof or hash-to-prime and output a commitment:
  * [snark\_range](src/protocols/hash_to_prime/snark_range.rs) - LegoGroth16-based range proof.
  * [snark\_hash](src/protocols/hash_to_prime/bp.rs) - Bulletproofs-based range proof.
  * [bp](src/protocols/hash_to_prime/snark_hash.rs) - LegoGroth16-based hash-to-prime proof.

## Usage

### Tests

The following commands assume you have a recent stable Rust toolchain installed, e.g. 1.42.0. The Bulletproofs implementation also requires a nightly toolchain.

To run the tests for membership and non-membership protocols on BLS12-381, run `cargo test --release`.

To run the tests for membership and non-membership protocols on Ristretto, run `cargo +nigthly test --release --no-default-features --features dalek`.

### Benchmarks

The library contains a number of benchmarks:

#### Set membership

* [membership\_prime](benches/membership_prime.rs) - benchmarks RSA-based set membership when the elements are prime with a LegoGroth16 range proof.
* [membership\_prime\_60](benches/membership_prime_60.rs) - benchmarks RSA-based set membership when the elements are prime and are also small (around 60 bits) with a LegoGroth16 range proof.
* [membership\_bp](benches/membership_bp.rs) - benchmarks RSA-based set membership when the elements are prime with a Bulletproofs range proof.
* [membership\_bp\_60](benches/membership_bp_60.rs) - benchmarks RSA-based set membership when the elements are prime and are also small (around 60 bits) with a Bulletproofs range proof.
* [membership\_hash](benches/membership_hash.rs) - benchmarks RSA-based set membership when the elements are not prime and a Blake2s-based hash-to-prime is performed.
* [membership\_class](benches/membership_class.rs) - benchmarks class groups-based set membership when the elements are prime with a LegoGroth16 range proof. This is slow and experimental and the paper doesn't prove its security.


#### Set non-membership
* [nonmembership\_prime](benches/nonmembership_prime.rs) - benchmarks RSA-based set non-membership when the elements are prime with a LegoGroth16 range proof.
* [nonmembership\_bp](benches/nonmembership_bp.rs) - benchmarks RSA-based set non-membership when the elements are prime with a Bulletproofs range proof.
* [nonmembership\_hash](benches/nonmembership_hash.rs) - benchmarks RSA-based set non-membership when the elements are not prime and a Blake2s-based hash-to-prime is performed.

To run benchmarks for the protocols with SNARKs use `cargo bench` and for the protocols with Bulletproofs use `cargo bench --no-default-features --features dalek`.

## Libraries

We've implemented [LegoGroth16](https://github.com/kobigurk/legogro16) on top of [Zexe library](https://github.com/scipr-lab/zexe).

We've modified the Cambrian Tech's accumulator library. The modified version is [available here](https://github.com/kobigurk/cpsnarks-set-accumulator).

We've modifies librustzcash to get benchmarks for Merkle tree-based membership proofs. The modified version is [available here](https://github.com/kobigurk/cpsnarks-librustzcash). To run the benchmarks use `cargo run --release --example merkle_sha` for SHA256-based trees and `cargo run --release --example merkle_pedersen` for Pedersen hash-based trees.

## License

This code is licensed under either of the following licenses, at your discretion.

 * [Apache License Version 2.0](LICENSE-APACHE)
 * [MIT License](LICENSE-MIT)

Unless you explicitly state otherwise, any contribution that you submit to this library shall be dual licensed as above (as defined in the Apache v2 License), without any additional terms or conditions.

## Reference paper

[Zero-Knowledge Proofs for Set Membership: Efficient, Succinct, Modular](https://eprint.iacr.org/2019/1255.pdf)

[Daniel Benarroch](https://github.com/daniben31), [Matteo Campanelli](https://www.github.com/matteocam), [Dario Fiore](https://github.com/dariofiore), [Kobi Gurkan](https://github.com/kobigurk), [Dimitris Kolonelos](https://software.imdea.org/people/dimitris.kolonelos/index.html).


