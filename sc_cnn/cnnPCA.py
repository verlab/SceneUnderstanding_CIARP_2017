import numpy as np
import caffe, sys, os, random
import cv2,json

import getopt
import ConfigParser
sys.path.append('/homeLocal/guilherme/sc_cnn/src')

from cnnmodel import CNN
import iocsv
import splitfeats


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


def savejson(mean,eigen,outputname):

	data = {"mean": mean.tolist(), "eigen-vectors": eigen.tolist()}
	with open(outputname, "w") as f:
    		json.dump(data, f)



###--------MAIN---------###	

if __name__ == "__main__":

	#Default parameters
	
	scale_number = '0'	
	fold = '0'
	pca_output = 'pca'+fold+'.json'
	components = 1000


	try:
      		opts, args = getopt.getopt(sys.argv[1:],'c:d:s:o:f:',['cfg=','comp=','scale=','output=','fold='])
   	
	except getopt.GetoptError:
     		 print 'Need configuration file to execute.'
     		 sys.exit(2)
	
	for opt, arg in opts:

		if opt in ('-d','--comp'):
			
			components = arg
	

		if opt in ('-c','--cfg'):

			cfg_file = arg
			print cfg_file

		if opt in ('-s','--scale'):

			scale_number = arg
			print scale_number


		if opt in ('-o','--output'):

			pca_output = arg
			print pca_output

		if opt in ('-f','--fold'):

			fold = arg
			print fold


	Config = ConfigParser.ConfigParser()
	Config.read(cfg_file)

	
	folder_ds = ConfigSectionMap('features',Config)['scale'+scale_number]
	test_data_set = ConfigSectionMap('folds',Config)['path'+fold]
	output = pca_output

	


	ConfigPCA = ConfigParser.ConfigParser()
	ConfigPCA.read(test_data_set)

	pca_samples = ConfigSectionMap('train_pca',ConfigPCA)['samples'].split(" ")

	print os.path.isfile(folder_ds), folder_ds

	#mean = np.load(mean_path).mean(1).mean(1)
	#mean = np.array([103.939, 116.779, 123.68])
	#cnnmodel = CNN(model_path,model_text,mean,cropsize,layer)

	all_feats = []

	for i in sorted(pca_samples):
	
		env_sample = i

		print "Extracting from: ",env_sample

		if not os.path.isfile(folder_ds+'/'+env_sample+'_feat.npz'):
			continue

		#feat = splitfeats.splitScene(img,img.shape[1]/cell_space,img.shape[0]/cell_space, img.shape[1]/(cell_space*stride),img.shape[0]/(cell_space*stride),cnnmodel)
		feat = iocsv.readNPY(folder_ds+'/'+env_sample+'_feat.npz')


		all_feats.append(feat)
		#labels.append(label_count)
		#print len(all_feats)


	print np.asarray(all_feats).shape

	all_feats = np.concatenate(all_feats, axis=0)
	print all_feats.shape

	print "Components:", components
	print "Scale:",scale_number
	print "Fold:", fold

	print 'Training PCA, please wait...'

	if float(components) > 1.:
		mean,eigen = cv2.PCACompute(all_feats,None,None,maxComponents = int(components))

	elif float(components) < 1. and float(components) > 0:

		mean,eigen = cv2.PCACompute(all_feats,retainedVariance=float(components),mean=None,eigenvectors=None)
	
	print 'Done!'
	print mean.shape, eigen.shape

	savejson(mean,eigen,output)

	


