import hashlib
import bcrypt
import time
from argon2 import PasswordHasher

ph = PasswordHasher()

with open("10k-most-common.txt", "r") as f:
    words = f.read().splitlines()

max_round = 100

def Hash(word, hash_type):
    start_time = time.perf_counter()
    for index, word in enumerate(words):
        if index == max_round:
            break

        if hash_type == "SHA1":
            hashlib.sha1(bytes(word, "utf-8")).hexdigest()
        elif hash_type == "MD5":
            hashlib.md5(bytes(word, "utf-8")).hexdigest()
        elif hash_type == "BCRYPT":
            bcrypt.hashpw(bytes(word, "utf-8"), bcrypt.gensalt())
        elif hash_type == "SHA256":
            hashlib.sha256(bytes(word, "utf-8")).hexdigest()
        elif hash_type == "SHA512":
            hashlib.sha512(bytes(word, "utf-8")).hexdigest()
        elif hash_type == "SCRYPT":
            hashlib.scrypt(bytes(word, "utf-8"), salt=b"salt", n=2**14, r=8, p=1)
        elif hash_type == "ARGON2":
            ph.hash(word)
    elapsed_time = time.perf_counter() - start_time
    return elapsed_time


algorithms = ["MD5", "SHA1", "SHA256", "SHA512", "BCRYPT", "SCRYPT", "ARGON2"]

for algorithm in algorithms:
    elapsed_time = Hash(words, algorithm)
    print(f"{algorithm}: {elapsed_time:.6f}s ({max_round/elapsed_time:.0f} hashes/second)")