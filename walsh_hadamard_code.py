import numpy as np
from itertools import product
import warnings
warnings.filterwarnings("ignore")


class Code():
    generator_matrix = 'Undefined'
    human_readable_generator_matrix = 'Undefined'
    word_lenght = 0
    codes = []
    human_readable_codes = []
    error_correcting_capability = 0

    def __init__(self, GF, k):

        #importing
        if GF.implementation == 'matrices':
            from field_as_matrices import add, mult
        if GF.implementation == 'polynomials':
            from field_as_polynomials import add, mult

        # G-matrix creation
        self.word_lenght = k
        self.generator_matrix = np.zeros([self.word_lenght, ((GF.size ** k - 1) / (GF.size - 1))], dtype=np.ndarray)
        self.human_readable_generator_matrix = np.empty([k, ((GF.size ** k - 1) / (GF.size - 1))], dtype='int64')
        pseudo_G = []
        self.error_correcting_capability = (GF.size ** (self.word_lenght - 1) - 1) // 2
        self.codes = []
        self.human_readable_codes = []

        for number_of_zeros in range(self.word_lenght):
            for comb in product(*[range(GF.size) for i in range(self.word_lenght - 1 - number_of_zeros)]):
                row = []
                row += list(comb)
                row.append(1)
                for zero in range(number_of_zeros):
                    row.append(0)
                pseudo_G.append(row)
        for i in range(len(pseudo_G)):
            for j in range(len(pseudo_G[i])):
                self.generator_matrix[j][i] = GF.elements[pseudo_G[i][j]]
                self.human_readable_generator_matrix[j][i] = pseudo_G[i][j]
        print('Generator matrix is found')

        # C-set creation
        for word in product(*[range(GF.size) for i in range(k)]):
            print('   ', 100 * len(self.codes) // (GF.size ** self.word_lenght), '%', end='\r')
            if GF.implementation == 'matrices':
                code = [np.zeros((GF.extension, GF.extension))]
                code = code * len(self.generator_matrix[0])
            if GF.implementation == 'polynomials':
                code = np.zeros((GF.extension), dtype=int)
                code = [code for i in range(len(self.generator_matrix[0]))]
            for i in range(len(self.generator_matrix[0])):
                for j in range(len(self.generator_matrix)):
                    code[i] = add(code[i], mult(GF.elements[word[j]], self.generator_matrix[j][i], GF), GF)
            self.codes.append(code)
        print('Codes are ready')

        
        for code in self.codes:
            human_readable_code = []
            for element in code:
                for i in range(GF.size):
                    if np.allclose(element, GF.elements[i]):
                        human_readable_code.append(i)
                        break
            self.human_readable_codes.append(human_readable_code)
            print('   ', 100 * len(self.human_readable_codes) // (GF.size ** self.word_lenght), '%', end='\r')
        print('Human readable codes are ready')

def hamming_distance(v1, v2):
    result = 0
    for i in range(len(v1)):
        if not np.allclose(v1[i], v2[i]):
            result += 1
    return result

def decode(message, Code):
    if len(message) != len(Code.human_readable_codes[0]):
        raise TypeError('Can not do decoding because of the lenght of a message')
    for code in Code.human_readable_codes:
        if hamming_distance(message, code) <= Code.error_correcting_capability:
            return code
    return None