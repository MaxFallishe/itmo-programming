import random
import typing as tp


def is_prime(n: int) -> bool:
    """
    Tests to see if a number is prime.

    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    # PUT YOUR CODE HERE
    if n > 1:
        temp_divider = 2
        while n % temp_divider != 0:
            temp_divider += 1

        return n == temp_divider
    else:
        return False


def gcd(a: int, b: int) -> int:
    """
    Euclid's algorithm for determining the greatest common divisor.

    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    # PUT YOUR CODE HERE
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a

    greater_common_divisor = a + b

    return greater_common_divisor


def multiplicative_inverse(e: int, phi: int) -> int:
    """
    Euclid's extended algorithm for finding the multiplicative
    inverse of two numbers.

    >>> multiplicative_inverse(7, 40)
    23
    """
    # PUT YOUR CODE HERE
    x1, x2, x3 = 1, 0, phi
    y1, y2, y3 = 0, 1, e

    while y3 != 1:
        if y3 == 0:
            return 0
        qfc = x3 // y3
        t1 = x1 - qfc * y1
        t2 = x2 - qfc * y2
        t3 = x3 - qfc * y3

        x1, x2, x3 = y1, y2, y3
        y1, y2, y3 = t1, t2, t3

    nod = y2 % phi
    return nod


print(multiplicative_inverse(42, 2017))


def generate_keypair(
    p: int, q: int
) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q cannot be equal")

    # n = pq
    # PUT YOUR CODE HERE
    n = p * q

    # phi = (p-1)(q-1)
    # PUT YOUR CODE HERE
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are coprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def encrypt(pk: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk: tp.Tuple[int, int], ciphertext: tp.List[int]) -> str:
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return "".join(plain)


if __name__ == "__main__":
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print("".join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
