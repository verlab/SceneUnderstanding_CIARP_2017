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
import sys, os, csv, time
import cv2,json

import getopt
import ConfigParser
import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))



#from cnnmodel import CNN
from iocsv import *
#import pooling
#import minimization
#import splitfeats

# -----------MAIN-------------#


if __name__ == "__main__":


	coeffs_outputfile = 'features.csv'
	with_pca = False
	scale_number = '0'	
	fold = '0'
	mode = 'Train'
	scale_number = '0'

	try:
	 opts, args = getopt.getopt(sys.argv[1:],'c:p:o:f:m:',['cfg=','pca=','output=','fold=','mode='])
	 print args	   	

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


			if opt in ('-o','--output'):

				coeffs_outputfile = arg
				print coeffs_outputfile

			if opt in ('-f','--fold'):

				fold = arg
				print fold


			if opt in ('-m','--mode'):

				mode = arg

			
	Config = ConfigParser.ConfigParser()
	
	Config.read(cfg_file)
	
	features_dataset_csv = ConfigSectionMap('folds',Config)['path'+fold]
	folder_ds = ConfigSectionMap('features',Config)['scale'+scale_number]	

	ConfigClasses = ConfigParser.ConfigParser()
	ConfigClasses.optionxform = str
	ConfigClasses.read(features_dataset_csv)

	classes_samples = ConfigSectionClasses(mode,ConfigClasses)

	labels = []
	all_coeffs = []
	label_count = 0

	print mode

	
	for i in sorted(classes_samples.keys()):

		env_class = i
		#all_feats = []
	
		for j in classes_samples[env_class]:
	
			env_sample = folder_ds+'/'+i+'/'+j

			if not os.path.isfile(env_sample+'_feat.npz'):
				print 'Cannot find '+env_sample
				continue

			
			print "Extracting from: ",env_sample
			feat = readNPY(env_sample+'_feat.npz')
			print np.asfortranarray(feat.tolist())	

			if with_pca:

				#feat = cv2.PCAProject(np.array(feat),mean_pca,eigen_pca)
				feat = pca.transform(feat)
				if cv2.norm(feat, cv2.NORM_L2) > 0:
                			feat = feat / cv2.norm(feat, cv2.NORM_L2)

			#print feat.shape
			all_coeffs.append(feat.tolist())
		
			labels.append(label_count)

		
		label_count = label_count + 1

	all_coeffs = np.array(all_coeffs)
	all_coeffs = np.concatenate(all_coeffs, axis=0 )
	print all_coeffs.shape

	writeNPY(np.asarray(all_coeffs),coeffs_outputfile)

	outlabel = os.path.splitext(coeffs_outputfile)[0]+"_label"	

	writeNPY(np.asarray(labels),outlabel)






