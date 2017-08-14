%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
%% This file is part of SceneUnderstanding@CIARP. 
% 
% SceneUnderstanding@CIARP is free software: you can redistribute it and/or modify 
% it under the terms of the GNU General Public License as published by 
% the Free Software Foundation, either version 3 of the License, or 
% (at your option) any later version. 
% 
% SceneUnderstanding@CIARP is distributed in the hope that it will be useful, 
% but WITHOUT ANY WARRANTY; without even the implied warranty of 
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
% GNU General Public License for more details. 
% 
% You should have received a copy of the GNU General Public License 
% along with SceneUnderstanding@CIARP. If not, see <http://www.gnu.org/licenses/>. 
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import numpy as np
import caffe, sys, os, spams, csv, time
import cv2
import getopt
import ConfigParser
#from scipy import misc
import skimage

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))



from cnnmodel import CNN
import iocsv
import pooling
import minimization
import splitfeats

def getClasses(mat):

	classes = set()

	for i in mat:

		classe = i.split('/')[0]

		classes.add(classe)


	return sorted(list(classes))
	


def readSamples(path_file):

	samples_file = open(path_file,'r')
	
	sample = []

	for i in samples_file:

		sample.append(i)


	return sorted(sample)


def read_caffe_img(path):
	return skimage.img_as_float(skimage.io.imread(path)).astype(np.float32).copy()


def ConfigSectionMap(section,Config):
   
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


# -----------MAIN-------------#
if __name__ == "__main__":

	
	with_pca = False
	scale_number = '0'	
	fold = '0'
	folder_output = 'folder'
	
	try:
      		opts, args = getopt.getopt(sys.argv[1:],'c:i:s:o:r:',['cfg=','input=','scale=','output=','resize='])
   	
	except getopt.GetoptError:
     		 print 'Need configuration file to execute.'
     		 sys.exit(2)
	
	for opt, arg in opts:

		

		if opt in ('-c','--cfg'):

			cfg_file = arg
			print cfg_file

		if opt in ('-s','--scale'):

			scale_number = arg
			print scale_number


		if opt in ('-o','--output'):

			folder_output = arg
			print folder_output


		if opt in ('-i','--input'):

			samples_input = arg
			print samples_input

		if opt in ('-r','--resize'):

			resize_input = int(arg)



		


	Config = ConfigParser.ConfigParser()
	Config.read(cfg_file)

	
	features_dataset = ConfigSectionMap('img_dataset',Config)['path']
	cell_space = int(ConfigSectionMap('img_set',Config)['size'+scale_number])
	model_path = ConfigSectionMap("cnn_model",Config)['caffemodel']
	model_text = ConfigSectionMap("cnn_model",Config)['deploy']
	mean_path = ConfigSectionMap("cnn_model",Config)['mean']
	stride = int(ConfigSectionMap('img_set',Config)['stride'+scale_number])
	cropsize = int(ConfigSectionMap("cnn_model",Config)['crop'])
	layer = ConfigSectionMap("cnn_model",Config)['layer']

	#dictionary = iocsv.readCSV(dictionary_path)
	#print "Dictionary: ",dictionary.shape
	labels = []
	all_coeffs = []
	label_count = 0

	mean = np.load(mean_path)
	print mean

	print mean.shape
	#mean = np.array([103.939, 116.779, 123.68])
	cnnmodel = CNN(model_path,model_text,mean,cropsize,layer)
	folder_name = folder_output
	os.system("mkdir "+folder_name)


	samples = readSamples(samples_input)

	for i in sorted(os.listdir(features_dataset)):
		print i		
		os.system("mkdir "+folder_name+"/"+i)

		new_env_class = folder_name+"/"+i
		env_class = features_dataset+"/"+i
		#all_feats = []
	
		for j in samples:
			if i == j.split('/')[0]:
			

				s = j.split('/')[1].replace('\n','')
				bn = j.split('/')[1].split('.')[0]
				
#				print bn

				
				if os.path.isfile(new_env_class+"/"+bn+"_feat.npz"): #If exists, does not create again		
					continue


				env_sample = env_class+"/"+s

				if not os.path.isfile(env_sample): #If image does not exist, continue
					continue

				#img = misc.imread(env_sample)
				img = read_caffe_img(env_sample)
				#print "Lido",env_sample	
				
				if img.any() == None:
					continue

				#print "Lido",env_sample	
				#cv2.imshow('img',img)
				#cv2.waitKey()
				
				if len(img.shape) < 3:

					img = cv2.merge([img,img,img])
					#cv2.imshow('img',img)
					#cv2.waitKey()

				#imgb,imgg,imgr = cv2.split(img)
				#img = cv2.merge([imgr,imgg,imgb])
		
				print "Extracting from: ",env_sample,img.shape

				#img = caffe.io.load_image(env_sample)
						
				feat = splitfeats.splitScene(img,img.shape[1]/cell_space,img.shape[0]/cell_space, img.shape[1]/(cell_space*stride),img.shape[0]/(cell_space*stride),cnnmodel,(resize_input,resize_input))
				print np.array(feat)				
				iocsv.writeNPY(np.asarray(feat),new_env_class+"/"+bn+"_feat")
				
			






