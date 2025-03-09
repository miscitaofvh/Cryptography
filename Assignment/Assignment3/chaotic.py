def logistic_map(x: float) -> float:
    if (x < 0.5): 
        return 2 * x
    else: 
        return 2 * x - 1
    
def chaotic_encrypt_decrypt(input_path: str, output_path: str, x0: float):
    """
    Encrypt or decrypt a file (any binary) using a Logistic map-based keystream.
    XOR is used for both encryption and decryption.
    
    :param input_path: path to the input file
    :param output_path: path to the output file
    :param x0: initial seed for the Logistic map
    """
    # Read entire file in binary mode
    with open(input_path, 'rb') as f_in:
        data = f_in.read()

    length = len(data)
    # Generate keystream of the same length
    key = bytearray(length)
    x = x0
    for i in range(length):
        # Logistic map iteration
        x = logistic_map(x)
        # Map x from (0..1) to a byte (0..255)
        key[i] = int(x * 256) & 0xFF

    # XOR each byte
    result = bytes(d ^ k for d, k in zip(data, key))

    # Write result to output
    with open(output_path, 'wb') as f_out:
        f_out.write(result)

def main():
    mode = input("Enter mode (encrypt/decrypt): ").strip().lower()
    if mode not in ("encrypt", "decrypt"):
        print("Invalid mode. Use 'encrypt' or 'decrypt'.")
        return
    input_file = input("Enter path to input file: ").strip()
    output_file = input("Enter path to output file: ").strip()
    try:
        x0 = float(input("Enter logistic map seed x0 (0 < x0 < 1): ").strip())
    except ValueError:
        print("Invalid seed value. Must be a float.")
        return

    if not (0 < x0 < 1):
        print("Invalid seed value. Must be in the range (0, 1).")
        return
    
    chaotic_encrypt_decrypt(input_file, output_file, x0)

    print(f"\nDone. Output written to {output_file}.")
if __name__ == "__main__":
    main()