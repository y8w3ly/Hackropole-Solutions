from sage.all import *
from Crypto.Util.number import *
from itertools import combinations
from Crypto.Util.number import long_to_bytes

n = 32317006071311007300714876688669951960444102669715484116646415746394635540935921521724498858714153019942728273207389351392489359055364847068112159175081645180751388138858639873796530441238955101568733568176426113140426646976937052525918530731769533330028543775101205176486450544323218351858348091394877603920443607214945787590258064663918917740728042628406529049644873974905470262922605695823668958842546472908325174694333334844222696779786423580284135591089906934014814106737656354549850191740172203279085863986305338341130808123659535483768004216490879857791785965848808238698345641038729244197829259714168491081729
e = 65537
c = 0x00bae65fbca88fea74202821d1773fa90e1a6e3532b3e60f1516ad8e04c84c1c42b733206d5b10bfeada9facd35adc426234b31183398adc4d0e842a3a2d09756f9e0bcdfdfe5b553dab4b21ea602eba4dc7db589f69360e1a598048ea0b719e7ab3ca25dec80acdaec582140877da1ce4c912425c43b1e19757309c2383b3b48ebbfcdac5bddfa167bbf1f7a31ec2a7758a52579956600306ca0dab86d5b37d3a7dfc9429a757f978905c01e46bd6d7c32f314a5916107545ad1cb17d76962b4ac11bbb6020a3ff0175d72081cc47cfd486ff05ed8799e2dd0991ce7b4f4ba2f2eae9dbddecc43e9d7a3899f6b493a839d5be7f9fe856fbe238e10047a7ad2945
s = bin(n)[2:]
#the hamming weight is the number of 1 bits in an integer
hw = s.count("1")
#the hamming wight of our n in 82
exponents = []
for i in range(len(s)):
    if s[-i-1]== "1":
        exponents.append(i)
#now we have the range of all our 1s

#now we have the property that says that if n=p*q then hw(n)<=hw(p)*hw(q)
#we know that the hw is 82, and sqrt(82)is around 9 so bit hamming weight of p and q are above 9
#you must think that 82 = 2* 41, yeah but let us assume that they have a same(or more precisely nearlt equal) hw

#now our attack is about to start
#when we do for example 3*7=21 we have (0b111)*(0b11)=(2^2+2^1+2^0)*(2^1+2^0)
#With distrubution it becomes 21 = 2^1*(2^2+2^1+2^0) + 2^0(2^1+2^0)
# Then 21 = 2^(1+2)+2^(1+1)+2^(1+0) + 2^(0+2) + 2^(0+1) + 2^(0+0)
# So 21 = 2^3 + 2^2 + 2^1 + 2^2 + 2^1 + 2^0 = 2^3 + 2*2^2 + 2*2^1 + 2^0 = 2^3 + 2^3 + 2^2 + 2^0 = 2^4 + 2^2 + 2^0 = (ob10101) which is true
#the sqrt(hw(21))=3 and hw(3)=2 andhw(7)=3 2*3>3.Here I can also assume that hw(p or q)> sqrt(hw(n))
# We all knew this before, but this is the trick that we are going to solve the challenge with.
# So we have all our bit positions of the modulus n, we can just compute how many times each bit appears as a sum of two other bits(like we have done in 3*7 multiplication)
#If the sum is in the set of a bit position(the array that we called exponents), the corresponding case in this array gets incremented
empty_counts =[0]*2049
#the array contains 2048 zeros because our n bit length is 2049, so from 0 to 2048 exponent
#I didn't figure out how to write this myself, so i got help from gpt.


#The offsets applied (relative to two selected positions x0 and y0) are:
#    (0, 0), (0, -1), (-1, -1), (-2, -1), (-2, -2), (-3, -2)

offsets = [(0, 0), (0, -1), (-1, -1), (-2, -1), (-2, -2), (-3, -2)]

# Convert exponents to a set for O(1) membership checks.
bit_set = set(exponents)

# Initialize the counter list. Adjust size if needed.

N = len(exponents)

# Loop over each unique pair in exponents.
for i in range(N):
    for j in range(i + 1, N):
        x0 = exponents[i]
        y0 = exponents[j]
        # Apply each offset pair and update counts if the sum is a valid bit position.
        for dx, dy in offsets:
            x = x0 + dx
            y = y0 + dy
            if (x + y) in bit_set:
                if 0 <= x < 2048 and 0 <= y < 2048:
                    empty_counts[x] += 1
                    empty_counts[y] += 1

# Collect and append indices where counts exceeds 9.
l = []
for i, c in enumerate(empty_counts):
    if c > 9:#we know that one of the factors must have more hamming weight than 9
        l.append(i)
print(l)


#so now, we must get all the combinations
#gpt again:

# Start checking with combinations of length 8
products =[]
for comb in combinations(l, 8):
    # Compute prod as 1 plus the sum of 2 raised to each exponent in the combination
    prod = 1 + sum(2**j for j in comb)
    products.append(prod)    
# Increment the combination length and print the new length being tested
n = 32317006071311007300714876688669951960444102669715484116646415746394635540935921521724498858714153019942728273207389351392489359055364847068112159175081645180751388138858639873796530441238955101568733568176426113140426646976937052525918530731769533330028543775101205176486450544323218351858348091394877603920443607214945787590258064663918917740728042628406529049644873974905470262922605695823668958842546472908325174694333334844222696779786423580284135591089906934014814106737656354549850191740172203279085863986305338341130808123659535483768004216490879857791785965848808238698345641038729244197829259714168491081729
e = 65537
c = 0x00bae65fbca88fea74202821d1773fa90e1a6e3532b3e60f1516ad8e04c84c1c42b733206d5b10bfeada9facd35adc426234b31183398adc4d0e842a3a2d09756f9e0bcdfdfe5b553dab4b21ea602eba4dc7db589f69360e1a598048ea0b719e7ab3ca25dec80acdaec582140877da1ce4c912425c43b1e19757309c2383b3b48ebbfcdac5bddfa167bbf1f7a31ec2a7758a52579956600306ca0dab86d5b37d3a7dfc9429a757f978905c01e46bd6d7c32f314a5916107545ad1cb17d76962b4ac11bbb6020a3ff0175d72081cc47cfd486ff05ed8799e2dd0991ce7b4f4ba2f2eae9dbddecc43e9d7a3899f6b493a839d5be7f9fe856fbe238e10047a7ad2945
#Now when we got all our combinations we just have to check the one that divides the n and we break 
for prod in products:
    if n%prod == 0:
        print(prod)
        p = prod
        break
q = n//p
assert q*p==n
phi = (p-1)*(q-1)
d = pow(e,-1,phi)
m = pow(c,d,n)
kaka = long_to_bytes(m).decode(errors="ignore")
flag = kaka[kaka.index("FCSC"):]
print(flag)
