import math

def modinv(a, m):
    """
    Returns the modular inverse of a modulo m.
    This function returns x such that (a * x) % m == 1.
    """
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None
def cryptanalysisAffineCipher(ciphertext):
    for a in range(26):
        for b in range(26):
            if math.gcd(a, 26) != 1:
                continue
            plaintext = ""
            for i in range(len(ciphertext)):
                if ciphertext[i].isalpha():
                    if ciphertext[i].isupper():
                        plaintext += chr(((ord(ciphertext[i]) - 65 - b) * modinv(a, 26)) % 26 + 65)
                    else:
                        plaintext += chr(((ord(ciphertext[i]) - 97 - b) * modinv(a, 26)) % 26 + 97)
                else:
                    plaintext += ciphertext[i]
            print("a = " + str(a) + "\nb = " + str(b) + "\nplaintext: " + plaintext)
def main():
    ciphertext = input("Enter the ciphertext for cryptanalysis: ")
    cryptanalysisAffineCipher(ciphertext)
if __name__ == "__main__":
    main()