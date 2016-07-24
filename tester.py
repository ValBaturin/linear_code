print("First of all you have to choose implementation of a finite field:\nthrought matrices or polynomials")
impl = input()
if impl == 'matrices':
	from field_as_matrices import GF
elif impl == 'polynomials':
	from field_as_polynomials import GF
else:
    raise ValueError('there is no implementation like you typed')

from walsh_hadamard_code import Code, decode

print("\nLet's build a finite field\nFor that we need a field characteristic P and\na degree of extension F(p) N")
p = int(input("Enter P\n"))
n = int(input("Enter N\n"))
Field = GF(p, n)

print('_______________________')
print("Now we can create a linear code based on the field we've just generated")
k = int(input("Enter the length of words from the field\n"))
C = Code(Field, k)

print("You need to know that this code you've created contains elements of size", 
	len(C.codes[0]), "\nand can correct no more then", C.error_correcting_capability, "mistakes!")

print()
print('From this moment we have the ability to decode recieved messages')

while True:
	message = input("Enter the recieved message to decode or 0 to exit\n").split()
	message = list(map(int, message))
	if message != [0]:
		decoded_message = decode(message, C)
		if decoded_message:
			print("The real message is")
			print(*decode(message, C))
		else:
			print("This message can not be decoded")
	else:
		break
