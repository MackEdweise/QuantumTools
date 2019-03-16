import numpy
import itertools

I = numpy.array([[1,0],
                 [0,1]])

X = numpy.array([[0,1],
                 [1,0]])

Y = numpy.array([[0, numpy.complex(0,-1)],
                 [numpy.complex(0,1), 0]])

Z = numpy.array([[1,0],
                 [0,-1]])

S = numpy.array([[1,0],
                 [0,numpy.complex(0,1)]])

CNOT = numpy.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 1],
                    [0, 0, 1, 0]])

SWAP = numpy.array([[1,0,0,0],
                  [0,0,1,0],
                  [0,1,0,0],
                  [0,0,0,1]
                ])


def U(theta, lamb, phi):
    return numpy.array(
        [
            [
                numpy.cos(theta/2),
                -numpy.e**(numpy.complex(0,1)*lamb)*numpy.sin(theta/2)
            ],
            [
                numpy.e**(numpy.complex(0,1)*phi)*numpy.sin(theta/2),
                numpy.e**(numpy.complex(0,1)*lamb+numpy.complex(0,1)*phi)*numpy.cos(theta/2)
            ]
        ]
    )
