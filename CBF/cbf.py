import numpy as np
import math
import zlib
import hashlib
import random

precision = 0.0001

file = 'text.txt'
random_state = random.randint(10, 100)


def get_unique_words_from_text(path: str):
    with open(path, encoding="utf8") as file:
        return set(file.read().split())


# a) amount of objects
unique_words = get_unique_words_from_text(file)
number_of_words = len(unique_words)
print(number_of_words)
print()

# m = - ( n * ln(P) ) / ( ln2 ) ^ 2

# c) length of CBF array.
cbf_size = -math.ceil((number_of_words * np.log(precision)) / (np.power(np.log(2), 2)))
print(cbf_size)
print()


def get_number_of_hash_functions(cbf_size, number_of_uw):
    return round((cbf_size / number_of_uw) * math.log(2))


# b) amount of hash functions (thinking about dynamic hash functions generating)
count_of_hash = get_number_of_hash_functions(cbf_size, number_of_words)
print(count_of_hash)
print()


# 2. To create a CBF based with precision = 0.0001 and for words for any internet post
def random_salts(hashes_count: int):
    salts = [
        hashlib.sha256(bytes(np.random.RandomState(random_state).randint(
            0, 999_999))).hexdigest() for _ in range(hashes_count)
    ]
    return salts


salts = random_salts(cbf_size)


def get_index_via_hash(obj: str, salt: str, cbf_length: int):
    return zlib.crc32(bytes(obj + salt, encoding='utf8')) % cbf_length


def countable_bloom_filter(objects: set, cbf_length: int, hashes_count: int):
    cbf_t = [0] * cbf_length
    salts_t = random_salts(hashes_count)
    for obj in objects:
        for i in range(hashes_count):
            index = get_index_via_hash(obj=obj, salt=salts_t[i], cbf_length=cbf_size)
            cbf_t[index] += 1
    return cbf_t


def word_prob(word_t: str, cbf_size: int, salts_t: list, hashes_count: int):
    minimal_val = 999999999

    for i in range(hashes_count):
        index = get_index_via_hash(obj=word_t, salt=salts_t[i], cbf_length=cbf_size)
        if cbf[index] < minimal_val:
            minimal_val = cbf[index]

    if minimal_val > 0:
        return 1 / minimal_val
    else:
        return 0


cbf = countable_bloom_filter(objects=unique_words, cbf_length=cbf_size, hashes_count=count_of_hash)
print(cbf)
print()

# 3. to check for existing any 10 words in CBF
words = ['data', 'тип', 'музей', 'облако', 'озеро', 'лес', 'перекресток', 'данных', 'витрина', 'lake']

for word in words:
    print(word_prob(word_t=word, cbf_size=cbf_size, salts_t=salts, hashes_count=count_of_hash))
