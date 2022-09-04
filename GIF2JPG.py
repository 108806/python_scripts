from PIL import Image
import os, sys


print(sys.argv)
filename = str()
if len(sys.argv) != 2: 
    print('Usage: python convert.py filename.gif')
else: 
    filename = str(sys.argv[1]).strip()
if len(sys.argv) == 1:
    print('''running test cases with arg of test.gif''')
    filename = 'test.gif'


print(os.getcwd(), filename)


def gif2jpg(file_name: str, num_key_frames: int, trans_color: tuple):
    """
    convert gif to `num_key_frames` images with jpg format
    :param file_name: gif file name
    :param num_key_frames: result images number
    :param trans_color: set converted transparent color in jpg image
    :return:
    """
    with Image.open(file_name) as im:
        prevData = []
        for i in range(num_key_frames):
            im.seek(im.n_frames // num_key_frames * i)
            image = im.convert("RGBA")
            datas = image.getdata()
            newData = []
            for item in datas:
                if item[3] == 0:  # if transparent
                    newData.append(trans_color)  # set transparent color in jpg
                else:
                    newData.append(tuple(item[:3]))
            
            if prevData != newData:
                image = Image.new("RGB", im.size)
                image.getdata()
                image.putdata(newData)
                image.save(filename+'_{}.jpg'.format(i))
                prevData = newData
            else: print("[*] skipping identical frame")


if __name__ == '__main__':
    gif2jpg(filename, 8, (255, 255, 255))  # convert image.gif to 8 jpg images with white background
