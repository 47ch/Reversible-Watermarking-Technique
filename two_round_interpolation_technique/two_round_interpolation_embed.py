from PIL import Image

def two_round_interpolation_embed(image_path, secret_data, output_path):
    # Loading the image and convert to grayscale if not already done
    image = Image.open(image_path).convert('L')
    pixel_map = image.load()
    width, height = image.size

    # Convert secret data to binary for the process of embeddding
    binary_data = ''.join(format(byte, '08b') for byte in bytearray(secret_data, encoding='utf-8'))

    # Divide the image into reference and carrier pixels
    index = 0
    for i in range(1, width-1, 2):  
        for j in range(1, height-1, 2):  
            if index < len(binary_data):
                # First round - Set A
                pixel_value = pixel_map[i, j]
                pixel_bin = format(pixel_value, '08b')
                new_pixel_bin = pixel_bin[:-1] + binary_data[index]
                pixel_map[i, j] = int(new_pixel_bin, 2)
                index += 1

                # Second round - Set B (if data remains)
                if index < len(binary_data):
                    pixel_value = pixel_map[i+1, j+1]
                    pixel_bin = format(pixel_value, '08b')
                    new_pixel_bin = pixel_bin[:-1] + binary_data[index]
                    pixel_map[i+1, j+1] = int(new_pixel_bin, 2)
                    index += 1

    # Save the image with embedded data
    image.save(output_path)
    image.show()


two_round_interpolation_embed('encrypted_image.tiff', 'This is a secret message', 'embedded_image.tiff')
