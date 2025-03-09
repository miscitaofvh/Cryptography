from collections import Counter
import string

# Known English letter frequencies (from most frequent to least frequent)
english_frequencies = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

cipher_text = ("Yfhac bzc xcrcqyc vp bzc pfxyb hvicr, Zqxxs Evbbcx qhw bzc Ezfrvyvezcx'y Ybvhc, vh 26 Gjhc 1997, bzc nvvoy zqic pvjhw fkkchyc evejrqxfbs qhw avkkcxafqr yjaacyy uvxrwufwc. Bzcs zqic qbbxqabcw q ufwc qwjrb qjwfchac qy ucrr qy svjhdcx xcqwcxy qhw qxc ufwcrs avhyfwcxcw avxhcxybvhcy vp kvwcxh rfbcxqbjxc,[3][4] bzvjdz bzc nvvoy zqic xcacficw kfmcw xcifcuy pxvk axfbfay qhw rfbcxqxs yazvrqxy. Qy vp Pcnxjqxs 2023, bzc nvvoy zqic yvrw kvxc bzqh 600 kfrrfvh avefcy uvxrwufwc, kqofhd bzck bzc ncyb-ycrrfhd nvvo ycxfcy fh zfybvxs, qiqfrqnrc fh wvtchy vp rqhdjqdcy. Bzc rqyb pvjx nvvoy qrr ycb xcavxwy qy bzc pqybcyb-ycrrfhd nvvoy fh zfybvxs, ufbz bzc pfhqr fhybqrkchb ycrrfhd xvjdzrs 2.7 kfrrfvh avefcy fh bzc Jhfbcw Ofhdwvk qhw 8.3 kfrrfvh avefcy fh bzc Jhfbcw Ybqbcy ufbzfh buchbs-pvjx zvjxy vp fby xcrcqyc. Fb zvrwy bzc Djfhhcyy Uvxrw Xcavxw pvx Ncyb-ycrrfhd nvvo ycxfcy pvx azfrwxch")

# Count letter frequencies in the ciphertext (ignoring non-alphabet characters)
cipher_counts = Counter(''.join(filter(str.isalpha, cipher_text.upper())))

# Sort the ciphertext letters by frequency (most frequent first)
sorted_cipher = ''.join([item[0] for item in cipher_counts.most_common()])

# Create an initial mapping from ciphertext letters to the English frequency order
mapping = {}
for i, letter in enumerate(sorted_cipher):
    mapping[letter] = english_frequencies[i]

# For any letters not present in the ciphertext, add an identity mapping
for letter in string.ascii_uppercase:
    if letter not in mapping:
        mapping[letter] = letter

# Optional manual adjustments to improve decryption quality
mapping["V"] = "O"
mapping["H"] = "N"
mapping["Z"] = "H"
mapping["B"] = "T"

def print_key_mapping_table(mapping):
    """
    Displays the key mapping in the requested table format:
    
     A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
     --+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--
     R  A  T  X  U  K  E  Y  H  O  I  D  V  F  G  M  P  L  Z  W  S  Q  J  C  B  N
    """
    plain_letters = list(string.ascii_uppercase)
    # Build the first row: plain letters with a fixed width (2 characters per letter)
    row1 = " ".join(f"{letter:2}" for letter in plain_letters)
    # Build the border row: "--+--+...+--"
    row2 = " " + "--" + "+--"*(len(plain_letters)-1) + " "
    # Build the third row: corresponding cipher letters from the mapping
    row3 = " ".join(f"{mapping[letter]:2}" for letter in plain_letters)
    
    print(row1)
    print(row2)
    print(row3)

# Display the final mapping using the desired table format
print_key_mapping_table(mapping)

# Decrypt the ciphertext using the mapping (preserving letter case)
decrypted_text = []
for char in cipher_text:
    if char.isalpha():
        if char.isupper():
            decrypted_text.append(mapping.get(char, char))
        else:
            decrypted_text.append(mapping.get(char.upper(), char.upper()).lower())
    else:
        decrypted_text.append(char)
decrypted_text = ''.join(decrypted_text)

print("\nDecrypted Text:")
print(decrypted_text)
