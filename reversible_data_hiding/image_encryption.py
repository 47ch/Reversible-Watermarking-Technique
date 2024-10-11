from PIL import Image 
  
# Import an image from directory: 
input_image = Image.open("7.1.07.tiff") 
  
# Extracting pixel map: 
pixel_map = input_image.load() 
  
# Extracting the width and height  
# of the image: 
width, height = input_image.size 
  
'''
Encryption process by looping through every pixel, using width and height as limits.
Each bit within the original pixel value undergoes a XOR operation with a bit generated using standard stream cipher.
The resulting bits from the operation are then added together to produce a modified pixel. 
'''
for i in range(width): 
    for j in range(height): 
        
        # getting the pixel value. 
        pixel_value = input_image.getpixel((i, j)) 
        after_encryption_pixel_value = 0

        for k in range(8):
            bit = (pixel_value/(2**k))%2

            # insert function for XOR operation with generated bit
            # bit is generated using standard stream cipher

            # resulting_bit as result of XOR operation between original bit and generated bit

            # UNCOMMENT THIS 
            #after_encryption_pixel_value += resulting_bit*(2**k)
            
    pixel_map[i,j] = int(after_encryption_pixel_value)
  
# Saving the final output 
input_image.save("encrypted", format="tiff") 
  
# use input_image.show() to see the image on the 
# output screen. 
# show encrypted version of image
#input_image.show("encrypted.tiff")