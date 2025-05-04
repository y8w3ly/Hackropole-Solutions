# *Aaarg*

## *Description*
Vous devez afficher le flag, quelque soit le moyen utilisé !

## *Solution*

First we try the basic things : 
```
y8w3ly@notarch:~/ctfs/Hackropole/reverse/aaarg$ file aaarg 
aaarg: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=f5b07c01242cc5987bed7730c2762ae0491b5ddc, stripped
```
Its a 64 elf, and stripped so It won't have debugging symbols.


I tired strings but nothing interesting.

After opening the binary with ghidra we go to the entry function that calls `__libc_start_main` with the argument `FUN00401190` so it is main.

main function : 
```
undefined8 main(int argc,long argv)

{
  undefined8 uVar1;
  ulong uVar2;
  char *local_10;
  
  uVar1 = 1;
  if (1 < argc) {
    uVar2 = strtoul(*(char **)(argv + 8),&local_10,10);
    uVar1 = 1;
    if ((*local_10 == '\0') && (uVar1 = 2, uVar2 == (long)-argc)) {
      uVar2 = 0;
      do {
        putc((int)(char)(&DAT_00402010)[uVar2],stdout);
        uVar2 = uVar2 + 4;
      } while (uVar2 < 0x116);
      putc(10,stdout);
      uVar1 = 0;
    }
  }
  return uVar1;
}
```
### Solution breakdown 
After analyzing the function we understand that :
+ The program must take at least one argument.
+ This argument is being converted to an unsigned long using `uVar2 = strtoul(*(char **)(argv + 8),&local_10,10)`.
+ Our argument is being compared to -argc(argc is the number of arguments that the program took)
+ We must keep in mind that argc counts the program name as an argument so if we run ./aaarg yanis this would cause argc to be 2
+ So to solve the challenge we just need to run `./aaarg -2` and here we get the flag :
```
FCSC{f9a38adace9dda3a9ae53e7aec180c5a73dbb7c364fe137fc6721d7997c54e8d}
```
