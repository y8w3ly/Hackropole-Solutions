flag = "FCSC{"

first = ""
arr = [101,55,53,53,50,99,102,54]
for i in arr:
	first+=chr(i)
flag+=first

tt = [104, 198, 202, 100, 202, 106, 194, 200]

second = ""
for i in tt:
	second += chr(i//2)

flag+=second
t = [384, 784, 784, 384, 456, 424, 416, 816]
third = ""
for i in t:
	third += chr(i//8)
flag+=third

fourth = ""
ttt = [1, 84, 85, 81, 9, 7, 87]
for c,i in enumerate(ttt) :
	fourth += chr(i^ord(third[c]))

flag += fourth
flag +="}"
print(flag)
