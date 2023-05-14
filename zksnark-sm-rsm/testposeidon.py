import json
import secrets
import sys
from babyjubjub import JUBJUB_E as order 
from field import FQ

from poseidonhash import poseidon

def gen_witness_testposeidon():
    v1 = 18125970593842551507389816904898427629615248786539058957789469117220859651232 #secrets.randbelow(order)
    v2 = 805607895884989731077939749188490849054497865688173424999458471517767516232 #secrets.randbelow(order)

    print("v1:", v1)
    print("v2:", v2)
    
    # ph = Poseidon(
    #     p=field_modulus,
    #     security_level=128,
    #     alpha=5,
    #     input_rate=2,
    #     t=3
    # )

    # h = ph.run_hash([v1,v2])

    h = poseidon([FQ(v1), FQ(v2)])

    print("h:", h)

    return [[str(v1), str(v2)]]


if __name__ == "__main__":
    zok_inp = gen_witness_testposeidon()
    with open("build/zok.inp", "w") as f:
        json.dump(zok_inp, f, indent=4)
        print("Written build/zok.inp")
