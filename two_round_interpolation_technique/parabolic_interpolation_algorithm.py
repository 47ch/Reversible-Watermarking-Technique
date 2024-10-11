from PIL import Image
import numpy as np
import math

def parabolic_interpolation_algorithm(image_path, output_path, data_hiding_key):
    """
    Prediction algorithm for set A.
    Set divided into 4 subcategories: second row, second last row, second last column, and anything else.
    Each subcategory goes through a different calculation.
    """

    circle_set = []
    triangle_set = []
    # Load the decrypted image
    image = Image.open(image_path).convert('L')
    pixel_map = image.load()
    width, height = image.size
    root_5 = math.sqrt(5)
    root_2 = math.sqrt(2)

    for m in range((height/2) - 1):
        for n in range((width/2)-1):
            circle_set.append((2*m,2*n+1))

    for m in range((height/2) - 1):
        for n in range((width/2)-1):
            triangle_set.append((2*m+1,2*n))

    for pixel in circle_set:
        if pixel[1] == 1:
            """
            Where pixel is in second row of image.
            Pixel on image is replaced at the end of if statement.
            """
            k = 0.1 #[0.1,0.2,0.3...1]
            mat1 = np.array([2**2,2,1])
            mat2 = np.array([1/8,-1/4,1/8],
                            [-1,3/2,-1/2],
                            [15/8,-5/4,3/8])
            mat3 = np.array([pixel_map[pixel[0]-1,pixel[1]]],
                            [pixel_map[pixel[0]+1,pixel[1]]],
                            [pixel_map[pixel[0]+3,pixel[1]]])
            
            f1 = np.matmul(np.matmul(mat1,mat2),mat3)
        
            resulting_pixel = k*f1+(1-k)*((pixel_map[pixel[0]-1,pixel[1]-2]/root_5)+
                                            (pixel_map[pixel[0]-1,pixel[1]])+
                                            (pixel_map[pixel[0]-1,pixel[1]+2]/root_5)+
                                            (pixel_map[pixel[0]+1,pixel[1]-2]/root_5)+
                                            (pixel_map[pixel[0]+1,pixel[1]])+
                                            (pixel_map[pixel[0]+1,pixel[1]+2]/root_5))/((4/root_5)+2)
            
            pixel_map(pixel[0],pixel[1]) = resulting_pixel

        if pixel[1] == height-2:
            k = 0.1 #[0.1,0.2,0.3...1]
            mat1 = np.array([4**2,4,1])
            mat2 = np.array([1/8,-1/4,1/8],
                            [-1,3/2,-1/2],
                            [15/8,-5/4,3/8])
            mat3 = np.array([pixel_map[pixel[0]-3,pixel[1]]],
                            [pixel_map[pixel[0]-1,pixel[1]]],
                            [pixel_map[pixel[0]+1,pixel[1]]])
            f1 = np.matmul(np.matmul(mat1,mat2),mat3)

            mat1 = np.array([2**2,2,1])
            mat2 = np.array([1/6,-1/2,1/3],
                            [-7/6,5/2,-4/3],
                            [2,-2,1 ])
            mat3 = np.array([pixel_map[pixel[0]-1,pixel[1]]],
                            [pixel_map[pixel[0]+1,pixel[1]]],
                            [pixel_map[pixel[0]+2,pixel[1]]])
            f2 = np.matmul(np.matmul(mat1,mat2),mat3)   

            resulting_pixel = k*((f1+f2)/2)+(1-k)*((pixel_map[pixel[0]-1,pixel[1]-2]/root_5)+
                                            (pixel_map[pixel[0]-1,pixel[1]])+
                                            (pixel_map[pixel[0]-1,pixel[1]+2]/root_5)+
                                            (pixel_map[pixel[0]+1,pixel[1]-2]/root_5)+
                                            (pixel_map[pixel[0]+1,pixel[1]])+
                                            (pixel_map[pixel[0]+1,pixel[1]+2]/root_5))/((4/root_5)+2)
            
        if pixel[0] == width-1:
            k = 0.1 #[0.1,0.2,0.3...1]
            mat1 = np.array([4**2,4,1])
            mat2 = np.array([1/8,-1/4,1/8],
                            [-1,3/2,-1/2],
                            [15/8,-5/4,3/8])
            mat3 = np.array([pixel_map[pixel[0]-3,pixel[1]]],
                            [pixel_map[pixel[0]-1,pixel[1]]],
                            [pixel_map[pixel[0]+1,pixel[1]]])
            f1 = np.matmul(np.matmul(mat1,mat2),mat3)

            mat1 = np.array([2**2,2,1])
            mat2 = np.array([1/8,-1/4,1/8],
                            [-1,3/2,-1/2],
                            [15/8,-5/4,3/8])
            mat3 = np.array([pixel_map[pixel[0]-1,pixel[1]]],
                            [pixel_map[pixel[0]+1,pixel[1]]],
                            [pixel_map[pixel[0]+2,pixel[1]]])
            f2 = np.matmul(np.matmul(mat1,mat2),mat3)   

            resulting_pixel = k*((f1+f2)/2)+(1-k)*((pixel_map[pixel[0]-1,pixel[1]-2]/root_5)+
                                            (pixel_map[pixel[0]-1,pixel[1]])+
                                            (pixel_map[pixel[0]-1,pixel[1]+1]/root_2)+
                                            (pixel_map[pixel[0],pixel[1]+1])+
                                            (pixel_map[pixel[0]+1,pixel[1]-2]/root_5)+
                                            (pixel_map[pixel[0]+1,pixel[1]])+
                                            (pixel_map[pixel[0]+1,pixel[1]+1]/root_2))/((2/root_5)+(2/root_2)+3)

        else:
            k = 0.1 #[0.1,0.2,0.3...1]
            mat1 = np.array([4**2,4,1])
            mat2 = np.array([1/8,-1/4,1/8],
                            [-1,3/2,-1/2],
                            [15/8,-5/4,3/8])
            mat3 = np.array([pixel_map[pixel[0]-3,pixel[1]]],
                            [pixel_map[pixel[0]-1,pixel[1]]],
                            [pixel_map[pixel[0]+1,pixel[1]]])
            f1 = np.matmul(np.matmul(mat1,mat2),mat3)

            mat1 = np.array([2**2,2,1])
            mat2 = np.array([1/8,-1/4,1/8],
                            [-1,3/2,-1/2],
                            [15/8,-5/4,3/8])
            mat3 = np.array([pixel_map[pixel[0]-1,pixel[1]]],
                            [pixel_map[pixel[0]+1,pixel[1]]],
                            [pixel_map[pixel[0]+2,pixel[1]]])
            f2 = np.matmul(np.matmul(mat1,mat2),mat3)   
                
            resulting_pixel = k*((f1+f2)/2)+(1-k)*((pixel_map[pixel[0]-1,pixel[1]-2]/root_5)+
                                            (pixel_map[pixel[0]-1,pixel[1]])+
                                            (pixel_map[pixel[0]-1,pixel[1]+2]/root_5)+
                                            (pixel_map[pixel[0]+1,pixel[1]-2]/root_5)+
                                            (pixel_map[pixel[0]+1,pixel[1]])+
                                            (pixel_map[pixel[0]+1,pixel[1]+2]/root_5))/((4/root_5)+2)
        
        pixel_map[pixel[0],pixel[1]] = resulting_pixel
            
    for pixel in triangle_set:
        if pixel[1] == 2:
            """
            Where pixel is in second row of image.
            Pixel on image is replaced at the end of if statement.
            """
            k = 0.1 #[0.1,0.2,0.3...1]
            mat1 = np.array([2**2,2,1])
            mat2 = np.array([1/8,-1/4,1/8],
                            [-1,3/2,-1/2],
                            [15/8,-5/4,3/8])
            mat3 = np.array([pixel_map[pixel[0],pixel[1]-1]],
                            [pixel_map[pixel[0],pixel[1]+1]],
                            [pixel_map[pixel[0],pixel[1]+3]])
            
            f1 = np.matmul(np.matmul(mat1,mat2),mat3)
        
            resulting_pixel = k*f1+(1-k)*((pixel_map[pixel[0]-2,pixel[1]-1]/root_5)+
                                            (pixel_map[pixel[0],pixel[1]-1])+
                                            (pixel_map[pixel[0]+2,pixel[1]-1]/root_5)+
                                            (pixel_map[pixel[0]-2,pixel[1]+1]/root_5)+
                                            (pixel_map[pixel[0],pixel[1]+1])+
                                            (pixel_map[pixel[0]+2,pixel[1]+1]/root_5))/((4/root_5)+2)
            
            pixel_map(pixel[0],pixel[1]) = resulting_pixel

        if pixel[1] == height-2:
            k = 0.1 #[0.1,0.2,0.3...1]
            mat1 = np.array([4**2,4,1])
            mat2 = np.array([1/8,-1/4,1/8],
                            [-1,3/2,-1/2],
                            [15/8,-5/4,3/8])
            mat3 = np.array([pixel_map[pixel[0],pixel[1]-3]],
                            [pixel_map[pixel[0],pixel[1]-1]],
                            [pixel_map[pixel[0],pixel[1]+1]])
            f1 = np.matmul(np.matmul(mat1,mat2),mat3)

            mat1 = np.array([2**2,2,1])
            mat2 = np.array([1/6,-1/2,1/3],
                            [-7/6,5/2,-4/3],
                            [2,-2,1 ])
            mat3 = np.array([pixel_map[pixel[0],pixel[1]-1]],
                            [pixel_map[pixel[0],pixel[1]+1]],
                            [pixel_map[pixel[0],pixel[1]+2]])
            f2 = np.matmul(np.matmul(mat1,mat2),mat3)   

            resulting_pixel = k*((f1+f2)/2)+(1-k)*((pixel_map[pixel[0]-2,pixel[1]-1]/root_5)+
                                            (pixel_map[pixel[0],pixel[1]-1])+
                                            (pixel_map[pixel[0]+2,pixel[1]-1]/root_5)+
                                            (pixel_map[pixel[0]-2,pixel[1]+1]/root_5)+
                                            (pixel_map[pixel[0],pixel[1]+1])+
                                            (pixel_map[pixel[0]+2,pixel[1]+1]/root_5))/((4/root_5)+2)
            
        if pixel[0] == width-1:
            k = 0.1 #[0.1,0.2,0.3...1]
            mat1 = np.array([4**2,4,1])
            mat2 = np.array([1/8,-1/4,1/8],
                            [-1,3/2,-1/2],
                            [15/8,-5/4,3/8])
            mat3 = np.array([pixel_map[pixel[0],pixel[1]-3]],
                            [pixel_map[pixel[0],pixel[1]-1]],
                            [pixel_map[pixel[0],pixel[1]+1]])
            f1 = np.matmul(np.matmul(mat1,mat2),mat3)

            mat1 = np.array([2**2,2,1])
            mat2 = np.array([1/8,-1/4,1/8],
                            [-1,3/2,-1/2],
                            [15/8,-5/4,3/8])
            mat3 = np.array([pixel_map[pixel[0],pixel[1]-1]],
                            [pixel_map[pixel[0],pixel[1]+1]],
                            [pixel_map[pixel[0],pixel[1]+2]])
            f2 = np.matmul(np.matmul(mat1,mat2),mat3)   

            resulting_pixel = k*((f1+f2)/2)+(1-k)*((pixel_map[pixel[0]-2,pixel[1]-1]/root_5)+
                                            (pixel_map[pixel[0],pixel[1]-1])+
                                            (pixel_map[pixel[0]+1,pixel[1]-1]/root_2)+
                                            (pixel_map[pixel[0]+1,pixel[1]])+
                                            (pixel_map[pixel[0]-2,pixel[1]+1]/root_5)+
                                            (pixel_map[pixel[0],pixel[1]+1])+
                                            (pixel_map[pixel[0]+1,pixel[1]+1]/root_2))/((2/root_5)+(2/root_2)+3)

        else:
            k = 0.1 #[0.1,0.2,0.3...1]
            mat1 = np.array([4**2,4,1])
            mat2 = np.array([1/8,-1/4,1/8],
                            [-1,3/2,-1/2],
                            [15/8,-5/4,3/8])
            mat3 = np.array([pixel_map[pixel[0],pixel[1]-3]],
                            [pixel_map[pixel[0],pixel[1]-1]],
                            [pixel_map[pixel[0],pixel[1]+1]])
            f1 = np.matmul(np.matmul(mat1,mat2),mat3)

            mat1 = np.array([2**2,2,1])
            mat2 = np.array([1/8,-1/4,1/8],
                            [-1,3/2,-1/2],
                            [15/8,-5/4,3/8])
            mat3 = np.array([pixel_map[pixel[0],pixel[1]-1]],
                            [pixel_map[pixel[0],pixel[1]+1]],
                            [pixel_map[pixel[0],pixel[1]+2]])
            f2 = np.matmul(np.matmul(mat1,mat2),mat3)   
                
            resulting_pixel = k*((f1+f2)/2)+(1-k)*((pixel_map[pixel[0]-2,pixel[1]-1]/root_5)+
                                            (pixel_map[pixel[0],pixel[1]-1])+
                                            (pixel_map[pixel[0]+2,pixel[1]-1]/root_5)+
                                            (pixel_map[pixel[0]-2,pixel[1]+1]/root_5)+
                                            (pixel_map[pixel[0],pixel[1]+1])+
                                            (pixel_map[pixel[0]+2,pixel[1]+1]/root_5))/((4/root_5)+2)

        pixel_map[pixel[0],pixel[1]] = resulting_pixel
            

    

    

    

    