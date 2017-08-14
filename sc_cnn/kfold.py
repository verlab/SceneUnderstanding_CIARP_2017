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
import sys
import os,random
import numpy as np
from random import shuffle


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


def writeCFGFile(samples_train, samples_test, str_classes,max_pc = 30, output = 'folds'):

	n_folds = len(samples_train)

	os.system("mkdir "+output)

	for i in xrange(n_folds):
		
		cfg_file = open(output+'/fold'+str(i)+'.cfg','w')	

		cfg_file.write('[Train]\n')

		
		for j in xrange(len(samples_train[i])):


			cfg_file.write(str_classes[j]+' : ')
			
			class_samples = samples_train[i][j]

			for k in class_samples:

				
				cfg_file.write(os.path.splitext(k)[0]+' ')


			cfg_file.write('\n')

		cfg_file.write('[Test]\n')


		for j in xrange(len(samples_test[i])):


			cfg_file.write(str_classes[j]+':')
			
			class_samples = samples_test[i][j]

			for k in class_samples:

				
				cfg_file.write(os.path.splitext(k)[0]+' ')


			cfg_file.write('\n')


		cfg_file.write('[train_dict]\n') #for dictionary

		train_pca = []
	
		for j in xrange(len(samples_train[i])):

			
			cfg_file.write(str_classes[j]+':')
			
			class_samples = samples_train[i][j]

			random.shuffle(class_samples)

			for k in class_samples[:max_pc]:
				
				cfg_file.write(os.path.splitext(k)[0]+' ')


			cfg_file.write('\n')									


		cfg_file.write('[train_pca]\n') #for pca

		cfg_file.write('samples :')
		
		for j in xrange(len(samples_train[i])):

			class_samples_ = samples_train[i][j]

			for k in class_samples_: #ok value?
				
				train_pca.append(str_classes[j]+'/'+os.path.splitext(k)[0])


		random.shuffle(train_pca)

		for j in train_pca[:1500]:

			cfg_file.write(j+' ')


		cfg_file.write('\n')


		cfg_file.close()
			
		

def kfold(k, list, path, folder_path_src, folder_path_dest):

        shuffle(list)
        slices = [list[i::k] for i in xrange(k)] #

	foldtrain = []
	foldtest = []

	
        for i in xrange(k):

	    test_fold = []
	    train_fold = []


            test = slices[i]
            training = [item
                        for s in slices if s is not test
                        for item in s]

           		
	    foldtrain.append(training)
	    foldtest.append(test)


	return foldtrain,foldtest

if __name__ == "__main__":


	l = []
	s = []
	n_folds = int(sys.argv[1])
	folder_path = sys.argv[2]
	folder_dest_path = sys.argv[3]
	max_per_class = int(sys.argv[4])
	samples_file = sys.argv[5]

	print "Fold: ", n_folds

	#os.system("mkdir "+folder_dest_path)

	sample_class = []
	str_classes = []

	samples = readSamples(samples_file)

	str_classes = getClasses(samples)
	
	print len(str_classes)

	amostras = []


	for fn in str_classes:

		for sample in samples:

			class_fn = sample.split('/')[0]

			if class_fn == fn:
			
				print "Sample ",os.path.abspath(folder_path+'/'+sample)
					
				sample = sample.split('/')[1].replace("\n","")
		
				s.append(sample)

	     	s_temp = s
	     	sample_class.append(kfold(n_folds,s_temp,fn,folder_path,folder_dest_path))
	      	s = []



	folds_train = []
	folds_test = []

	for i in sample_class:

		folds_train.append(i[0])
		folds_test.append(i[1])

	folds_train = np.array(folds_train)
	folds_test = np.array(folds_test)

	print len(folds_train[:,0])

	folds_t = []	
	folds_te = []
	
	for i in xrange(n_folds):

		folds_class = []

		for j in folds_train[:,i]:

			folds_class.append(j)
	
		folds_t.append(folds_class)

		folds_class = []

		for j in folds_test[:,i]:

			folds_class.append(j)
	
		folds_te.append(folds_class)


	writeCFGFile(folds_t, folds_te, str_classes,max_per_class,folder_dest_path)


	'''

	

	for fn in sorted(os.listdir(folder_path)):

	     print "Folder ",fn
	     str_classes.append(fn)
	     
	     for sample in sorted(os.listdir(folder_path+'/'+fn)):
		    print "Sample ",os.path.abspath(folder_path+'/'+fn+'/'+sample)

		    s.append(sample)

	     s_temp = s
	     sample_class.append(kfold(n_folds,s_temp,fn,folder_path,folder_dest_path))
	     s = []
	     
	folds_train = []
	folds_test = []

	for i in sample_class:

		folds_train.append(i[0])
		folds_test.append(i[1])

	folds_train = np.array(folds_train)
	folds_test = np.array(folds_test)

	print len(folds_train[:,0])

	folds_t = []	
	folds_te = []
	
	for i in xrange(n_folds):

		folds_class = []

		for j in folds_train[:,i]:

			folds_class.append(j)
	
		folds_t.append(folds_class)

		folds_class = []

		for j in folds_test[:,i]:

			folds_class.append(j)
	
		folds_te.append(folds_class)


	writeCFGFile(folds_t, folds_te, str_classes,max_per_class,folder_dest_path)

	'''





	
				






