from LSB_embedding import *
import os

def data_extraction(image_path, output_path, group_size, data_hiding_key, t=1):
    """
    Extracting data by using the data hiding key to find pixel groups for set A and set B, then
    flipping the t-th LSB of all pixels within each pixel group, creating Gi and FGi, which stands
    for the pixel group and flipped pixel group. The two-round interpolation technique is used to 
    judge which of these pixel groups are correct for set A. After all pixels of set A have been 
    recovered to their original values, the pixel groups for set B are reconstructed. A similar 
    process of flipping pixel groups are done for set B, but the pixel prediction is executed with 
    the variant cubic based bicubic interpolation algorithm.
    """
    returned_data = ""
    embedded_bits = ""
    # Load the decrypted image
    image_full_path = os.path.join("reversible-data-hiding", image_path)
    output_full_path = os.path.join("reversible-data-hiding", output_path)
    
    image = Image.open(image_full_path).convert('L')   
    pixel_map = image.load()
    width, height = image.size

    # Initialize random seed for reproducibility
    random.seed(data_hiding_key)

    # copy input image twice for spatial correlation comparison
    h0_image = image.copy()
    h0_pixelmap = h0_image.load()
    h1_image = image.copy()
    h1_pixelmap = h1_image.load()

    # Define sets A and B based on pixel positions
    set_a = []
    set_b = []

    for i in range(height):
        for j in range(width):
            if i % 2 == 0 and j % 2 == 1:  # Set A: even rows, odd columns
                set_a.append((i, j))
            elif i % 2 == 1 and j % 2 == 0:  # Set B: odd rows, even columns
                set_b.append((i, j))

    # Function to flip the t-th least significant bit of a pixel
    def flip_t_bit(pixel_value, bit, t):
        mask = 1 << (t - 1)
        return (pixel_value & ~mask) | ((bit << (t - 1)) & mask)

    # Shuffle the pixel groups using the data hiding key
    random.shuffle(set_a)
    random.shuffle(set_b)

    # Split Set A and Set B into non-overlapping groups
    def create_groups(pixel_set, group_size):
        groups = [pixel_set[i:i+group_size] for i in range(0, len(pixel_set), group_size)]
        return groups

    groups_a = create_groups(set_a, group_size)
    groups_b = create_groups(set_b, group_size)

    # Embed data into Set A (simplified embedding for demo purposes)
    for group in groups_a:
        if bit_index >= len(secret_bits):
            break
        for pixel in group:
            if bit_index >= len(secret_bits):
                break
            pixel_value = pixel_map[pixel]
            bit_to_embed = int(secret_bits[bit_index])
            bit_index += 1
            # Flip the t-th LSB to embed the bit
            pixel_map[pixel] = flip_t_bit(pixel_value, bit_to_embed, t)

    # Embed data into Set B (optional, depending on available data)
    for group in groups_b:
        if bit_index >= len(secret_bits):
            break
        for pixel in group:
            if bit_index >= len(secret_bits):
                break
            pixel_value = pixel_map[pixel]
            bit_to_embed = int(secret_bits[bit_index])
            bit_index += 1
            # Flip the t-th LSB to embed the bit
            pixel_map[pixel] = flip_t_bit(pixel_value, bit_to_embed, t)

    # Save the image with the embedded data
    image.save(output_image_path, format="tiff")
    print("Data embedding completed and saved as", output_image_path)
    image.show()