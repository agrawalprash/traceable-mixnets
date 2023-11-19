use accumulator::group::Rsa2048;
use accumulator::{group::Group, AccumulatorWithoutHashToPrime};
use ark_ff::PrimeField;
use ark_bls12_381::{Bls12_381, Fr, G1Projective};

use cpsnarks_set::{
    commitments::Commitment,
    parameters::Parameters,
    protocols::{
        hash_to_prime::{
            snark_hash::{HashToPrimeHashParameters, Protocol as HPProtocol},
            CRSSize,
        },
        membership::{
            transcript::{TranscriptProverChannel, TranscriptVerifierChannel},
            Protocol, Statement, Witness,
        },
    },
};
use criterion::{criterion_group, criterion_main, Criterion};
use merlin::Transcript;
use rand::thread_rng;
use rug::rand::RandState;
use rug::Integer;
use std::cell::RefCell;

const LARGE_PRIMES: [u64; 3] = [
    12_702_637_924_034_044_211,
    378_373_571_372_703_133,
    8_640_171_141_336_142_787,
];

struct TestHashToPrimeParameters {}
impl HashToPrimeHashParameters for TestHashToPrimeParameters {
    const MESSAGE_SIZE: u16 = 254;
}

pub fn criterion_benchmark(c: &mut Criterion) {
    let params = Parameters::from_curve::<Fr>().unwrap().0;
    println!("params: {}", params);
    let mut rng1 = RandState::new();
    rng1.seed(&Integer::from(13));
    let mut rng2 = thread_rng();

    let crs = cpsnarks_set::protocols::membership::Protocol::<
        Rsa2048,
        G1Projective,
        HPProtocol<Bls12_381, TestHashToPrimeParameters>,
    >::setup(&params, &mut rng1, &mut rng2)
    .unwrap()
    .crs;
    println!(
        "crs size: {:?}",
        crs.crs_hash_to_prime.hash_to_prime_parameters.crs_size()
    );
    let protocol = Protocol::<
        Rsa2048,
        G1Projective,
        HPProtocol<Bls12_381, TestHashToPrimeParameters>,
    >::from_crs(&crs);
    drop(crs);

    let value = Integer::from(Integer::u_pow_u(
        2,
        (protocol.crs.parameters.hash_to_prime_bits) as u32,
    ))
    .random_below(&mut rng1);
    let (hashed_value, _) = protocol.hash_to_prime(&value).unwrap();
    let randomness =
        Integer::from(Integer::u_pow_u(2, Fr::size_in_bits() as u32)).random_below(&mut rng1);
    let commitment = protocol
        .crs
        .crs_modeq
        .pedersen_commitment_parameters
        .commit(&hashed_value, &randomness)
        .unwrap();

    let accum =
        accumulator::Accumulator::<Rsa2048, Integer, AccumulatorWithoutHashToPrime>::empty();
    let accum = accum.add(
        &LARGE_PRIMES
            .iter()
            .skip(1)
            .map(|p| Integer::from(*p))
            .collect::<Vec<_>>(),
    );

    let accum = accum.add_with_proof(&[hashed_value.clone()]);
    let acc = accum.0.value;
    let w = accum.1.witness.0.value;
    assert_eq!(Rsa2048::exp(&w, &hashed_value), acc);

    let proof_transcript = RefCell::new(Transcript::new(b"membership"));
    let mut verifier_channel = TranscriptVerifierChannel::new(&protocol.crs, &proof_transcript);
    let statement = Statement {
        c_e_q: commitment,
        c_p: acc.clone(),
    };
    protocol
        .prove(
            &mut verifier_channel,
            &mut rng1,
            &mut rng2,
            &statement,
            &Witness {
                e: value.clone(),
                r_q: randomness.clone(),
                w: w.clone(),
            },
        )
        .unwrap();
    let proof = verifier_channel.proof().unwrap();
    let verification_transcript = RefCell::new(Transcript::new(b"membership"));
    let mut prover_channel =
        TranscriptProverChannel::new(&protocol.crs, &verification_transcript, &proof);
    protocol.verify(&mut prover_channel, &statement).unwrap();

    c.bench_function("membership_hash protocol proving", |b| {
        b.iter(|| {
            let proof_transcript = RefCell::new(Transcript::new(b"membership"));
            let mut verifier_channel =
                TranscriptVerifierChannel::new(&protocol.crs, &proof_transcript);
            let statement = Statement {
                c_e_q: commitment,
                c_p: acc.clone(),
            };
            protocol
                .prove(
                    &mut verifier_channel,
                    &mut rng1,
                    &mut rng2,
                    &statement,
                    &Witness {
                        e: value.clone(),
                        r_q: randomness.clone(),
                        w: w.clone(),
                    },
                )
                .unwrap();
        })
    });

    c.bench_function("membership_hash protocol verification", |b| {
        b.iter(|| {
            let verification_transcript = RefCell::new(Transcript::new(b"membership"));
            let mut prover_channel =
                TranscriptProverChannel::new(&protocol.crs, &verification_transcript, &proof);
            protocol.verify(&mut prover_channel, &statement).unwrap();
        })
    });

    // Create an array of values against which the membership witness is computed. Note:
    // 1. Although ideally each of these values should be distinct, the accumulation process in the following benchmark doesn't care 
    //    and proceeds the same way by computing G^prod where prod is a product of each element in value_arr, so we repeat the same 
    //    element to keep things simple.  
    // 2. We also ignore the cost to hash set elements to prime numbers, because presumably this could be done ahead of time for each
    //    element. Thus, we make it so that our set elements are already prime numbers.
    let prime_arr = vec![LARGE_PRIMES[0].clone(); 10000];
    
    c.bench_function("membership_hash creating witness", |b| {
        b.iter(|| {
            // Witness creation follows exactly the same process as accumulator creation of computing G^prod, but  
            // prod denotes the product of all elements except the element whose witness is being computed. We simulate 
            // this by skipping the first element from value_arr.
            let accum = accumulator::Accumulator::<Rsa2048, Integer, AccumulatorWithoutHashToPrime>::empty();
            let accum = accum.add(
                &prime_arr
                    .iter()
                    .skip(1)
                    .map(|p| Integer::from(*p))
                    .collect::<Vec<_>>(),
            );
            let _witness = accumulator::Witness::<Rsa2048, Integer, AccumulatorWithoutHashToPrime>(accum);
        })
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
