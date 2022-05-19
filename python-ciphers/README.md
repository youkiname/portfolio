# Python Ciphers

Лабораторная работа 6 семестр

Handmade python implementation of SubstitutionCipher, PermutationCipher, XorCipher, CircularShiftCipher, ComboCypher.

### Usage
```
from ciphers import XorCipher

cipher = XorCipher()
cipher.cipher("myfile.txt", "encrypted.txt", "key.txt")
cipher.decipher("encrypted.txt", "decipher.txt", "key.txt")
```
