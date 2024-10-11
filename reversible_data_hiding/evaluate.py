import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from reversible_data_hiding.image_encryption2 import encrypt_image
from reversible_data_hiding.data_embedding import data_embedding_paper
from reversible_data_hiding.ch_data_extraction_ver1 import decrypt_image, data_extraction, calculate_ber, plot_ber_vs_block_size
import os

def calculate_psnr(original_image_path, decrypted_image_path):
    original = Image.open(original_image_path).convert('L')
    decrypted = Image.open(decrypted_image_path).convert('L')

    # Convert images to numpy arrays
    original_array = np.array(original)
    decrypted_array = np.array(decrypted)

    # Calculate the mean squared error (MSE)
    mse = np.mean((original_array - decrypted_array) ** 2)

    # Calculate the PSNR
    if mse == 0:
        return float('inf')
    psnr = 10 * np.log10(255 * 255 / mse)
    return psnr

def run_experiment(image_path, output_path, secret_data, key, block_sizes, data_hiding_key=1234):
    ber_values = []

    # Get only the image filename, not the full path
    image_filename = os.path.basename(image_path)

    for block_size in block_sizes:
        print(f"Running for block size: {block_size} on {image_path}")

        # Corrected file paths
        encrypted_image_path = f"encrypted_{image_filename}"
        output_image_path = f"embedded_{encrypted_image_path}"
        decrypted_image_path = f"decrypted_{encrypted_image_path}"

        # 1. Encrypt the image
        encrypt_image(image_path, encrypted_image_path, key)

        # 2. Embed the data into the encrypted image
        data_embedding_paper(encrypted_image_path, secret_data, output_image_path, block_size, data_hiding_key)

        # 3. Decrypt the image with embedded data
        decrypt_image(output_image_path, decrypted_image_path, key)

        # 4. Extract the data from the decrypted image
        extracted_bits = data_extraction(decrypted_image_path, output_path, block_size, data_hiding_key)

        # Convert the original secret data to binary for comparison
        original_bits = ''.join(format(byte, '08b') for byte in bytearray(secret_data, encoding='utf-8'))

        # Calculate BER
        ber = calculate_ber(extracted_bits, original_bits)
        ber_values.append(ber*100)  # Convert to percentage for visualization (similar to the paper)
        print(f"BER for block size {block_size}: {ber}%")

        psnr_value = calculate_psnr(image_path, decrypted_image_path)
        print(f"PSNR for block size {block_size}: {psnr_value:.2f} dB")

    return block_sizes, ber_values

def plot_multiple_ber(block_sizes, ber_results, image_names):
    plt.figure(figsize=(10, 6))

    for ber_values, image_name in zip(ber_results, image_names):
        plt.plot(block_sizes, ber_values, marker='o', label=image_name)

    plt.title('Extracted-Bit Error Rate with Respect to Block Sizes')
    plt.xlabel('Block Size')
    plt.ylabel('Extracted-bit Error Rate (%)')
    plt.legend()
    plt.grid(True)
    plt.show()