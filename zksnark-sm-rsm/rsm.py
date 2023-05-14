import json
import sys
from babyjubjub import JUBJUB_C, JUBJUB_A, JUBJUB_D, MONT_A, MONT_B
from merkle_tree import MerkleTree
from math import ceil, log
from utils import sha256gelem, sha256internal, poseidongelem, poseidoninternal, G, H, INF, IDEN, create_elems_rands_comms, fastcreate_elems_rands_comms, u32arr 

def gen_witness_reverse_set_membership(elems, rands, comms, elemindex, hashfuncstr):
    hashfuncleaves = sha256gelem if hashfuncstr == "sha256" else poseidongelem
    hashfuncinternal = sha256internal if hashfuncstr == "sha256" else poseidoninternal
    mtree = MerkleTree(comms, hashfuncleaves=hashfuncleaves, hashfuncinternal=hashfuncinternal, padelem=IDEN)
    leaf = mtree.getnode(mtree.address(elemindex))
    auth_path = mtree.get_auth_path(mtree.address(elemindex))
    mtree.check_auth_path(comms[elemindex], auth_path)

    ## Prepare witness to be sent to ZoKrates ##    
    # Public component
    v = str(elems[elemindex])
    _H = [str(H.x), str(H.y)]
    rootval = u32arr(mtree.getRootHash()) if hashfuncstr == "sha256" else str(mtree.getRootHash())
    jubjubctx = {
        "JUBJUB_C": str(JUBJUB_C),
        "JUBJUB_A": str(JUBJUB_A),
        "JUBJUB_D": str(JUBJUB_D),
        "MONT_A": str(MONT_A),
        "MONT_B": str(MONT_B),
        "INFINITY": [str(INF.x),str(INF.y)],
        "Gu": str(G.x),
        "Gv": str(G.y)
    }
    # Private component
    r = str(rands[elemindex])
    path = {
        "valsibling": [u32arr(valsibling) if hashfuncstr=="sha256" else str(valsibling) for valsibling, _ in auth_path], 
        "dirsibling": [bool(dirsibling) for _, dirsibling in auth_path]
    }

    print("root hash:", mtree.getRootHash())

    return [v, _H, rootval, jubjubctx, r, path]

if __name__ == "__main__":
    n = int(sys.argv[1])
    treedepth =  ceil(log(n, 2))
    hashfuncstr = sys.argv[2]
    print("n=%s" % n)
    print("treedepth=%s" % treedepth)
    print("hashfunc=%s" % hashfuncstr)

    # Concretise the template of the ZOK file.
    with open("rsm-%s.zok.tmpl" % hashfuncstr, "r") as f:
        zokcontents = f.read()
    zokcontents = zokcontents.replace("__DEPTH__", str(treedepth))
    with open("build/rsm.zok", "w") as f:
        f.write(zokcontents)
        print("Written build/rsm.zok")

    # Create input for the ZOK file.
    elems, rands, comms = fastcreate_elems_rands_comms(n)
    zok_inp = gen_witness_reverse_set_membership(elems, rands, comms, 3, hashfuncstr)
    with open("build/zok.inp", "w") as f:
        json.dump(zok_inp, f, indent=4)
        print("Written build/zok.inp")