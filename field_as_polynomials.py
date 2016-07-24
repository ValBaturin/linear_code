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

        # irreducibility test
        irreducible = True
        for x in range(1, field):
            if polynomial_value(applicant, x, field) == 0:
                irreducible = False
                break
        if irreducible:
            return applicant


def add(first, second, field):
    if field.extension > 1:
        while first.shape != second.shape:
            if first.shape < second.shape:
                first = np.append(first, 0)
            else:
                second = np.append(second, 0)
        result = np.add(first, second)
        result = np.array(list(map(lambda x: x % field.char, result)))
    else:
        result = first + second
        result = result % field.char
    return result

def polynomial_normalization(polynomial, field):
    ir = field.irreducible_polynomial
    curr = polynomial
    rem = np.array([])
    while len(curr) >= len(ir):
        diff = len(curr) - len(ir)
        state = np.append(np.zeros((diff)), ir)
        coeff = curr[-1] / state[-1]
        state = np.array(list(map(lambda x: coeff * x, state)))
        curr = curr - state
        last_non_zero = 0
        for i in range(len(curr) - 1, 0, -1):
            if np.allclose(curr[i], 0):
                last_non_zero = i
            else:
                break
        curr = curr[:last_non_zero]
        curr = np.array(list(map(lambda x: x % field.char, curr)))
    return curr




def mult(first, second, field):
    if field.extension > 1:
        result = np.zeros((len(first) + len(second) - 1), dtype=int)
        for f in range(len(first)):
            for s in range(len(second)):
                result[f + s] +=  first[f] * second[s]
        return polynomial_normalization(result, field)
    else:
        return (first * second) % field.char


class GF:
    implementation = None
    elements = []
    char = 'Undefined'
    extension = 'Undefined'
    size = 'Undefined'
    irreducible_polynomial = 'Not found'

    def __init__(self, prime, n):
        if not is_prime(prime):
            raise ValueError(prime, 'is not a prime number')
        self.implementation = 'polynomials'
        self.char = prime
        self.extension = n
        self.size = self.char ** self.extension
        self.elements = []
        
        if n > 1:
            self.irreducible_polynomial = irreducible_polynomial_search(self.extension, self.char)
            print('Irreducible polynomial is found')

            # fill array of field's elements

            for word in product(*[range(prime) for i in range(n)]):
                self.elements.append(np.array(word))

        elif n == 1:
            self.irreducible_polynomial = None
            self.companion_matrix = None
            self.elements = [i for i in range(0, prime)]
        print('Field GF', prime**n, 'is generated')

    def __getitem__(self, index):
        return self.elements[index]
