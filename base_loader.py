import os
import cv2
import numpy as np
from median import median_filter

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

	def equalization(self):
		equalized_images = []
		for image in self.images:
			height , width = image.shape
			equalized_image = np.zeros((height , width) , np.uint8)
			equalized_image = cv2.equalizeHist(image)
			equalized_images.append(equalized_image)
		return equalized_images


base = BaseLoader('DB1_2000')
#print(base.image_paths)
enhanced_images = base.enhancement()
#for image in enhanced_images[1]:
#	cv2.imshow('image' , image)
#	cv2.waitKey(0)
#equalized_images = base.equalization()
#for image in equalized_images:
#	cv2.imshow('image' , image)
#	cv2.waitKey(100)

cv2.imshow('original' , base.images[0])
cv2.imshow('enhanced' ,  enhanced_images[0])
cv2.imshow('median' , median_filter(enhanced_images[0] , 5))
cv2.waitKey(0)