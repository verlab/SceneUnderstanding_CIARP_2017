####################################################################################### 
## This file is part of SceneUnderstanding@CIARP. 
# 
# SceneUnderstanding@CIARP is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version. 
# 
# SceneUnderstanding@CIARP is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details. 
# 
# You should have received a copy of the GNU General Public License 
# along with SceneUnderstanding@CIARP. If not, see <http://www.gnu.org/licenses/>. 
# 
#######################################################################################

import numpy as np
import sys, os, spams, csv, time
import cnnmodel
import cv2


def extractFeatROI(img,i,j,cell_size_x,cell_size_y,CNN,img_resize=(227,227)):

	
	img_roi = img[i:i+cell_size_y,j:j+cell_size_x]
	
	#print img_roi.shape[0], cell_size_y, img_roi.shape[1], cell_size_x
	
	if img_roi.shape[0] < cell_size_y or img_roi.shape[1] < cell_size_x:
		
		return None
	
	img_roi = cv2.resize(img_roi,img_resize)

	#cv2.imshow("test",img_roi)
	#cv2.waitKey()
	
	CNN.setImage(img_roi)
	feat_roi = CNN.extractFeatures()

	return feat_roi	


def splitScene(scene, cell_size_x, cell_size_y, WINSTEP_X, WINSTEP_Y,CNN,img_resize=(227,227)): #img,(cell size x, cell size y) stride X, stride Y


	all_descs = [ ]

	for i in range(0,scene.shape[0],WINSTEP_Y):
	
		
		for j in range(0,scene.shape[1],WINSTEP_X):
				
			feat_roi = extractFeatROI(scene,i,j,cell_size_x, cell_size_y,CNN,img_resize) # rever isso
		        if feat_roi == None:
		        	continue
		        
		        all_descs.append(feat_roi)
		
	#all_descs = np.concatenate(all_descs, axis=0)
	
	print np.asarray(all_descs).shape
		
	return np.asarray(all_descs)

def extractFeatROI_(img,i,j,cell_size_x,cell_size_y,CNN):

	
	img_roi = img[i:i+cell_size_y,j:j+cell_size_x]
	
	#print img_roi.shape[0], cell_size_y, img_roi.shape[1], cell_size_x
	
	if img_roi.shape[0] < cell_size_y or img_roi.shape[1] < cell_size_x:
		
		return None
	
	
	#cv2.imshow("test",img_roi)
	#cv2.waitKey()
	
	CNN.setImage(img_roi)
	feat_roi = CNN.extractFeatures()

	return feat_roi	


def splitScene_(scene, cell_size_x, cell_size_y, WINSTEP_X, WINSTEP_Y,CNN): #img,(cell size x, cell size y) stride X, stride Y


	all_descs = [ ]

	for i in range(0,scene.shape[0],WINSTEP_Y):
	
		
		for j in range(0,scene.shape[1],WINSTEP_X):
				
			feat_roi = extractFeatROI(scene,i,j,cell_size_x, cell_size_y,CNN) # rever isso
		        if feat_roi == None:
		        	continue
		        
		        all_descs.append(feat_roi)
		
	#all_descs = np.concatenate(all_descs, axis=0)
	
	print np.asarray(all_descs).shape
		
	return np.asarray(all_descs)
