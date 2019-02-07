import math

def create_multiplicative_group(group_order):
    multiplicative_group = [i for i in range(group_order)][1:]
    
    print(multiplicative_group)
    return multiplicative_group

def find_generator(multiplicative_group, max_generator):
    found = False
    g = 1
    
    while (found == False) and (g < max_generator):
        matches = []
        powers = []
        for r in range(100):
            result = g**r % group_order
            if result in multiplicative_group and result not in matches:
                matches.append(result)
                powers.append(r)
        if len(matches) == len(multiplicative_group):
            found = True
            print("found generator: g = {0}".format(g))
            print("group member matches:")
            print(matches)
            print("powers of {0}:".format(g))
            print(powers)
            return g
        g += 1
    print('No generator < {0} found'.format(max_generator))
    return None
        
def create_tables(generator, multiplicative_group, group_order):
    
    print("\nUsing generator {0} to graph discrete log:".format(generator))

    def discrete_log_function(x1, x2, a, group_order):
        a_term = a**(-x2)
        return ((generator**x1)*(a_term)) % group_order
    
    for a in multiplicative_group:
        print('\n\nFor group member {0}:'.format(a))
        print('lines parallel to ({0}, 1)'.format(math.log(a, generator)))
        for i in range(len(multiplicative_group)):
            print('\n')
            for j in range(len(multiplicative_group)):
                print("f({0},{1}) = {2:5s}".format(i,j,str(round(discrete_log_function(i, j, a, group_order), 4))), end=' ')

group_order = 4
max_generator = 100
multiplicative_group = create_multiplicative_group(group_order)
g = find_generator(multiplicative_group, max_generator)
if g is not None:
    create_tables(g, multiplicative_group, group_order)