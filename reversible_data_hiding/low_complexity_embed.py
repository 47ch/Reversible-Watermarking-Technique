from PIL import Image

def low_complexity_embed(image_path, secret_data, output_path, block_size=8):
    # Load the image and convert to grayscale if not already done
    image = Image.open(image_path).convert('L')
    pixel_map = image.load()
    width, height = image.size

    # Convert secret data to binary for the process dof embedding 
    binary_data = ''.join(format(byte, '08b') for byte in bytearray(secret_data, encoding='utf-8'))

    # Divide image into blocks and embed the data given
    index = 0
    for i in range(0, width, block_size):
        for j in range(0, height, block_size):
            if index < len(binary_data):
                for m in range(block_size):
                    for n in range(block_size):
                        if i+m < width and j+n < height and index < len(binary_data):
                            # Modify the LSB of the pixel to hide the secret bit
                            pixel_value = pixel_map[i+m, j+n]
                            pixel_bin = format(pixel_value, '08b')
                            new_pixel_bin = pixel_bin[:-1] + binary_data[index]
                            pixel_map[i+m, j+n] = int(new_pixel_bin, 2)
                            index += 1

    # Save the image with embedded data
    image.save(output_path)
    image.show()

low_complexity_embed('encrypted_image2.tiff', 'This is a secret message', 'embedded_image2.tiff')
