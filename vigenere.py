#!/usr/bin/python3

# Run me like this:
# $ cat ciphertext_file | python3 vigenere.py

import sys

# taken from Wikipedia
letter_freqs = {
    "A": .08167, "B": .01492, "C": .02782, "D": .04253, "E": .12702, "F": .02228,
    "G": .02015, "H": .06094, "I": .06996, "J": .00153, "K": .00772, "L": .04025,
    "M": .02406, "N": .06749, "O": .07507, "P": .01929, "Q": .00095, "R": .05987,
    "S": .06327, "T": .09056, "U": .02758, "V": .00978, "W": .02360, "X": .00150,
    "Y": .01974, "Z": .00074
}

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def shift_letter(c: str, key: str) -> str:
    """Shift character c by key positions."""
    return alphabet[(alphabet.index(c) - alphabet.index(key)) % 26]


def decipher(cipher: str, key: str) -> str:
    """Decipher vigenere cipher using key."""
    message = ''
    for i in range(len(cipher)):
        message += shift_letter(cipher[i], key[i % len(key)])
    return message


if __name__ == "__main__":
    cipher = sys.stdin.read().replace("\n", "").replace(" ", "").upper()

    # convert letters to numbers
    nums = {
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,
        'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11,
        'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17,
        'S': 18, ' T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23,
        'Y': 24, 'Z': 25
    }

    def get_freqs(text):
        # get letter frequencies
        freqs = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0,
                 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0,
                 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0,
                 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0,
                 'Y': 0, 'Z': 0}
        length = len(text)
        for c in text:
            freqs[c] += 1/length
        return freqs

    def get_freq(c, text):
        length = len(text)
        freq = 0
        for char in text:
            if char == c:
                freq += 1/length

        return freq

    # pop variance of text
    def popvar(text):
        freqs = get_freqs(text)
        # variance formula
        var = 0
        for c in freqs:
            var += (freqs[c] - 1/26)**2

        return var/26

    # find key length
    def key_length(text):
        length = 2
        mindif = 1000
        for k in range(2, 14):
            # split text and get mean popvar
            meanvar = 0
            dif = 0.000000000000
            for i in range(k):
                split = ""                                  # string starts empty
                for j in range(0, len(text[i:]), k):        # starting from ith letter, add every kth letter
                    split += text[i + j]

                meanvar += popvar(split)/k                  # calculate mean population variance
                dif = abs(meanvar - 0.0010405667735207)

            if dif < mindif:
                mindif = dif
                length = k

        return length

    # find key given length k
    def find_key(k, text):
        # split text and solve caesar cipher
        currkey = ""
        for i in range(k):
            split = ""  # string starts empty
            for j in range(0, len(text[i:]), k):  # starting from ith letter, add every kth letter
                split += text[i + j]

            least_chisq = 100000
            next_char = 'A'

            # shift split by each letter for Caesar cipher
            for a in alphabet:
                # shift each character by one
                new_split = ""
                for char in split:
                    new_split += shift_letter(char, 'B')
                split = new_split

                # chi-squared analysis on letter frequencies
                chisq = 0
                for letter in alphabet:
                    chisq += (get_freq(letter, split) - letter_freqs[letter])**2 / letter_freqs[letter]
                if chisq < least_chisq:
                    least_chisq = chisq
                    next_char = shift_letter(a, 'Z')

            currkey += next_char

        return currkey

    kl = key_length(cipher)
    key = find_key(kl, cipher)
    print(key)
