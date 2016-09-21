import os
import cv2
import numpy as np

class BaseLoader(object):

	def __init__(self , base_path):
		self.base_path = base_path
		self.images = []
		self.image_paths = []
		self.load_images()

	def load_images(self):
		print("loading base ...")
		self.image_paths = os.listdir(self.base_path)
		self.image_paths.sort()
		for image_path in self.image_paths:
			image = cv2.imread(self.base_path + "/" + image_path , 0)
			self.images.append(image)
		print("load complete")

	def enhancement(self , alpha = 150 , y = 95):
		print("enhancement started ...")
		enhanced_images = []
		for image in self.images:
			mean = np.mean(image)                 #compute mean value
			variance = np.var(image)              #compute the variance 
			standard_deviation = np.std(image)    #computing standard deviation
			height , width = image.shape                           
			enhanced_image = np.zeros((height , width) , np.uint8)  #create empty image ,this matrix will reciave the enhanced values calculated
			for x_axis in xrange(0 , height):
				for y_axis in xrange(0 , width):
					new_value = alpha + y * (int(image.item((x_axis , y_axis)) - mean) / standard_deviation) #works better with standard deviation than variance
					if new_value < 0:             #verifing if new value is between 0 and 255 (minimum and maximun values possible))
						new_value = 0
					elif new_value > 255:
						new_value = 255
					enhanced_image.itemset((x_axis , y_axis) , new_value) #setting enhanced value 
			enhanced_images.append(enhanced_image)
		print("enhancement completed")
		return enhanced_images

	def equalize(self):
		equalized_images = []
		for image in self.images:
			height , width = image.shape
			equalized_image = np.zeros((height , width) , np.uint8)
			equalized_image = cv2.equalizeHist(image)
			equalized_images.append(equalized_image)
		return equalized_images

	def devide_into_blocks(self , image , block_size):
		blocks = []
		image_height ,image_width = image.shape[:2]
		for x_axis in xrange(0,image_height , block_size):
			for y_axis in xrange(0,image_width , block_size):
				seed = tuple([x_axis , y_axis])
				block = []
				for i in xrange(seed[0],seed[0] + block_size):
					for j in xrange(seed[1],seed[1] + block_size):
						if i >= image_height:
							i = image_height - 1
						if j >= image_width:
							j = image_width - 1
						#print("i : " + str(i) + " | j : " + str(j))
						block.append(image.item(i,j))
				blocks.append(block)
		#print(len(blocks))
		return blocks

	def orientation(self , image , median_kernel_size , sobel_kernel_size):
		median_image = cv2.medianBlur(image , median_kernel_size)
		gx = cv2.Sobel(image,cv2.CV_64F,1,0,ksize=sobel_kernel_size)
		gy = cv2.Sobel(image,cv2.CV_64F,0,1,ksize=sobel_kernel_size)
		gx_blocks = self.devide_into_blocks(gx , 11)
		gy_blocks = self.devide_into_blocks(gy , 11)
		x_orientations = []
		y_orientetions = []
		for   block_index in range(0 , len(gx_blocks)):
			gx_block = np.array(gx_blocks[block_index] , np.uint8)
			gy_block = np.array(gy_blocks[block_index] , np.uint8)
			a_x = int(np.sum(abs((gx_block * gx_block) - (gy_block * gy_block))) / (11 * 11))
			a_y = int(np.sum(abs(2 * gx_block * gy_block)) / (11 * 11))
			x_orientations.append(a_x)
			y_orientetions.append(a_y)
		print(x_orientations)
		print(y_orientetions)

		

base = BaseLoader('test')
enhanced_images = base.enhancement()
base.orientation(enhanced_images[0] ,5 ,  3)













"""image = base.images[0]
k_height = k_width = 11
blocks = []
image_height ,image_width = image.shape[:2]
print(image_height)
print(image_width)
for x_axis in xrange(0,image_height , k_height):
	for y_axis in xrange(0,image_width , k_width):
		seed = tuple([x_axis , y_axis])
		block = []
		#print(seed)
		for i in xrange(seed[0],seed[0] + k_height):
			for j in xrange(seed[1],seed[1] + k_width):
				if i >= image_height:
					i = image_height - 1
				if j >= image_width:
					j = image_width - 1
				print("i : " + str(i) + " | j : " + str(j))
				block.append(image.item(i,j))
		#print(block)
		blocks.append(block)
print(len(blocks))"""

#for block in blocks:
#	print(len(block))




























#for image in enhanced_images[1]:
#	cv2.imshow('image' , image)
#	cv2.waitKey(0)
#equalized_images = base.equalization()
#for image in equalized_images:
#	cv2.imshow('image' , image)
#	cv2.waitKey(100)

#cv2.imshow('original' , base.images[0])
#cv2.imshow('enhanced' ,  enhanced_images[0])
#cv2.imshow('median' , base.orientation(enhanced_images[0] , 5))
"""gx , gy = base.orientation(enhanced_images[0] , 5)
cv2.imshow('gx' , gx)
cv2.imshow('gy' , gy)
cv2.waitKey(0)"""