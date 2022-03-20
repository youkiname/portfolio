# Python Ciphers

Лабораторная работа 6 семестр

Handmade python implementation of SubstitutionCipher, PermutationCipher, XorCipher.

### Usage
```
from ciphers import XorCipher  # or SubstitutionCipher, PermutationCipher

cipher = XorCipher()
cipher.cipher("myfile.txt", "encrypted.txt", "key.txt")
cipher.decipher("encrypted.txt", "decipher.txt", "key.txt")
```
