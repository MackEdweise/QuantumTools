import numpy
from gates import X, Y, Z, I, SWAP

gates = {
    'I': I,
    'X': X,
    'Y': Y,
    'Z': Z
    }


# performs hilbert schmidt inner product of two matrices
def hilbert_schmidt(U1, U2):
    return (numpy.dot(U1.conjugate().transpose(), U2)).trace()


# decomposes a 4 x 4 operator into pauli matrices.
def decompose(U):
    for first_name, first_gate in gates.items():
        for second_name, second_gate in gates.items():
            product = first_name + second_name
            component = (1/4) * hilbert_schmidt(numpy.kron(first_gate, second_gate), U)
            if component != 0:
                print ("{0} * {1}".format(str(component), product))


decompose(SWAP)