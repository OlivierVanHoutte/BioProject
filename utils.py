import math


def to_bin(input, step=2):
    tmp = ''
    length = 0
    tmp = ''.join(f"{ord(i):08b}" for i in input)

    counter = 0
    while len(tmp) % step != 0:
        tmp = '0' + tmp
        counter += 1
    return tmp, counter


def bye_to_char(byte):
    tmp = int(('0b' + byte), 2)
    return chr(tmp)


def is_pow_two(n):
    return math.log(n, 2).is_integer()
