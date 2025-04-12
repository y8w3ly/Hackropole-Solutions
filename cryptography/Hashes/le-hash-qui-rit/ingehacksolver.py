from pwn import *
import hashlib
import hashpumpy  # Install with pip install hashpumpy
import binascii

def bytes_to_bits(byte_sequence):
    # Convert each byte to its 8-bit binary representation, then flatten the list.
    return vector(GF(2), sum([list(map(int, format(byte, "08b"))) for byte in byte_sequence], []))

# Establish secure connection to the challenge server.
connection = remote("hashes.ctf.ingeniums.club", 1337, ssl=True)
assert connection

# Receive the AI-generated signature (i.e. the target hash digest) from the server.
ai_hash = connection.recvline().strip().decode()
log.info(f"ai_hash: {ai_hash}")

# Define the secret length (16 bytes in this example)
secret_len = 16

ai_vectors = []  # This list will store linearly independent bit-vectors.
payloads = []    # This list will store the corresponding forged payloads.

# Iterate over many possible appended values until we collect 256 independent vectors.
for i in range(10000):
    if len(ai_vectors) == 256:
        break

    appended_info = str(i)
    # Use hashpumpy.hashpump for the length extension attack.
    # The parameters: (old_hash, original_data, data_to_append, secret_length)
    new_ai_hash, ai_payload_str = hashpumpy.hashpump(ai_hash, "", appended_info, secret_len)
    
    # Convert new hash signature from hex into bytes and then into a bit vector.
    new_ai_hash_bytes = bytes.fromhex(new_ai_hash)
    bit_vector = bytes_to_bits(new_ai_hash_bytes)

    # Check if the new vector is linearly independent with respect to the already stored ones.
    temp_matrix = matrix(GF(2), ai_vectors + [bit_vector]).transpose()
    if temp_matrix.rank() == len(ai_vectors) + 1:
        log.info(f"{new_ai_hash} is linearly independent")
        payloads.append(ai_payload_str.encode())  # Save the forged payload as bytes.
        ai_vectors.append(bit_vector)

# Convert the original AI hash from hex into a bit vector.
target_bit_vector = bytes_to_bits(bytes.fromhex(ai_hash))

# Build the matrix from the independent vectors and solve the linear system.
matrix_ai = matrix(GF(2), ai_vectors).transpose()
solution_vector = matrix_ai.solve_right(target_bit_vector)

# Send back forged payloads corresponding to '1's in the solution vector.
for idx, flag in enumerate(solution_vector):
    if flag == 1:
        connection.sendline(payloads[idx].hex().encode())

connection.sendline(b"q")
connection.interactive()
