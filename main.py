from collections import defaultdict

from plot import plot
from utils import to_bin, is_pow_two, bye_to_char
from itertools import combinations
import math
import random
import string

Bases = ['A', 'C', 'G', 'T']

Degenerated = {
    'R': ['A', 'G'],
    'Y': ['C', 'T'],
    'M': ['A', 'C'],
    'K': ['G', 'T'],
    'S': ['C', 'G'],
    'W': ['A', 'T'],
    'H': ['A', 'C', 'T'],
    'B': ['C', 'G', 'T'],
    'V': ['A', 'C', 'G'],
    'D': ['A', 'G', 'T'],
    'N': ['A', 'C', 'G', 'T']
}

Degen_dict = {}


def convert_to_valid_bases_amount(bases):
    removed_bases = []
    while not is_pow_two(len(bases)):
        removed_bases.append(bases[-1])
        bases = bases[:-1]

    combs = []
    for i in range(1, len(Bases) + 1):
        tmp = list(combinations(Bases, i))
        combs += tmp

    if len(bases) > len(combs):
        print("To much degenerated bases for the amount of bases.")
        exit(0)

    if removed_bases:
        print(f"Removed bases {removed_bases} to receive a convertible amount")
    return bases, combs


def conversion(bases):
    bases, combs = convert_to_valid_bases_amount(bases)
    for i in range(len(bases)):
        if len(combs[i]) > 1:
            Degen_dict[bases[i]] = list(combs[i])

    bits_per_base = 0
    tmp_dict = {}
    for i in range(len(bases)):
        bin = ''.join((format(i, 'b')))
        # while len(bin) < bits_per_base:
        #     bin = '0' + bin
        if len(bin) > bits_per_base:
            bits_per_base = len(bin)
        tmp_dict[bin] = bases[i]

    conv_dict = {}
    for key, val in tmp_dict.items():
        new = key
        while len(new) < bits_per_base:
            new = '0' + new
        conv_dict[new] = val

    return conv_dict


def to_DNA(input, amount=1000):
    bases = Bases + list(Degenerated.keys())
    conversions = conversion(bases)
    stings = []
    step = len(list(conversions.keys())[0])

    # print(Degen_dict)

    binary, added_bits = to_bin(input, step)

    compact = ''
    strings = []
    for i in range(amount):
        output = ''
        for j in range(0, len(binary), step):
            bit = binary[j:j + step]
            tmp = conversions[bit]
            if i == 0:
                compact += tmp
            if tmp in Degenerated.keys():
                output += random.choice(Degen_dict[tmp])
            else:
                output += tmp

        strings.append(output)
    plot(strings, compact)
    return strings, compact, added_bits, conversions

def to_simple_DNA(input):
    binary, added_bits = to_bin(input)
    conversions = conversion(Bases)
    output = ''
    for i in range(0, len(binary), 2):
        bit = binary[i:i + 2]
        output += conversions[bit]
    return [output]


def DNA_to_text(strings, added_bits, conversions, amount=1):
    binary = ''
    combination_dict = defaultdict(set)

    picked = random.sample(strings, amount)

    for i in range(len(picked[0])):
        for s in picked:
            combination_dict[i].add(s[i])

    for index, items in combination_dict.items():
        items = list(items)
        if len(items) == 1:
            if items[0] not in Bases:
                print("item not in bases, error. Picking 0")
                binary += conversions[conversions.keys()[0]]
            else:
                for key, val in conversions.items():
                    if val == items[0]:
                        binary += key
                        break
        else:
            added = False
            for key, val in Degen_dict.items():
                intersect = set(val).intersection(set(items))
                if intersect == set(items):
                    for conv_bin, conv_val in conversions.items():
                        if conv_val == key:
                            binary += conv_bin
                    added = True
                    break
            if not added:
                print("item not in bases, error. Picking 0")
                binary += conversions[conversions.keys()[0]]
    binary = binary[added_bits:]
    string = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]
        string += bye_to_char(byte)
    return picked, string


if __name__ == '__main__':
    input = 'badkamer qiU!,dhg qhgqshgmquh qohg qduhsdi flIBDFQDHGB'

    output = {}
    print(f"Converting input string of size {len(input)} bytes")
    # simple = to_simple_DNA(input)
    DNA, compact, added_bits, conversions = to_DNA(input, 1000)
    print(f"DNA:\n\t{compact}")
    print(f"length:\n\t{len(compact)}")
    retries = 500
    for i in range(1, 50):
        correct = True
        corr = 0
        for j in range(retries):
            picked, parsed = DNA_to_text(DNA, added_bits, conversions, i)
            # print(f"\n{picked}\n converts to '{parsed}'")
            if input != parsed:
                correct = False
            else:
                corr += 1
        if correct:
            print(f'correct with {i} DNA strings')
            # break
        else:
            if corr == 0:
                print(f'error in conversion with rate 0% DNA strings for length {i}')

            else:
                print(f'error in conversion with rate {(corr / retries) * 100}% DNA strings for amount {i}')

    print("Done")
