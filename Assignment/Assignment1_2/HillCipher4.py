import numpy as np
import string 
def print_key_matrix(matrix):
    """
    Prints a matrix in a formatted manner.
    """
    for row in matrix:
        print(" ".join(f"{num:3}" for num in row))


def mod_inverse(a, mod):
    for i in range(1, mod):
        if (a * i) % mod == 1:
            return i
    return None  

def insert(character, text, index):
    """
    Inserts a character into a string at the specified index.
    """
    if (index == len(text)):
        return text + character
    return text[:index] + character + text[index:]

def get_inverse_key_matrix(matrix, mod=26):
    det = int(round(np.linalg.det(matrix))) 
    det = det % mod  
    #print(det)
    det_inv = mod_inverse(det, mod)  
    if det_inv is None:
        return None 
    
    adjugate = np.round(np.linalg.inv(matrix) * det).astype(int) 
    inverse_matrix = (det_inv * adjugate) % mod  

    return inverse_matrix.tolist()

def hill_encrypt(plaintext, key_matrix):
    """
    Encrypts the plaintext using the Hill cipher with the provided 4x4 key matrix.
    Processes blocks of 4 letters at a time.
    """
    plaintext = plaintext.upper()
    letters = [char for char in plaintext if char.isalpha()]
    while len(letters) % 4 != 0:
        letters.append('X')

    ciphertext = ""
    plaintext_idx = 0
    letter_idx = 0
    for char in ciphertext:
        if char not in string.ascii_uppercase:
            ciphertext = insert(char, ciphertext, plaintext_idx)
        else:
            if letter_idx % 4 == 0:
                block = letters[letter_idx:letter_idx+4]
                block_vector = [ord(letter) - ord('A') for letter in block]
                encrypted_vector = [
                    sum(key_matrix[i][j] * block_vector[j] for j in range(4)) % 26
                    for i in range(4)
                ]
                cipher_block = "".join(chr(num + ord('A')) for num in encrypted_vector)
                ciphertext += cipher_block
            letter_idx += 1
        plaintext_idx += 1

    return ciphertext

def hill_decrypt(ciphertext, key_matrix):
    inv_matrix = get_inverse_key_matrix(key_matrix)
    if inv_matrix is None:
        raise ValueError("The key matrix is not invertible modulo 26.")
    ciphertext = ciphertext.upper()
    letters = [char for char in ciphertext if char.isalpha()]

    plaintext = ""
    ciphertext_idx = 0
    letter_idx = 0
    for char in ciphertext:
        if char not in string.ascii_uppercase:
            plaintext = insert(char, plaintext, ciphertext_idx)
        else:
            if (letter_idx % 4 == 0):
                block = letters[letter_idx:letter_idx+4]
                block_vector = [ord(letter) - ord('A') for letter in block]
                decrypted_vector = [
                    sum(inv_matrix[i][j] * block_vector[j] for j in range(4)) % 26
                    for i in range(4)
                ]
                plain_block = "".join(chr(num + ord('A')) for num in decrypted_vector)
                plaintext += plain_block
            letter_idx += 1
        ciphertext_idx += 1
    return plaintext

def main():
    print("Hill Cipher (4x4 Matrix)")
    print("Enter 16 integers (space-separated) to form the key matrix (row-wise):")
    try:
        values = list(map(int, input().split()))
        if (len(values) != 16):
            print("Please enter exactly 16 intergers.")
            return
    except ValueError:
        print("Invalid input. Please enter 16 integers separated by spaces.")
        return
    
    key_matrix = [values[0:4], values[4:8], values[8:12], values[12:16]]
    
    print("\nKey_matrix")
    print_key_matrix(key_matrix)

    inv_matrix = get_inverse_key_matrix(key_matrix)
    
    if inv_matrix is None:
        print("The key matrix is not invertible modulo 26.")
        return
    
    print("\nInverse Key Matrix:")
    print_key_matrix(inv_matrix)

    plaintext = input("\nEnter the plaintext to encrypt: ").upper()
    encrypted_text = hill_encrypt(plaintext, key_matrix)
    print("Encrypted Text: ")
    print(encrypted_text)

    input("Press Enter to continue to decryption...")
    decrypted_text = hill_decrypt(encrypted_text, key_matrix)
    print("Decrypted Text: ")
    print(decrypted_text)
if __name__ == "__main__":
    main()