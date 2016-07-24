import time

from field_as_matrices import GF as mField
from field_as_polynomials import GF as pField
from walsh_hadamard_code import Code



def compare(p, n, k):
	p = int(p)
	n = int(n)
	k = int(k)


	start_p = time.clock()
	c = Code(pField(p, n), k)
	finish_p = time.clock()
	result_p = finish_p - start_p
	
	start_m = time.clock()
	c = Code(mField(p, n), k)
	finish_m = time.clock()
	result_m = finish_m - start_m

	print('n = {0} | p = {1} | k = {2}\n{3:.3f} seconds with matrices\n{4:.3f} seconds with polynomials\n'.format(n, p, k, result_m, result_p))
	return None

while True:
	data = input().split()
	if data == ['0']:
		break
	compare(*data)

