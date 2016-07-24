import numpy as np
from itertools import product
import warnings
warnings.filterwarnings("ignore")

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def polynomial_value(polynomial, x, field):
    value = 0
    for degree, coeff in enumerate(polynomial):
        value += (coeff * ((x ** degree) % field)) % field
    return value % field

def irreducible_polynomial_search(degree, field):
    if degree == 1:
        return np.array([1])
    while True:
        # creation of random polynomial
        applicant = np.array([], dtype='int64')
        applicant = np.append(applicant, np.random.randint(1, high=field)) # zeroth coeff elem can't be 0
        for i in range(1, degree):
            applicant = np.append(applicant, np.random.randint(0, high=field))
        applicant = np.append(applicant, 1) # the last coeff is 1
        irreducible = True

        # irreducibility test
        for x in range(1, field):
            if polynomial_value(applicant, x, field) == 0:
                irreducible = False
                break
        if irreducible:
            return applicant

def matrix_normalization(matrix, field):
    matrix = matrix.reshape(-1)
    for i, v in enumerate(matrix):
        matrix[i] = matrix[i] % field.char

def mult(first_matrix, second_matrix, field):
    result = np.dot(first_matrix, second_matrix)
    matrix_normalization(result, field)
    return result

def add(first_matrix, second_matrix, field):
    result = first_matrix + second_matrix
    matrix_normalization(result, field)
    return result

class GF:
    implementation = None 
    elements = []
    char = 'Undefined'
    extension = 'Undefined'
    size = 'Undefined'
    irreducible_polynomial = 'Not found'
    companion_matrix = np.array([])

    def __init__(self, prime, n):
        if not is_prime(prime):
            raise ValueError(prime, 'is not a prime number')
        self.implementation = 'matrices'
        self.char = prime
        self.extension = n
        self.size = self.char ** self.extension
        self.elements = []
        
        if n > 1:
            self.irreducible_polynomial = irreducible_polynomial_search(self.extension, self.char)
            print('Irreducible polynomial is found')
            self.companion_matrix = np.polynomial.polynomial.polycompanion(self.irreducible_polynomial)
            matrix_normalization(self.companion_matrix, self)

            # fill array of field's elements
            roots = []
            roots.append(np.eye(n))
            for i in range(1, n):
                roots.append(np.dot(roots[i - 1], self.companion_matrix))
            for word in product(*[range(prime) for i in range(n)]):
                elem = np.zeros((n))
                for i, coeff in enumerate(word):
                    elem = elem + coeff * roots[self.extension - i - 1]
                self.elements.append(elem)

            # normalization
            for index in range(prime ** n):
                matrix_normalization(self.elements[index], self)

        elif n == 1:
            self.irreducible_polynomial = None
            self.companion_matrix = None
            self.elements = [i for i in range(0, prime)]
        print('Field GF', prime**n, 'is generated')

    def __getitem__(self, index):
        return self.elements[index]