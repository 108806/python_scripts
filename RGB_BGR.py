import os
from PIL import Image

def convert_rgb_to_grb(image_path):
    # Open the image
    image = Image.open(image_path)
    assert '.' in image_path
    
    # Generate the output path
    dirpath = os.sep.join(image_path.split(os.sep)[:-1])
    filename = image_path.split(os.sep)[-1].split('.')[0]
    newfile = filename+'_BGR'+'.'+image_path.split('.')[-1]
    converted_image_path = dirpath+os.sep+newfile
    print(converted_image_path)
    
    # Convert the image to RGB mode if it's not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert each pixel from RGB to GRB
    pixels = image.load()
    width, height = image.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            pixels[x, y] = b, g, r
    
    # Save the converted image
    image.save(converted_image_path)
    
    print("Conversion complete. Saved as", converted_image_path)

# Example usage
if __name__ == '__main__':
	image_path = input('path/to/your/image.jpg\n')
	convert_rgb_to_grb(image_path)
