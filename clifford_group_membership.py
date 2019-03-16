import numpy
import itertools
from functools import reduce
from gates import X, Y, Z, I


def check_for_clifford_group_membership(operator, group):
    
    print('determining whether the following matrix is a member of clifford group {0}:'.format(group), end='\n\n')
    print(operator, end='\n\n')
    
    #create operator dagger
    operator_dagger = numpy.transpose(operator).conjugate()
    
    # tensor product construction of matrices operated on by operator, operator dagger
    operands = []
    
    print('operands:', end='\n\n')
    
    for j in range(group):
        if group - j - 1 != 0 and j != 0:
            prefix_Is = reduce(lambda accumulator, matrix: numpy.kron(accumulator, matrix), [I for i in (range(group - j - 1))])
            postfix_Is = reduce(lambda accumulator, matrix: numpy.kron(accumulator, matrix), [I for i in (range(j))])
            operand_X = numpy.kron(numpy.kron(prefix_Is,X), postfix_Is)
            operand_Z = numpy.kron(numpy.kron(prefix_Is,Z), postfix_Is)
            operands.append(operand_X)
            operands.append(operand_Z)
            
            for i in (range(group - j - 1)):
                print('I', end='')
            print('X', end='')
            for i in range(j):
                print('I', end='')
            
            print()
            print(operand_X, end='\n\n')
            
            for i in (range(group - j - 1)):
                print('I', end='')
            print('Z', end='')
            for i in range(j):
                print('I', end='')
            
            print()
            print(operand_Z, end='\n\n')
            
        elif j != 0:
            postfix_Is = reduce(lambda accumulator, matrix: numpy.kron(accumulator, matrix), [I for i in (range(j))])
            operand_X = numpy.kron(X, postfix_Is)
            operand_Z = numpy.kron(Z, postfix_Is)
            operands.append(operand_X)
            operands.append(operand_Z)
            
            print('X', end='')
            for i in range(j):
                print('I', end='')
            
            print()
            print(operand_X, end='\n\n')
            
            print('Z', end='')
            for i in range(j):
                print('I', end='')
            
            print()
            print(operand_Z, end='\n\n')
            
        elif group - j - 1 != 0:
            prefix_Is = reduce(lambda accumulator, matrix: numpy.kron(accumulator, matrix), [I for i in (range(group - j - 1))])
            operand_X = numpy.kron(X, prefix_Is)
            operand_Z = numpy.kron(Z, prefix_Is)
            operands.append(operand_X)
            operands.append(operand_Z)
            
            for i in (range(group - j - 1)):
                print('I', end='')
            print('X', end='')
            
            print()
            print(operand_X, end='\n\n')
            
            for i in (range(group - j - 1)):
                print('I', end='')
            print('Z', end='')
                
            print()
            print(operand_Z, end='\n\n')
        
        else:
            operands.append(X)
            operands.append(Z)
            
            print('X', end='\n')
            
            print(X)
            
            print('Z', end='\n')
            
            print(Z)
            
    # calculate results
    results = []
    print('candidates for membership in pauli group {0}:'.format(group), end='\n\n')
    for operand in operands:
        result = numpy.matmul(numpy.matmul(operator, operand), operator_dagger)
        results.append(result)
    
        # if each candidate is an element of the pauli group, then the operator is a member of the corresponding clifford group
        print(result, end='\n\n')
    
    # generate the permutations of the pauli matrices that make up the elements of the pauli group
    pauli_group_permutations = list(itertools.product([I,X,Y,Z], repeat=group))
    pauli_group = []
    
    print('generating pauli group {0}.'.format(group), end='\n\n')
    
    for p in range(len(pauli_group_permutations)):
        pauli_group_member = numpy.array(list(reduce(lambda accumulator, pauli_matrix: numpy.kron(accumulator, pauli_matrix), pauli_group_permutations[p])))
        pauli_group.append(pauli_group_member)
        print(pauli_group_permutations[p], end='\n\n')
        print('yields pauli group member:', end='\n\n')
        print(pauli_group_member, end='\n\n')
        
    # generate the members of the pauli group for each of a = {0,1,2,3}
    for e in [1,2,3]:
        pauli_group_subset = [(numpy.complex(0, 1)**e)*subset_element for subset_element in pauli_group]
        pauli_group = pauli_group + pauli_group_subset
    
    # check the candidates for membership in the pauli group
    matches = 0
    
    for result in results:
    
        match_found = False
        
        for pauli_group_matrix in pauli_group:
            if numpy.array_equal(result, pauli_group_matrix):
                match_found = True
                matches += 1
                break
        
        # if one candidate was not matched with any member of the pauli group, the operator is not a member of the clifford group
        if not match_found:
            print('operator not in clifford group since:', end='\n\n')
            print(result, end='\n\n')
            print('not in pauli group', end='\n\n')
            
    print('{0} of the {1} required matrices were elements of the pauli group'.format(matches, len(results)), end='\n\n')
               
# create toffoli operator
toffoli = numpy.array([[1,0,0,0,0,0,0,0],
                        [0,1,0,0,0,0,0,0],
                        [0,0,1,0,0,0,0,0],
                        [0,0,0,1,0,0,0,0],
                        [0,0,0,0,1,0,0,0],
                        [0,0,0,0,0,1,0,0],
                        [0,0,0,0,0,0,0,1],
                        [0,0,0,0,0,0,1,0]
                       ])

# create 2 qubit QFT operator
QFT = 0.5 * numpy.array([[1,1,1,1],
                             [1, numpy.complex(0,1), -1, -numpy.complex(0,1)],
                             [1, -1, 1, -1],
                             [1, -numpy.complex(0,1), -1, numpy.complex(0,1)]
                           ])


check_for_clifford_group_membership(QFT, 2)
