def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    # PUT YOUR CODE HERE

    if len(keyword) < len(plaintext):
        keyword = keyword * ((len(plaintext) // len(keyword)) + 1)

    keyword = keyword.lower()
    lower_letters_ords = [i for i in range(ord("a"), ord("z") + 1)]

    for letter_index in range(len(plaintext)):
        letter = plaintext[letter_index]
        shift = ord(keyword[letter_index]) - 97
        upper_flag = False
        if letter.isupper():
            upper_flag = True
        letter = letter.lower()
        if ord(letter) in lower_letters_ords:
            caesar_letter = chr(ord(letter) + shift)
            if shift > 26:
                shift = shift % 26
            if ord(caesar_letter) not in lower_letters_ords:
                caesar_letter = chr(
                    min(lower_letters_ords)
                    + (ord(caesar_letter) - max(lower_letters_ords))
                    - 1
                )
            if upper_flag is True:
                caesar_letter = chr(ord(caesar_letter) - 32)
            ciphertext += caesar_letter
        else:
            ciphertext += letter

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    if len(keyword) < len(ciphertext):
        keyword = keyword * ((len(ciphertext) // len(keyword)) + 1)

    keyword = keyword.lower()

    lower_letters_ords = [i for i in range(ord("a"), ord("z") + 1)]

    for letter_index in range(len(ciphertext)):
        letter = ciphertext[letter_index]
        shift = ord(keyword[letter_index]) - 97
        upper_flag = False
        if letter.isupper():
            upper_flag = True
        letter = letter.lower()

        if ord(letter) in lower_letters_ords:
            caesar_letter = chr(ord(letter) - shift)
            if shift > 26:
                shift = shift % 26
            if ord(caesar_letter) not in lower_letters_ords:
                caesar_letter = chr(
                    max(lower_letters_ords)
                    - (min(lower_letters_ords) - ord(caesar_letter))
                    + 1
                )

            if upper_flag is True:
                caesar_letter = chr(ord(caesar_letter) - 32)
            plaintext += caesar_letter
        else:
            plaintext += letter

    return plaintext
