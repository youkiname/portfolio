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

You can add some files to sources in tests.py
```
sources = ["img2.png", "myfile.txt"]
```

and run tests with md5 hash checking

```
python tests.py
```

Result
```
Test SubstitutionCipher
img2.png - OK
myfile.txt - OK

Test PermutationCipher
img2.png - OK
myfile.txt - OK

Test XorCipher
img2.png - OK
myfile.txt - OK

Test OneTimePad
img2.png - OK
myfile.txt - OK

Test ComboCypher
img2.png - OK
myfile.txt - OK
```

