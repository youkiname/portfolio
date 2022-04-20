import random
import json
import sys
import os


def get_file_extension(filename: str):
    return filename.rsplit('.', 1)[1]


def get_sys_arg(index: int, default=None):
    try:
        return sys.argv[index]
    except IndexError:
        return default


def turn_over_dict(origin: dict) -> dict:
    return dict((v, int(k)) for k, v in origin.items())


def byte_to_int(byte):
    return int.from_bytes(byte, "little")


def int_to_byte(n):
    return n.to_bytes(1, "little")


def write_bytes_to_file(filename: str, bytes, append=False):
    mode = "wb"
    if append:
        mode += "a"
    with open(filename, mode) as result_file:
        result_file.write(bytes)


class AbstractCipher:
    def __init__(self) -> None:
        self.block_size = 1

    def save_key(self, filename: str, key):
        with open(filename, "w") as file:
            file.write(json.dumps(key))

    def load_key(self, filename: str):
        result = {}
        with open(filename, "r") as file:
            result = json.loads(file.read())
        return result

    def iterate_bytes(self, filename: str, apply_key) -> list:
        new_bytes = bytearray()
        with open(filename, "rb") as file:
            for _ in range(0, os.path.getsize(filename), self.block_size):
                bytes = file.read(self.block_size)
                if len(bytes) != self.block_size:
                    # add null bytes if bytes % block_size != 0
                    extra_length = self.block_size-len(bytes)
                    bytes += bytearray([255 for _ in range(extra_length)])
                new_bytes += apply_key(bytes)
        return new_bytes

    def count_null_ending_bytes(self, bytes) -> int:
        i = 1
        while bytes[-i] == 255:
            i += 1
        return i - 1

    def remove_null_ending_bytes(self, bytes):
        extra_bytes_amount = self.count_null_ending_bytes(bytes)
        if extra_bytes_amount == 0:
            return bytes
        return bytes[:-extra_bytes_amount]

    def cipher(self, filename: str, result_filename: str, key_filename: str):
        self._cipher(filename, result_filename, key_filename)

    def decipher(self, filename: str, result_filename: str, key_filename: str):
        self._decipher(filename, result_filename, key_filename)

    def _cipher(self, filename: str, result_filename: str, key_filename: str):
        key = self.generate_key()
        new_bytes = self.iterate_bytes(
            filename, lambda bytes: self.apply_key(bytes, key))
        write_bytes_to_file(result_filename, new_bytes)
        self.save_key(key_filename, key)

    def _decipher(self, filename: str, result_filename: str, key_filename: str):
        key = self.generate_decipher_key(self.load_key(key_filename))
        new_bytes = self.iterate_bytes(
            filename, lambda bytes: self.apply_decipher_key(bytes, key))
        new_bytes = self.remove_null_ending_bytes(new_bytes)
        write_bytes_to_file(result_filename, new_bytes)


class SubstitutionCipher(AbstractCipher):
    def __init__(self) -> None:
        super().__init__()
        self.block_size = 1

    def generate_key(self):
        return {}

    def generate_decipher_key(self, key: dict) -> dict:
        return turn_over_dict(key)

    def apply_key(self, bytes, key: dict):
        int_byte = bytes[0]
        if int_byte not in key:
            new_int_byte = random.randint(0, 255)
            while new_int_byte in key.values():
                new_int_byte = random.randint(0, 255)
            key[int_byte] = new_int_byte
        return bytearray(int_to_byte(key[int_byte]))

    def apply_decipher_key(self, bytes, key):
        int_byte = bytes[0]
        return bytearray(int_to_byte(key[int_byte]))


class PermutationCipher(AbstractCipher):
    def __init__(self) -> None:
        super().__init__()
        self.block_size = 7

    def generate_key(self) -> list[int]:
        key = list(range(self.block_size))
        random.shuffle(key)
        return key

    def generate_decipher_key(self, key: list[int]) -> list[int]:
        key_with_indices = turn_over_dict(dict(enumerate(key))).items()
        sorted_indices = sorted(key_with_indices, key=lambda x: x[0])
        return [n[1] for n in sorted_indices]

    def apply_key(self, bytes, key: list[int]) -> bytearray:
        new_bytes = list(zip(key, bytes))
        new_bytes = sorted(new_bytes, key=lambda x: x[0])
        return bytearray([x[1] for x in new_bytes])

    def apply_decipher_key(self, bytes, key: list[int]) -> bytearray:
        return self.apply_key(bytes, key)


class XorCipher(AbstractCipher):
    def __init__(self) -> None:
        super().__init__()
        self.block_size = 7

    def generate_key(self) -> list[int]:
        key = [random.randint(0, 255) for _ in range(self.block_size)]
        return key

    def generate_decipher_key(self, key: list[int]) -> list[int]:
        return key

    def apply_key(self, bytes, key: list[int]) -> bytearray:
        new_bytes = []
        for i, byte in enumerate(bytes):
            new_bytes.append(byte ^ key[i])
        return bytearray(new_bytes)

    def apply_decipher_key(self, bytes, key: list[int]) -> bytearray:
        return self.apply_key(bytes, key)


class OneTimePad(XorCipher):
    def cipher(self, filename: str, result_filename: str, key_filename: str):
        self.block_size = os.path.getsize(filename)
        self._cipher(filename, result_filename, key_filename)

    def decipher(self, filename: str, result_filename: str, key_filename: str):
        self.block_size = os.path.getsize(filename)
        self._decipher(filename, result_filename, key_filename)


class ComboCypher:
    ciphers = [
        SubstitutionCipher,
        PermutationCipher,
        XorCipher,
    ]

    def __init__(self) -> None:
        self.block_size = 64

    def generate_key(self) -> list[int]:
        key = [random.randint(0, 255) for _ in range(self.block_size)]
        return key

    def generate_decipher_key(self, key: list[int]) -> list[int]:
        return key


def main():
    cipher_name = get_sys_arg(1, default="s")
    source_filename = get_sys_arg(2, default="myfile.txt")
    result_filename = get_sys_arg(
        3, "result." + get_file_extension(source_filename))
    key_filename = get_sys_arg(4, "key.txt")

    ciphers = {
        "s": SubstitutionCipher,
        "p": PermutationCipher,
        "x": XorCipher,
        "o": OneTimePad,
    }

    cipher = ciphers[cipher_name]()
    cipher.cipher(source_filename, result_filename, key_filename)
    cipher.decipher(result_filename, "de_" + result_filename, key_filename)


if __name__ == "__main__":
    main()
