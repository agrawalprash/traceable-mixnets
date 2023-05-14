""" An implementation of the Poseidon hash as per the implementation in the ZoKrates standard library:
https://github.com/Zokrates/ZoKrates/tree/latest/zokrates_stdlib/stdlib/hashes/poseidon
"""

from poseidonconsts import POSEIDON_C, POSEIDON_M
from field import FQ

def arc(state, c, it):
    """ Add round constants (ARC) layer (state: state vector, c: constants list, it: offset in constants list for current round). """
    
    N = len(state)
    for i in range(N):
        state[i] = state[i] + c[it+i]
    return state

def sbox(state, f, p, r):
    """ S-box layer (state: state vector, f: no. of full rounds, p: no. of partial rounds, r: current round number). """

    N = len(state)
    state[0] = state[0] ** 5
    for i in range(1, N):
        state[i] = state[i]**5 if ((r < f/2) or (r >= f/2 + p)) else state[i]
    return state

def mix(state, m):
    """ Mix layer (state: state vector, m: matrix for the mixing layer). """

    N = len(state)
    out = [0]*len(state)
    for i in range(N):
        acc = 0
        for j in range(N):
            acc = acc + state[j] * m[i][j]
        out[i] = acc
    return out

def poseidon(inputs):
    """ Compute poseidon hash of a list of N field elements, where 0<N<=6, and return a single field element. """

    t = len(inputs)+1                        # number of field elements in the state vector (reserving one element for the capacity and N for the rate)
    rounds_p = [56, 57, 56, 60, 63, 64, 63]  # defining the number of partial rounds for each of 7 values of t.

    f = 8                                    # number of full rounds (combining those at the beginning and those at the end)
    p = rounds_p[t-2]                        # number of partial rounds    

    c = POSEIDON_C[t-2]                      # constants list for the given width of the state vector.
    m = POSEIDON_M[t-2]                      # mixing matrix for the given width of the state vector.

    state = [FQ(0)]                          # initialising the state vector by populating its rate component with input data and setting capacity to 0. 
    for i in range(t-1):
        state.append(inputs[i])

    for r in range(f+p):
        state = arc(state, c, r*t)
        state = sbox(state, f, p, r)
        state = mix(state, m)

    return state[0]