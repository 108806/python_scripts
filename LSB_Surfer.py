import chardet
import numpy as np
import ctypes, struct, os, sys, cv2
from functools import lru_cache


@lru_cache(maxsize=None, typed=True)
def collect_lsb(FILENAME:str, CHR_SIZE:int=8, STOP_THRESHOLD:int=16):
	'''
	Collects all the least significant bytes from the img.
	FILENAME : file name string, image.png
	CHR_SIZE : byte size of characters, 8 for utf8
	STOP_THRESHOLD : stopping when n empty blocks are being continously found
	'''
	#TODO: Optimize performance, use chardet at the end

	img = cv2.imread(FILENAME)
	shp = img.shape
	print(shp)
	
	LSB_ARR = np.zeros((shp[0]*shp[1]*shp[2],CHR_SIZE),dtype=np.uint8)
	#p_arr_t = LSB_ARR.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
	print(LSB_ARR.shape)
	CHR_ARR = np.zeros((LSB_ARR.shape[0] // CHR_SIZE, 1), dtype=np.uint32)
	index, elem = np.uint8(0),np.uint8(0)
	THRESHOLD = 0

	def dec0de(ARR:np.array, CHR_SIZE=CHR_SIZE):
		#binStr = ''.join([str(x) for x in ARR]).strip()
		binStr = ARR
		return binStr

	for col in range(0, shp[0]-1):
		for row in range(0, shp[1]-1):
			for pixel in range(0, shp[2]-1):
				# get last byte from the pixels:
				LSB = bin(img[col][row][pixel])[-1:]

				LSB_ARR[elem][index] = LSB

				index += 1
				if index // CHR_SIZE:
					
					if STOP_THRESHOLD and not any(LSB_ARR[elem]):
						THRESHOLD+=1
						if THRESHOLD==STOP_THRESHOLD:
							print('Empty blocks tresh found, stopping.')
							return CHR_ARR, LSB_ARR	

					bin_char = ''.join(str(LSB_ARR[elem])).replace(' ', '')[1:-1]
					print(bin_char, sep='', end='')
					CHR_ARR[elem] = bin_char
	
					index = 0
					elem += 1

	return [x for x in CHR_ARR], LSB_ARR




if __name__=='__main__':
		result, LSB_ARR = collect_lsb(FILENAME='encoded_image.png', CHR_SIZE=8, STOP_THRESHOLD=4)
		print(len(result))

		FIN = np.array([int('0b'+np.array2string(x)[1:-1], 2) for x in result])
		WRD = np.array(''.join([chr(C) for C in FIN]))
		print(WRD)
		
		# guess = chardet.detect(FIN.tobytes())
		# print(guess)


 
