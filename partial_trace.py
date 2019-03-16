import numpy
from gates import X, Y, Z, I, U, CNOT


def trace_two_qubit_gate(subsystem, gate):

    if subsystem == 0:
        return numpy.matmul(
            numpy.array(
                [
                    [1, 0, 0, 0],
                    [0, 1, 0, 0]
                 ]
            ),
            numpy.matmul(
                gate,
                numpy.array(
                    [
                        [1, 0],
                        [0, 1],
                        [0, 0],
                        [0, 0]
                    ]
                )
            )
        ) \
        + numpy.matmul(
            numpy.array(
                [
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]
                 ]
            ),
            numpy.matmul(
                gate,
                numpy.array(
                    [
                        [1, 0],
                        [0, 1],
                        [0, 0],
                        [0, 0]
                    ]
                )
            )
        )

    if subsystem == 1:
        return numpy.matmul(
            numpy.array(
                [
                    [1, 0, 0, 0],
                    [0, 0, 1, 0]
                 ]
            ),
            numpy.matmul(
                gate,
                numpy.array(
                    [
                        [1, 0],
                        [0, 0],
                        [0, 1],
                        [0, 0]
                    ]
                )
            )
        ) \
        + numpy.matmul(
            numpy.array(
                [
                    [0, 1, 0, 0],
                    [0, 0, 0, 1]
                 ]
            ),
            numpy.matmul(
                gate,
                numpy.array(
                    [
                        [0, 0],
                        [1, 0],
                        [0, 0],
                        [0, 1]
                    ]
                )
            )
        )


print(trace_two_qubit_gate(0, CNOT))