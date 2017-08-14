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
import sys,os,getopt
from sklearn.externals import joblib
import numpy as np
from sklearn.metrics import confusion_matrix
#import matplotlib.pyplot as plt
from sklearn import svm, grid_search

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


import iocsv

def save_cm(cm,outpath):

	print cm
	fig = plt.figure()
        plt.matshow(cm)
        plt.title('Confusion Matrix')
        plt.colorbar()
        plt.ylabel('True Label')
        plt.xlabel('Predicated Label')
        fig.savefig(outpath)



def predict_svm(mat,labels,classifier,input_file):

	pred_labels = []

	
	for i in mat:

		pred_labels.append(int(classifier.predict(i.reshape(1,-1))))


	pred_labels = np.array(pred_labels)
	'''
	
	cm = confusion_matrix(labels,pred_labels)
	cm_normalized = cm.astype('float')/cm.sum(axis=1)[:,np.newaxis]
	'''
	#save_cm(cm,'confmatrix.png')

	#print pred_labels	
	
	acc = np.sum(pred_labels == labels)/float(labels.shape[0])
	
	print "File: ", os.path.basename(input_file) ,"Accuracy:", acc

	return pred_labels,acc
	

def load_pickle(svm_path):
    return joblib.load(svm_path)

# Protocol 0 is the most inefficient, and is default fo backwards compatibility. 2 is the most efficient :)
def dump_pickle(classifier, svm_path):
    joblib.dump(classifier, svm_path)


def train_best_svm(mat,labels,K_SVM='linear'):

	parameters = {'kernel':[K_SVM], 'C':[1.,1.1,1.3,1.5,1.7,1.9,2.1]}
	svr  = svm.SVC()
	clf = grid_search.GridSearchCV(svr, parameters,n_jobs=32)

	print "Training, please wait..."

	clf.fit(mat, labels.ravel())

	print "Done!"

	return clf
	

def train_svm(mat, labels, C_SVM = 1.7, K_SVM = 'linear'):
    
#    classifier = svm.SVC(kernel=K_SVM, C=C_SVM)
    classifier = svm.LinearSVC(C=C_SVM)
    classifier.fit(mat, labels.ravel())
    return classifier


if __name__ == "__main__":

	#Default parameters
	svm_mode = 'train'
	output_model = 'svm_model.pkl'
	confmat_file = 'confmat.png'
	stats_file = 'stats.png'
	with_cm = True
	with_stats = False


	try:
      		opts, args = getopt.getopt(sys.argv[1:],'m:i:l:o:c:s:',['mode=','input=','labels=','outmodel=','confmat=','stats'])
   	
	except getopt.GetoptError:
     		 print 'Need configuration file to execute.'
     		 sys.exit(2)
	
	for opt, arg in opts:

		if opt in ('-m','--mode'):
			
			svm_mode = arg
			print svm_mode


		if opt in ('-i','--input'):

			input_file = arg

		if opt in ('-l','--labels'):

			label_file = arg

		if opt in ('-o','--outmodel'):

			output_model = arg

		if opt in ('-c','--confmat'):

			confmat_file = arg
			with_cm = True


		if opt in ('-s','--stats'):
			
			stats_file = arg
			with_stats = True


	if svm_mode == 'Train':

	
		if os.path.splitext(input_file)[1] == '.csv':
			features = iocsv.readCSV(input_file)
		
		elif os.path.splitext(input_file)[1] == '.npz':

			features = iocsv.readNPY(input_file)

		labels = iocsv.readNPY(label_file)
		print features.shape
		classifier = train_svm(features,labels)
		dump_pickle(classifier,output_model)


	elif svm_mode == 'train_best':

		print "Grid Search SVM. It may take several minutes, please wait..."
		if os.path.splitext(input_file)[1] == '.csv':
			features = iocsv.readCSV(input_file)
		
		elif os.path.splitext(input_file)[1] == '.npz':

			features = iocsv.readNPY(input_file)
		labels = iocsv.readNPY(label_file)
		print features.shape
		classifier = train_best_svm(features,labels)
		dump_pickle(classifier,output_model)


		

	elif svm_mode == 'Test':

		if os.path.splitext(input_file)[1] == '.csv':
			features = iocsv.readCSV(input_file)
		
		elif os.path.splitext(input_file)[1] == '.npz':

			features = iocsv.readNPY(input_file)
		labels = iocsv.readNPY(label_file)
		print features.shape
		classifier = load_pickle(output_model)
		
		pred_labels, acc = predict_svm(features,labels,classifier,input_file)
		print pred_labels,os.path.basename(input_file).split('.')[0]+'_predlabel.csv'
		iocsv.writeCSV(pred_labels,os.path.basename(input_file).split('.')[0]+'_predlabel.csv')


		if with_stats:

			print "Mean Accuracy:", acc


		if with_cm:
			cm = confusion_matrix(labels, pred_labels)
			iocsv.writeNPY(cm, 'confmat')
			#plot_confusion_matrix(cm, range(67))
			#confmat_file = 'confmat.png'
			#save_cm(cm,confmat_file)	


	else:

		print 'Invalid svm mode, please type \'train\' for training mode or \'test\' for testing mode'










	










