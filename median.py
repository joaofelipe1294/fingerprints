import numpy as np
import cv2

def median_filter(image , kernel_size):
	kernel_height = kernel_size
	kernel_width = kernel_size
	kernel_ray = int(kernel_size / 2)
	image_height , image_width = image.shape
	median_image = np.zeros((image_height, image_width) , np.uint8)
	for x_axis in xrange(0,image_height):
		for y_axis in xrange(0,image_width):
			if x_axis == 0:
				if y_axis == 0:
					x_min = x_axis
					x_max = x_axis + kernel_ray + 1
					y_min = y_axis
					y_max = y_axis + kernel_ray + 1	
					
				elif y_axis == image_width - 1:
					x_min = x_axis
					x_max = x_axis + kernel_ray + 1
					y_min = y_axis - kernel_ray
					y_max = image_width

				else:
					x_min = x_axis
					x_max = x_axis + kernel_ray + 1
					if y_axis - kernel_ray < 0:
						y_min = 0
					else:
						y_min = y_axis - kernel_ray
					if y_max + kernel_ray + 1 > image_width:
						y_max = image_width - 1
					else:
						y_max = y_axis + kernel_ray + 1
					
			elif x_axis == image_height - 1:

				if y_axis == 0:
					x_min = x_axis - kernel_ray - 1
					x_max = x_axis
					y_min = y_axis
					y_max = y_axis + kernel_ray + 1	
					
				elif y_axis == image_width - 1:
					x_min = x_axis - kernel_ray
					if x_max + kernel_ray > image_height:
						x_max = image_height
					else:
						x_max = x_axis + kernel_ray
					y_min = y_axis - kernel_ray
					y_max = image_width

				else:
					x_min = x_axis - kernel_ray
					if x_axis + kernel_ray > image_height:
						x_max = image_height
					else:
						x_max = x_axis + kernel_ray
					y_min = y_axis - kernel_ray
					if y_axis + kernel_ray + 1 > image_width:
						y_max = image_width
					else:
						y_max = y_axis + kernel_ray + 1
			elif y_axis == 0 and x_axis > 0:
				x_min = x_axis - kernel_ray
				if x_axis + kernel_ray + 1 > image_height:
					x_max = image_height
				else:
					x_max = x_axis + kernel_ray + 1
				y_min = y_axis
				y_max = y_axis + kernel_ray + 1
			elif y_axis == image_width - 1 and x_axis > 0:
				x_min = x_axis - kernel_ray
				if x_max + kernel_ray + 1 > image_height:
					x_max = image_height
				else:
					x_max = x_axis + kernel_ray + 1
				y_min = y_axis - kernel_ray
				if y_axis + kernel_ray > image_width:
					y_max = image_width
				else:
					y_max = y_axis + kernel_ray
			else:
				if x_axis - kernel_ray < 0:
					x_min = 0
				else:
					x_min = x_axis - kernel_ray
				if x_axis + kernel_ray + 1 > image_height:
					x_max = image_height
				else:
					x_max = x_axis + kernel_ray + 1
				if y_axis - kernel_ray < 0:
					y_min = 0
				else:
					y_min = y_axis - kernel_ray
				if y_axis + kernel_ray + 1 > image_width:
					y_max = image_width
				else:
					y_max = y_axis + kernel_ray + 1
				#print(" X_min : " + str(x_min) + " X_max : " + str(x_max) + " Y_min : " + str(y_min) +  " Y_max : " + str(y_max))
			values = []
			for x in xrange(x_min, x_max):
				for y in xrange(y_min, y_max):
					values.append(image.item(x,y))

			values.sort()
			mean_index = int(len(values) / 2)
			#print(values[mean_index])
			median_image.itemset((x_axis , y_axis) , values[mean_index])
	return median_image

#image = np.array(([ 3, 1, 2, 5, 9, 12] ,
#				   [ 3, 8, 0, 0, 3, 5],
#				   [ 0, 8, 8, 2, 8, 9] ,
#				   [ 0, 6, 7, 3, 4, 8] ,
#				   [ 0, 3, 5, 4, 9, 3] ,
#				   [ 2, 2, 1, 2, 1, 0]
#						) , np.uint8)

#image = cv2.imread("DB1_2000/101_1.tif" , 0)
#print(image)
#median_image = median_filter(image , 5)
#cv2.imshow('original' , image)
#cv2.imshow('mean' , median_image)
#cv2.waitKey(0)
#print(median_image)