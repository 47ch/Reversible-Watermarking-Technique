
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util import Counter

'''
Encryption process by looping through every pixel, using width and height as limits.
Each bit within the original pixel value undergoes a XOR operation with a bit generated using standard stream cipher.
The resulting bits from the operation are then added together to produce a modified pixel. 
'''

def aesCTR(key, num_bits):
    # Create a counter object for AES-CTR mode
    counter = Counter.new(128)
    
    # Create a new AES cipher object in CTR mode
    cipher = AES.new(key, AES.MODE_CTR, counter=counter)
    
    # Generate the pseudo-random bits
    num_bytes = (num_bits + 7) // 8
    random_bytes = cipher.encrypt(b'\x00' * num_bytes)
    
    # Convert bytes to bits
    random_bits = []
    for byte in random_bytes:
        for i in range(8):
            random_bits.append((byte >> (7 - i)) & 1)
    
    return random_bits

def encrypt_image(input_image_path, output_image_path, key):
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
    encrypted_image = Image.new("L", (width, height))
    pixel_map = encrypted_image.load()
    
    # Encryption process
    for i in range(width):
        for j in range(height):
            # Getting the pixel value
            pixel_value = input_image.getpixel((i, j))
            after_encryption_pixel_value = 0
            
            for k in range(8):
                # Bit extraction using division and modulo
                bit = (pixel_value // (2 ** k)) % 2
                
                # Get the corresponding pseudo-random bit
                random_bit = stream_cipher[bit_index]
                bit_index += 1
                
                # XOR operation with generated bit
                resulting_bit = bit ^ random_bit
                
                after_encryption_pixel_value += resulting_bit * (2 ** k)
            
            # Update the pixel value with the encrypted value
            pixel_map[i, j] = int(after_encryption_pixel_value)
    
    # Saving the final output
    encrypted_image.save(output_image_path, format="tiff")
    
    # Show encrypted version of image
    encrypted_image.show()

# key = b'pzkUHwYaLVLml0hh' 
# encrypt_image("7.1.07.tiff", "encrypted_image2.tiff", key)