from gmpy2 import powmod as pow
from Crypto.PublicKey import RSA

class Smolkkey:
	def __init__(self):
		k = RSA.generate(2048, e = 3)
		self.pk = (k.n, k.e)
		self.sk = (k.n, k.d)

	def encrypt(self, m):
		n, e = self.pk
		c = pow(m, e, n)
		return int(c)

	def decrypt(self, c):
		n, d = self.sk
		m = pow(c, d, n)
		return int(m)

# Generate a key
E = Smolkkey()

# Encrypt the fag
flag = open("flag.txt", "rb").read()
flag = int.from_bytes(flag, "little")
c = E.encrypt(flag)

# Test decryption
assert flag == E.decrypt(c)

# Output public values
n, e = E.pk
print(f"{n = }")
print(f"{e = }")
print(f"{c = }")
