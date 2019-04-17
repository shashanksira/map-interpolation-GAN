from PIL import Image
import os
import sys 
import csv
import pandas as pd

#if there are more water pixels than im_size / threshold, don't consider that image for training
#threshold = 2

#add col's to CSV for different thresholds, whether to include that image at a certain threshold
image_details_df = pd.read_csv("ImageDetails.csv")
#create new columns for image path, then the threshold values (1 or 0)
# to make new col, append all the values to a list, then just do
#	image_details_df['New col name'] = list
#image_details_df['thresh_50'] = threshold_50

dir_path = os.path.dirname(os.path.realpath(__file__))
#WATER COLOR OF MAPS  ~= R:170 G:218 B:255
#	find maps that have lots of their pixels near this value 
ims_disqualified_25 = 0
ims_disqualified_35 = 0
ims_disqualified_50 = 0
threshold_25 = []		#threshold = 4
threshold_35 = []		#threshold = 2.9
threshold_50 = []		#threshold = 2
file_paths = []
#for filename in os.listdir(dir_path + '/maps/'):
for im_name in image_details_df['Image Name']:
	im_name = im_name.split('_')
	#names in CSV file are off by one. IE they start at image_number_0, when the actual
	#	images start at 1. Need to increment the last value for each file name 
	im_name[len(im_name) - 1] = int(im_name[len(im_name) - 1]) + 1
	#insert 'roadmap' to the file name
	im_name.insert(3, 'roadmap')
	im_name.remove('number')
	im_name = '_'.join(str(e) for e in im_name)

	file_paths.append(dir_path + '/roadmap-images/' + im_name + '.png')

	im = Image.open(dir_path + '/roadmap-images/' + im_name + '.png').convert('RGB')
	h = im.histogram()
	r_h = h[0:256]
	g_h = h[256:512]
	b_h = h[512:768]
	#50% of image is water
	if (sum(r_h[168:172]) + sum(g_h[216:220]) + sum(b_h[250:255]) > ((im.size[0] * im.size[1]) / 2)):
		threshold_25.append(0)
		threshold_35.append(0)
		threshold_50.append(0)
		ims_disqualified_50 += 1
		continue
	else:
		threshold_50.append(1)
	#75% of image is water
	if (sum(r_h[168:172]) + sum(g_h[216:220]) + sum(b_h[250:255]) > ((im.size[0] * im.size[1]) / 2.9)):
		threshold_25.append(0)
		threshold_35.append(0)
		ims_disqualified_35 += 1
		continue
	else:
		threshold_35.append(1)
	#83% of the image is water 
	if (sum(r_h[168:172]) + sum(g_h[216:220]) + sum(b_h[250:255]) > ((im.size[0] * im.size[1]) / 4)):
		threshold_25.append(0)
		ims_disqualified_25 += 1
		continue
	else:
		threshold_25.append(1)

print('Data frame length: ' + str(len(image_details_df)))
print('Threshold Lengths:  ')
print('25 : ' + str(len(threshold_25)))
print('35 : ' + str(len(threshold_35)))
print('50 : ' + str(len(threshold_50)))
print('File paths length: ' + str(len(file_paths)))
print('Number of files that failed the 25% threshold: ' + str(ims_disqualified_25))
print('Number of files that failed the 35% threshold: ' + str(ims_disqualified_35))
print('Number of files that failed the 50% threshold: ' + str(ims_disqualified_50))

image_details_df['File Path'] = file_paths
image_details_df['Threshold 25%'] = threshold_25
image_details_df['Threshold 35%'] = threshold_35
image_details_df['Threshold 50%'] = threshold_50

image_details_df.to_csv('Image_Details.csv')
