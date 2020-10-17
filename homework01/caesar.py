import typing as tp
import time


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    lower_letters_ords = [i for i in range(97, 122+1)]

    for letter in plaintext:
        upper_flag = False

        if letter.isupper():
            upper_flag = True

        letter = letter.lower()

        if ord(letter) in lower_letters_ords:

            caesar_letter = chr(ord(letter)+shift)

            if shift > 26:
                shift = shift % 26

            if ord(caesar_letter) not in lower_letters_ords:
                caesar_letter = chr(min(lower_letters_ords) + (ord(caesar_letter) - max(lower_letters_ords))-1)

            if upper_flag is True:
                caesar_letter = chr(ord(caesar_letter)-32)

            ciphertext += caesar_letter

        else:
            ciphertext += letter

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    # PUT YOUR CODE HERE

    lower_letters_ords = [i for i in range(97, 122 + 1)]

    for letter in ciphertext:
        upper_flag = False

        if letter.isupper():
            upper_flag = True

        letter = letter.lower()

        if ord(letter) in lower_letters_ords:

            caesar_letter = chr(ord(letter) - shift)

            if shift > 26:
                shift = shift % 26

            if ord(caesar_letter) not in lower_letters_ords:
                caesar_letter = chr(max(lower_letters_ords) - (min(lower_letters_ords) - ord(caesar_letter)) + 1)

            if upper_flag is True:
                caesar_letter = chr(ord(caesar_letter) - 32)

            plaintext += caesar_letter

        else:
            plaintext += letter

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
