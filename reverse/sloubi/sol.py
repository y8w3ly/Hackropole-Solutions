import string
charset = string.printable

"""
4B}mCuCNJmeVhvCzQusFHS7{2gCBCrQW
for ( i = 0LL; i < 0x20; ++i )
        s1[(17 * i + 51) % 0x20] = s[i];
"""
flag = ""
s1 = "4B}mCuCNJmeVhvCzQusFHS7{2gCBCrQW"
for i in range(32):
	flag += s1[(17*i + 51)%0x20]

print(flag)
