import random
from PIL import Image

def data_embedding_paper(image_path, secret_data, output_path, block_size, data_hiding_key=1234):
    # Load the encrypted image
    secret_data = secret_data + "***"
    image = Image.open(image_path).convert('L')
    pixel_map = image.load()
    width, height = image.size
    
    # Convert secret data to binary
    binary_data = ''.join(format(byte, '08b') for byte in bytearray(secret_data, encoding='utf-8'))

    # Initialize random seed for reproducibility
    random.seed(data_hiding_key)
    
    # Segmentation of encrypted image into non-overlapping blocks
    index = 0
    for i in range(0, width, block_size):
        for j in range(0, height, block_size):
            if index < len(binary_data):
                # Each block will be used to carry one additional bit
                block_pixels = []
                for m in range(block_size):
                    for n in range(block_size):
                        if i + m < width and j + n < height:
                            block_pixels.append((i + m, j + n))
                
                # Pseudo-randomly divide pixels into two sets (Set A and Set B)
                set_A = []
                set_B = []
                for pixel in block_pixels:
                    if random.random() < 0.5:
                        set_A.append(pixel)
                    else:
                        set_B.append(pixel)
                
                # Embed the bit into the block
                if binary_data[index] == '0':
                    # Flip the LSBs of pixels in Set A
                    for pixel in set_A:
                        pixel_value = pixel_map[pixel]
                        pixel_bin = format(pixel_value, '08b')
                        new_pixel_bin = pixel_bin[:-3] + ''.join(['1' if b == '0' else '0' for b in pixel_bin[-3:]])
                        pixel_map[pixel] = int(new_pixel_bin, 2)
                else:
                    # Flip the LSBs of pixels in Set B
                    for pixel in set_B:
                        pixel_value = pixel_map[pixel]
                        pixel_bin = format(pixel_value, '08b')
                        new_pixel_bin = pixel_bin[:-3] + ''.join(['1' if b == '0' else '0' for b in pixel_bin[-3:]])
                        pixel_map[pixel] = int(new_pixel_bin, 2)
                
                index += 1

    # Save the image with embedded data
    image.save(output_path)
    # image.show()
    

# Example usage:
# data_embedding_paper('encrypted_image.tiff', 'Secret', 'embedded_image123.tiff', block_size=32, data_hiding_key=1234)
