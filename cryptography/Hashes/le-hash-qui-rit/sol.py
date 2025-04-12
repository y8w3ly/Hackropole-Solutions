#!/usr/bin/env python3
from pwn import remote
from sage.all import *
from hashlib import sha256

def bytes2bits(data):
    return vector(GF(2), sum([list(map(int, format(byte, "08b"))) for byte in data], []))

r = remote("localhost", 4000)

line = r.recvline().strip().decode()
challenge_hex = line.split()[-1][2:]
challenge = bytes.fromhex(challenge_hex)
basis_vectors = []
payloads = []

for  i in range(256):
    M_i = str(i).encode()
    h_i = sha256(M_i).digest()
    v_i = bytes2bits(h_i)
    basis_vectors.append(v_i)
    payloads.append(M_i)
M = matrix(GF(2), basis_vectors)
M = M.transpose() 


challenge_vec = bytes2bits(challenge)
solution = M.solve_right(challenge_vec)


for idx, coef in enumerate(solution):
    if coef == 1:
        payload_hex = payloads[idx].hex()
        r.sendline(payload_hex.encode())
print(payloads)

r.interactive()
