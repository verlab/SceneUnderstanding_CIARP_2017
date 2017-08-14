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
import sys, os, random, spams
import cv2, json
import getopt
import ConfigParser
from scipy import misc
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from sklearn.decomposition import MiniBatchDictionaryLearning
#from cnnmodel import CNN
import iocsv
#import splitfeats
import time
import pickle

def ConfigSectionClasses(section,Config):


	options = Config.options(section)
	mat_classes = []

	dict1 = {}

	for i in sorted(options):

		dict1[i] = Config.get(section,i).split(' ')


	return dict1

	
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


###--------MAIN---------###	
if __name__ == "__main__":

	#Default Settings

	num_clusters = 30 
	with_pca = False
	scale_number = '0'	
	fold = '0'
	dictionary_output = 'dictionary'+fold+'.csv'
	with_dl = False
	cnn = 'IMNET'
	
	try:
      		opts, args = getopt.getopt(sys.argv[1:],'c:p:s:o:f:n:r:l:v',['cfg=','pca=','scale=','output=','fold=','nclusters=','resize=','dl=', 'cnn='])
   	
	except getopt.GetoptError:
     		 print 'Need configuration file to execute.'
     		 sys.exit(2)
	
	for opt, arg in opts:

		if opt in ('-p','--pca'):
			
			print arg        	
			with_pca = True
			pca_file = open(arg)
			pca = pickle.load(pca_file)
			pca_file.close()
			#json_pca = arg	
			#pca = json.loads(open(json_pca).read())
			#eigen_pca = np.array(pca["eigen-vectors"])
			#mean_pca = np.array(pca["mean"])
	

		if opt in ('-c','--cfg'):

			cfg_file = arg
			print cfg_file

		if opt in ('-s','--scale'):

			scale_number = arg
			print scale_number


		if opt in ('-o','--output'):

			dictionary_output = arg
			print dictionary_output

		if opt in ('-f','--fold'):

			fold = arg
			print fold

		if opt in ('-n','--nclusters'):

			num_clusters = int(arg)
			print fold

		if opt in ('-r','--resize'):

			resize_input = int(arg)

		if opt in ('-l','--dl'):

			with_dl = True
			dlambda = float(arg)




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
	test_data_set = ConfigSectionMap('folds',Config)['path'+fold]

	feat_rootpath = ConfigSectionMap('features',Config)['scale'+scale_number]
	#dictionary = iocsv.readCSV(dictionary_path)
	#print "Dictionary: ",dictionary.shape
	labels = []
	all_coeffs = []
	label_count = 0

	mean = np.load(mean_path)
	print mean


	#mean = np.array([103.939, 116.779, 123.68])
	#cnnmodel = CNN(model_path,model_text,mean,cropsize,layer)

	all_feats = []
	labels = []
	label_count=0


	ConfigDict = ConfigParser.ConfigParser()
	ConfigDict.optionxform = str
	ConfigDict.read(test_data_set)

	dict_samples = ConfigSectionClasses('train_dict',ConfigDict)

	
	#mean_model = np.load(mean_path).mean(1).mean(1)
	#cnnmodel = CNN(model_path,model_text,mean_model,cropsize,layer)

	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)
	flags = cv2.KMEANS_PP_CENTERS

	centers = []
	centers2 = []

	print "Number of clusters:", num_clusters, test_data_set
	
	for i in sorted(dict_samples.keys()):

		env_class = i
		#all_feats = []
	
		for j in dict_samples[env_class]:
	
			env_sample = features_dataset+'/'+i+'/'+j

	
		#	if not os.path.isfile(env_sample+'.jpg'):
		#		print "Cannot find ",env_sample+'.jpg'
		#		continue
			
		#	img = misc.imread(env_sample+'.jpg')

				#print "Lido",env_sample	
				
		#	if img == None:
		#		continue

			#print "Lido",env_sample	
			#cv2.imshow('img',img)
			#cv2.waitKey()
				
		#	if len(img.shape) < 3:

		#		img = cv2.merge([img,img,img])
		

			print "Reading: ", env_sample+'.jpg'

		#	img = cv2.flip(img,1)

			#cv2.imshow('img',img)
			#cv2.waitKey()			

			#### APAGAR ####
			#feat_path = '/home/camilalaranjeira/projects/tests_sc/places365_guilherme/' + cnn + '_feats/' + cnn + '_' + str(resize_input) + '/'
			
			feat_path = feat_rootpath + '/' + i + '/' + j + '_feat.npz'
			if not os.path.isfile(feat_path):
				print "Cannot find ", feat_path
				continue
			feat = iocsv.readNPY(feat_path)
		#	print feat_path
	#		print feat.shape

			#### APAGAR ####

			#feat = splitfeats.splitScene(img,img.shape[1]/cell_space,img.shape[0]/cell_space, img.shape[1]/(cell_space*stride),img.shape[0]/(cell_space*stride),cnnmodel,(resize_input,resize_input))

			if with_pca:

				#feat = cv2.PCAProject(np.array(feat),mean_pca,eigen_pca)
				feat = pca.transform(feat)
				
				if cv2.norm(feat, cv2.NORM_L2) > 0:
                			feat = feat / cv2.norm(feat, cv2.NORM_L2)
			

			all_feats.append(feat)

		
		label_count = label_count + 1



	all_feats = np.concatenate(all_feats, axis=0)
	all_feats = np.array(all_feats)
	all_feats = np.float32(all_feats)
	all_feats = np.ascontiguousarray(all_feats)
	print all_feats.shape
	
	print "Clustering ",all_feats.shape," features..."	
	outkmeans = cv2.kmeans(data=all_feats, K=num_clusters,bestLabels = None, criteria = criteria,attempts = 10,flags = flags)
	print "Done!"	
	class_dict = outkmeans[2]
	print outkmeans[2].shape
	print outkmeans[2]

	iocsv.writeNPY(np.asarray(class_dict), dictionary_output)
	exit()

	#class_dict = iocsv.readNPY(dictionary_output + '.bkp.npz')
	
	with_dl = True
	if with_dl == True:

#		class_dict = spams.trainDL(X = all_feats.transpose(),D=class_dict.transpose(),iter=20,lambda1=dlambda,posD=True).transpose()
#		class_dict = spams.trainDL(X = all_feats.transpose(), K = num_clusters, iter=20,lambda1=dlambda,posD=True).transpose()
		#class_dict = spams.trainDL(X = all_feats.transpose(),D=class_dict.transpose(),iter=100,lambda1=dlambda,mode=3,batchsize=1024).transpose()
#		class_dict = spams.trainDL_Memory(X = all_feats.transpose(),D=class_dict.transpose(),iter=100,lambda1=dlambda,mode=3,batchsize=1024).transpose()
		dict_learning = MiniBatchDictionaryLearning(n_components=num_clusters, alpha=dlambda, n_iter=100)
		class_dict = dict_learning.fit(class_dict)
	centers2.append(class_dict)
	
	print np.asarray(centers2).shape
	print np.asarray(centers2)

	centers3 = np.concatenate(centers2, axis=0)
	print "Centers3\n"
	print np.asarray(centers3).shape
	print np.asarray(centers3)
	
	print 'Writing Dictionary...'	
	#iocsv.writeNPY(np.asarray(class_dict),dictionary_output)
	#iocsv.writeNPY(np.asarray(class_dict),dictionary_output + '_cat')	
	print 'Done'
	


