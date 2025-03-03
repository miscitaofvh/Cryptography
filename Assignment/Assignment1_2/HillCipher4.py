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

def determinant3(key_matrix):
    a, b, c = key_matrix[0]
    d, e, f = key_matrix[1]
    g, h, i = key_matrix[2]
    
    det = (a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g))
    return det

def get_inverse_key_matrix(key_matrix):

    cofactor = []
    for i in range(4):
        cofactor_row = []
        for j in range(4):
            submatrix = [row[:j] + row[j+1:] for row in key_matrix[:i] + key_matrix[i+1:]]
            cofactor_row.append(((-1) ** (i+j)) * determinant3(submatrix) % 26)
        cofactor.append(cofactor_row)

    det = 0

    for i in range(4):
        det += key_matrix[0][i] * cofactor[0][i]
    
    det = det % 26

    inv_det = mod_inverse(det, 26)
    if inv_det is None:
        return None

    adjugate = []
    for j in range(4):
        adjugate_row = [cofactor[i][j] for i in range(4)]
        adjugate.append(adjugate_row)
        
    inv_matrix = [[adjugate[row][col] * inv_det % 26 for col in range(4)] for row in range(4)]
    
    return inv_matrix

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
    for char in plaintext:
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