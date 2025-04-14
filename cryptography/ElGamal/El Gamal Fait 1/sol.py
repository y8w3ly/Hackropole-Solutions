from pwn import remote
import time
#ez
io = remote("localhost",4000)

io.recvuntil(b"p = ")
p = int(io.recvline().decode())
io.recvuntil(b"g = ")
g = int(io.recvline().decode())
io.recvuntil(b"y = ")
y = int(io.recvline().decode())
m = 0
r = y
s = (-y) % (p - 1)
io.sendlineafter(b">>> ",str(m).encode())
io.sendlineafter(b">>> ",str(r).encode())
io.sendlineafter(b">>> ",str(s).encode())
io.interactive()