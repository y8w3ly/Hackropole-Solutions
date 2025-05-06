# *Guessy*

## *Description*
Il va probablement vous falloir beaucoup de chance pour deviner le flag. Ou quelques compétences en rétro-ingénierie.

## *Solution*
First we try the basic things : 
```
y8w3ly@notarch:~/ctfs/Hackropole/reverse/guessy$ file guessy 
guessy: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, not stripped
```
Its a 64 bit elf, dynamically so the source won't be fuzzy, and it is not stripped, so we have the debugging symbols.

After seeing the strings we can know what the challenge looks like : 
```
Can you guess the LAST character of the flag ?
Really ? I ask you for a single character and you give me this ?
Oh no, you were so close !
Congratulations, you've guessed the flag !
Now you can try to guess the next eight characters of the flag.
Well it seems that someone has trouble counting to eight.
Wrong guess.
Well done, you can try to guess the next eight characters but it won't be so easy.
I see you've got some skills in reversing, but can you guess the next eight ?
I must say that I'm impressed but it's not over. Will you be able to guess the next eight characters ?
Wrong guess
Alright, now let's go to the most difficult part of this challenge.
Well it does not begin well for you.
Come on, it's not that difficult !
Ok so I see we have an understanding. Let's begin the difficult part now.
Give me the flag:
```
Let's decompile the binary with ida.
+ main:
```
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char s[32]; // [rsp+0h] [rbp-20h] BYREF

  puts("Give me the flag:");
  fgets(s, 32, _bss_start);
  validate(s);
  return 0;
}
```
We understand that it takes from input a 32bytes string and store it in the variable s, then pass it to the function `validate` to check if its correct. 

+ validate:
```
int __fastcall validate(_BYTE *a1)
{
  if ( *a1 != 70 || a1[1] != 67 || a1[2] != 83 || a1[3] != 67 )
    return puts("Well it does not begin well for you.");
  if ( a1[4] != 123 )
    return puts("Come on, it's not that difficult !");
  puts("Ok so I see we have an understanding. Let's begin the difficult part now.");
  difficult_part();
  return 0;
}
```
Alright validate checks the flag format `FCSC{` with comparing our input with their ascii values `*a1 != 70 || a1[1] != 67 || a1[2] != 83 || a1[3] != 67`
Then it calls the function called `difficult_part`:

+ difficult_part:
```
int difficult_part()
{
  char v1[16]; // [rsp+0h] [rbp-20h] BYREF
  char s; // [rsp+10h] [rbp-10h] BYREF
  unsigned __int8 v3; // [rsp+11h] [rbp-Fh]
  unsigned __int8 v4; // [rsp+12h] [rbp-Eh]
  unsigned __int8 v5; // [rsp+13h] [rbp-Dh]
  unsigned __int8 v6; // [rsp+14h] [rbp-Ch]
  unsigned __int8 v7; // [rsp+15h] [rbp-Bh]
  unsigned __int8 v8; // [rsp+16h] [rbp-Ah]
  char v9; // [rsp+17h] [rbp-9h]

  puts("Now you can try to guess the next eight characters of the flag.");
  fgets(&s, 16, _bss_start);
  if ( strlen(&s) != 9 )
    return puts("Well it seems that someone has trouble counting to eight.");
  if ( s != 101 || v3 != 55 || v4 != 53 || v5 != 53 || v6 != 50 || v7 != 99 || v8 != 102 || v9 != 54 )
    return puts("Wrong guess.");
  puts("Well done, you can try to guess the next eight characters but it won't be so easy.");
  fgets(&s, 16, _bss_start);
  if ( strlen(&s) != 9 )
    return puts("Well it seems that someone has trouble counting to eight.");
  if ( 2 * s != 104
    || 2 * (char)v3 != 198
    || 2 * (char)v4 != 202
    || 2 * (char)v5 != 100
    || 2 * (char)v6 != 202
    || 2 * (char)v7 != 106
    || 2 * (char)v8 != 194
    || 2 * v9 != 200 )
  {
    return puts("Wrong guess.");
  }
  puts("I see you've got some skills in reversing, but can you guess the next eight ?");
  fgets(&s, 16, _bss_start);
  if ( strlen(&s) != 9 )
    return puts("Well it seems that someone has trouble counting to eight.");
  if ( 8 * s != 384
    || 8 * (char)v3 != 784
    || 8 * (char)v4 != 784
    || 8 * (char)v5 != 384
    || 8 * (char)v6 != 456
    || 8 * (char)v7 != 424
    || 8 * (char)v8 != 416
    || 8 * v9 != 816 )
  {
    return puts("Wrong guess.");
  }
  puts("I must say that I'm impressed but it's not over. Will you be able to guess the next eight characters ?");
  fgets(v1, 16, _bss_start);
  if ( strlen(v1) != 9 )
    return puts("Well it seems that someone has trouble counting to eight.");
  if ( ((unsigned __int8)s ^ v1[0]) != 1
    || (v3 ^ v1[1]) != 84
    || (v4 ^ v1[2]) != 85
    || (v5 ^ v1[3]) != 81
    || (v6 ^ v1[4]) != 9
    || (v7 ^ v1[5]) != 7
    || (v8 ^ v1[6]) != 87
    || v9 != v1[7] )
  {
    return puts("Wrong guess");
  }
  puts("Alright, now let's go to the most difficult part of this challenge.");
  most_difficult_part();
  return 0;
}
```
This one passes our input to some checks(by chunks of eight), so we have four parts that we should get.

+ first part:
```
arr = [101,55,53,53,50,99,102,54]
first=""
for i in arr:
        first+=chr(i)
```

+ second :
```
tt = [104, 198, 202, 100, 202, 106, 194, 200]
second = ""
for i in tt:
        second += chr(i//2)
```

+ third :
```
t = [384, 784, 784, 384, 456, 424, 416, 816]
third = ""
for i in t:
        third += chr(i//8)
```

+ fourth :
```
fourth = ""
ttt = [1, 84, 85, 81, 9, 7, 87]
for c,i in enumerate(ttt) :
        fourth += chr(i^ord(third[c]))
```

+ After all, the program calls the function `most_difficult_part` which just checks for the last character `}` :
```
int most_difficult_part()
{
  char s[16]; // [rsp+0h] [rbp-10h] BYREF

  puts("Can you guess the LAST character of the flag ?");
  fgets(s, 16, _bss_start);
  if ( strlen(s) != 2 )
    return puts("Really ? I ask you for a single character and you give me this ?");
  if ( s[0] != 125 )
    return puts("Oh no, you were so close !");
  puts("Congratulations, you've guessed the flag !");
  return 0;
}
```


and gg you got the flag : `FCSC{e7552cf64ce2e5ad0bb0954f167a02c}`
solve script can found [here](sol.py)
