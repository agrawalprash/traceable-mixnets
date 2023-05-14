zkSNARKs for proving set membership and reverse set membership in ZK
====================================================================

Proof of set membership, given in the form of a proof of knowledge of (v,r) 
s.t. c=comm(v,r) and a Merkle path to v in the merkle tree constructed using 
elements in set phi. This is given as the following proof of knowledge: 
    PK{(v,r,path): c = comm(v,r) && root_phi = MerkleDigest(v, path)}.

Proof of reverse set membership, given in the form of a proof of knowledge 
of (r) and a Merkle path to comm(v,r) in the merkle tree constructed using 
elements in a set Phi of commitments. This is given as the following proof
of knowledge: 
    PK{(r,path): root_Phi = MerkleDigest(comm(v,r), path)}.

Installation instructions
=========================

- Install zokrates from https://zokrates.github.io/gettingstarted.html
- Install bitstring python package: pip3 install bitstring

A note about curve choices 
==========================

- The default curve used in verifying zkSNARK proofs is the alt_bn128 
  curve, which is also known as the BN254 curve (or sometimes, confusingly, 
  the BN128 curve). 
- This curve is named BN254 because the field Fp on which the elliptic curve 
  points are defined is of size p, where p is of 254 bits.
- This is the curve on which we had defined our commitment scheme when 
  benchmarking set membership and reverse set membership proofs. This means 
  that group elements were points on this curve. Thus, it means that the 
  coordinates of those points were of 254 bits.
- (The name alt_bn128 is derived by the level of security provided by this curve,
  which, at the time, was thought to be 128 bits. Later, because of newer attack
  algorithms, the security got reduced to 111 bits, which may have led to the 
  phasing out of this name.)
- Let the order of the BN254 curve (also known as the order of the "exponent 
  group") be r, which denotes the number of distinct points in the group.
- Since the order of the group is r, zkSNARKs instantiated with the BN254 curve 
  can verify proofs of any F_r arithmetic circuit. This is simply because the 
  arithmetic in the exponent can be translated to arithmetic in the base group 
  using group operations and pairing operations. However, what if one wishes to 
  define some circuits on the group elements, e.g., one that computes their hash?
  For this, a curve Baby Jubjub is defined [1] over the finite 
  field F_r. This means that coordinates of the points of the Baby Jubjub curve 
  are elements of field F_r. The order of the Baby Jubjub curve itself, n, is 
  smaller than r.
- Therefore, if we choose Baby Jubjub for all elliptic curve cryptography, then 
  all ECC calculations like point additions can be performed in ZK because it 
  would correspond to field operations in field F_r. And since zkSNARKs can prove 
  all arithmetic computations in field F_r in zero knowledge, we can prove 
  arbitrary statements involving elliptic curve cryptography. (Note: technically, 
  it is possible to perform ECC computations even without choosing such a 
  special curve, but it would require expensive modulus operations to support 
  ECC operations like point addition, etc. The Baby Jubjub approach makes this 
  process far more efficient.)

A note about hash function choices
==================================

- It is claimed that the Poseidon hash function is particularly suitable for ZK 
  proofs and that the sha256 function is particularly unsuitable. Thus, we must 
  benchmark against the Poseidon hash function.
- The set of parameters (t,M,p,alpha) completely specify a unique instance of
  Poseidon. All other parameters are derived from these.
- The optimised Poseidon hash function is instantiated in the same way as the 
  un-optimised algorithm, but it requires additional precomputation of some
  quantities.
- The hash function itself takes a list of elements from a certain field F and 
  outputs a single field element.
- Poseidon original paper: https://eprint.iacr.org/2019/458.pdf
- Poseidon hash is a sponge construction:  https://en.wikipedia.org/wiki/Sponge_function
- Poseidon's input is t field elements, which means that if the field is F_p, where
  p is of n bits then the total size of the input in bits is t*n.


References
==========

1. Barry WhiteHat, Marta Belles, Jordi Baylina, "ERC-2494: Baby Jubjub Elliptic Curve", https://eips.ethereum.org/EIPS/eip-2494
2. Jonathan Wang, "BN254 for the rest of us", https://hackmd.io/@jpw/bn254
3. ZoKrates tutorial
4. Introduction to zkSNARKs
5. An introduction to hashing in ethereum
