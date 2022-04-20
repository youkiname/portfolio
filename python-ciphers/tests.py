import hashlib
from ciphers import SubstitutionCipher, PermutationCipher, XorCipher, OneTimePad, get_file_extension
from colorama import init
from colorama import Fore
init(autoreset=True)


sources = ["myfile.txt", "img2.png"]
key_filename = "key.txt"


def md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def check_filesum(filename1: str, filename2: str):
    if md5(filename1) == md5(filename2):
        print(Fore.GREEN + "OK")
    else:
        print(Fore.RED + "ERROR:")
        print(f"{md5(filename1)}\n{md5(filename2)}")


def check_cipher(cipher):
    print(Fore.CYAN + "Test " + type(cipher).__name__)
    for source_filename in sources:
        result_filename = "result." + \
            get_file_extension(source_filename)
        print(source_filename, end=" - ")
        cipher.cipher(source_filename, result_filename, key_filename)
        cipher.decipher(result_filename, "de_" +
                        result_filename, key_filename)
        check_filesum(source_filename, "de_" + result_filename)
    print()


def main():
    check_cipher(SubstitutionCipher())
    check_cipher(PermutationCipher())
    check_cipher(XorCipher())
    # check_cipher(OneTimePad())


if __name__ == "__main__":
    main()
