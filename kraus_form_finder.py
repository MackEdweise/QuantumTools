import numpy
import itertools
    
def kraus_form(original, transformation, terms):

    pauli_elements = [numpy.complex(0,0),numpy.complex(1,0),-numpy.complex(1,0),numpy.complex(0,1),-numpy.complex(0,1)]
    num_variables = terms*4
    
    possible_element_permutations = list(itertools.product(pauli_elements, repeat=num_variables))
    
    found = False
    p = 0
    
    for permutation in possible_element_permutations:
        
        p += 1
        print('Attempting permutation {0} of {1}'.format(p, len(possible_element_permutations)))
        
        matrices = list(zip(*(iter(permutation),)*4))
        
        abstract_kraus_sum_elements = []
        abstract_kraus_sum_daggers = []
        
        for matrix in matrices:
            
            N = numpy.array([[matrix[0],matrix[1]],
                             [matrix[2],matrix[3]]
                           ])
            
            abstract_kraus_sum_elements.append(N)
            abstract_kraus_sum_daggers.append(numpy.transpose(N).conjugate())
            
        sum = numpy.matmul(numpy.matmul(abstract_kraus_sum_elements[0], original), abstract_kraus_sum_daggers[0])
        
        i = 1
        while i < len(abstract_kraus_sum_elements):
            sum += numpy.matmul(numpy.matmul(abstract_kraus_sum_elements[i], original), abstract_kraus_sum_daggers[i])
            i+=1
        
        if numpy.array_equal(sum, transformation) and not numpy.array_equal(sum, null):
            
            found += 1
            
            print('Kraus sum found with elements:', end='\n\n')
    
            for j in range(len(abstract_kraus_sum_elements)):
                
                print('N{0}:'.format(j), end='\n\n')
                print(abstract_kraus_sum_elements[j], end='\n\n')
                
                print('N{0} dagger:'.format(j), end='\n\n')
                print(abstract_kraus_sum_daggers[j], end='\n\n')
    
    if found == False:
        print('No Kraus form with {0} element(s) exists'.format(terms))
    else:
        print('{1} Kraus form(s) with {0} element(s) exists'.format(terms, found))
    

# prime numbers unlikely to become indistinguishable
o1 = 3
o2 = 431
o3 = 1231
o4 = 9931

null = numpy.array([[numpy.complex(0,0), numpy.complex(0,0)],
                    [numpy.complex(0,0), numpy.complex(0,0)]
                   ])

original = numpy.array([[o1,o2],
                        [o3,o4]
                       ])
        
transformation = numpy.array([[o3,-o4],
                             [o1,-o2]
                            ])

terms = 3

kraus_form(original, transformation, terms)