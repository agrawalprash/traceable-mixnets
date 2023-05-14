import bitstring
import hashlib
import secrets
import time
from babyjubjub import Point
from babyjubjub import JUBJUB_E as order
from field import FQ

from poseidonhash import poseidon

G = Point.generator()
H = Point(FQ(17777552123799933955779906779655732241715742912184938656739573121738514868268), FQ(2626589144620713026669568689430873010625803728049924121243784502389097019475))
GplusH = G + H
INF = Point.infinity()
IDEN = G.mult(0)

def timed(f):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = f(*args, **kwargs)
        end = time.perf_counter()
        print("Time %s: %s sec" % (f.__name__, end-start))
        return res
    return wrapper

def u32arr(hexdigest): 
    """ Convert a given hexdigest to an array of u32's, each again expressed in hex. """
    bs = bitstring.BitArray("0x"+hexdigest)
    arr = []
    for i in range(8):
        bs_slice = bs[32*i:32*(i+1)]
        bs_slice_u32 = bs_slice.u32
        bs_slice_hex = hex(bs_slice_u32)
        arr.append(bs_slice_hex)
    return arr

def sha256int(i):
    """ Compute sha256(b_i), where b_i is 512-bit representation of i, padded w/ leading zeros. """
    b = format(i, '#0514b') # map i to a 512-bit binary string with prefix '0b' (padded with leading zeros)
    bb = bitstring.BitArray(b)
    return hashlib.sha256(bb.bytes).hexdigest()

def sha256gelem(g):
    """ Compute sha256(g.x, g.y), where g.x,g.y represent coordinates of Point g. """
    bx = format(g.x.n, '#0258b') # map g.x to a 256-bit binary string with prefix '0b' (padded with leading zeros)
    by = format(g.y.n, '#0258b') # map g.y to a 256-bit binary string with prefix '0b' (padded with leading zeros)
    bbx = bitstring.BitArray(bx)
    bby = bitstring.BitArray(by)
    bb = bbx + bby             # a 512-bit bitstring
    return hashlib.sha256(bb.bytes).hexdigest()

def sha256internal(h1, h2):
    """ Compute sha256(h1, h2), where h1, h2 are both 256-bit hex strings. """
    return hashlib.sha256(bytes.fromhex(h1+h2)).hexdigest()

def poseidonint(i):
    """ Compute poseidon([FQ(0), FQ(i)]), where i is an integer expressible in 256 bits. """
    return poseidon([FQ(0), FQ(i)])

def poseidongelem(g):
    """ Compute poseidon([g.x, g.y]), where g.x,g.y represent coordinates of Point g. """
    return poseidon([g.x, g.y])

def poseidoninternal(h1, h2):
    """ Compute poseidon([h1, h2]), where h is a 512-bit hex string. """
    return poseidon([h1, h2])

        
def commitment(v, r):
    """ Compute Pedersen commitment under constant generators G and H. """
    return G.mult(v).add(H.mult(r))

@timed
def create_elems_rands_comms(n):
    """ Create n elements, randomness pairs in the exponent group of the 
    Baby Jubjub curve and corresponding commitments. """
    elems, rands, comms = [], [], []
    for i in range(n):
        elem = secrets.randbelow(order)
        rand = secrets.randbelow(order)
        comm = commitment(elem, rand)
        elems.append(elem)
        rands.append(rand)
        comms.append(comm)
    return elems, rands, comms

@timed
def fastcreate_elems_rands_comms(n):
    """ Like create_elems_rands_comms, but make it faster by creating all elems, rands
    consecutive to each other so that creating commitments requires only a single group 
    operation. 
    
    Warning: Do not use except for benchmarking purposes.
    """
    elem = secrets.randbelow(order)
    rand = secrets.randbelow(order)
    comm = commitment(elem, rand)
    elems, rands, comms = [elem], [rand], [comm]
    for i in range(n-1):
        elem = elem + 1
        rand = rand + 1
        comm = comm + GplusH
        elems.append(elem)
        rands.append(rand)
        comms.append(comm)
    return elems, rands, comms
