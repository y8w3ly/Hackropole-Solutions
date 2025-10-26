from pwn import remote
from gmpy2 import gcd

r = remote("localhost",4000)
e = 0x10001#this is an assumption
r.recvuntil(b"Encrypted flag: ")
c = int(r.recvline().decode())
print(f"{c=}\n")
m1 = 2
m2 = 3
r.sendlineafter(b">>> ",str(m1).encode())
s1 = int(r.recvline().decode())
print(s1)
r.sendlineafter(b">>> ",str(m2).encode())
s2 = int(r.recvline().decode())
print(s2)
p = gcd(pow(m1,e)-s1,pow(m2,e)-s2)
print(p)