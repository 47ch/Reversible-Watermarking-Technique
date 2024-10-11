from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util import Counter
from image_encryption import aesCTR
import random

def decrypt_image(input_image_path, output_image_path, key):
    '''
    Decryption process is similar to encryption process, just done it reverse using the same key.
    '''
    # Ensure key is 16 bytes long (128 bits)
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes (128 bits) long.")
    
    # Import an image from directory
    input_image = Image.open(input_image_path)
    
    # Extracting the width and height of the image
    width, height = input_image.size
    
    # Generate pseudo-random bits using AES-CTR
    num_bits = width * height * 8
    stream_cipher = aesCTR(key, num_bits)
    
    bit_index = 0
    
    # Create a new image for the encrypted output
    decrypted_image = Image.new("L", (width, height))
    pixel_map = decrypted_image.load()
    
    # Decryption process
    for i in range(width):
        for j in range(height):
            # Getting the pixel value
            pixel_value = input_image.getpixel((i, j))
            after_decryption_pixel_value = 0
            
            for k in range(8):
                # Bit extraction using division and modulo
                bit = (pixel_value // (2 ** k)) % 2
                
                # Get the corresponding pseudo-random bit
                random_bit = stream_cipher[bit_index]
                bit_index += 1
                
                # XOR operation with generated bit
                resulting_bit = bit ^ random_bit
                
                after_decryption_pixel_value += resulting_bit * (2 ** k)
            
            # Update the pixel value with the encrypted value
            pixel_map[i, j] = int(after_decryption_pixel_value)
    
    # Saving the final output
    decrypted_image.save(output_image_path, format="tiff")
    
    # Show encrypted version of image
    decrypted_image.show()