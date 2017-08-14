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
import sys, os, subprocess
import ConfigParser
import getopt
import multiprocessing
from joblib import Parallel, delayed
import time

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


if __name__ == "__main__":

	output = 'test.txt'


	try:
		 opts, args = getopt.getopt(sys.argv[1:],'f:o:k:m:d:e:l:t:j:',['folder=','output=','fold=','mode=','ns1=','ns2=','lambda=','method=','dl='])
		 print args	   	

	except getopt.GetoptError:

			 
		 print 'Need configuration file to execute.'
		 sys.exit(2)
	
	for opt, arg in opts:

		if opt in ('-f','--folder'):
			
			print "Folder:", arg        	
			folder = arg
		
		if opt in ('-o','--output'):
			
			print "output:", arg        	
			output = arg

		if opt in ('-k','--fold'):
			
			print "fold:", arg        	
			fold = arg

		if opt in ('-m','--mode'):
			
			print "mode:", arg        	
			mode = arg

		if opt in ('-d','--ns1'):
			
			print "dict1:", arg        	
			ns1 = arg

		if opt in ('-e','--ns2'):
			
			print "dict2:", arg        	
			ns2 = arg

		if opt in ('-l','--lambda'):
			
			print "lambda:", arg        	
			L = arg

		if opt in ('-t','--method'):
			
			print "method:", arg        	
			meth = arg

		if opt in ('-j','--dl'):
			
			print "dlambda:", arg        	
			dlambda = arg




	dict_imnet_s1 = folder+'/dicts/dict_imnet_s1_f'+fold+'_'+ns1+'_dl'+dlambda.replace('.','')+'.npz'
	dict_imnet_s2 = folder+'/dicts/dict_imnet_s2_f'+fold+'_'+ns2+'_dl'+dlambda.replace('.','')+'.npz'

	dict_places_s1 = folder+'/dicts/dict_places_s1_f'+fold+'_'+ns1+'_dl'+dlambda.replace('.','')+'.npz'
	dict_places_s2 = folder+'/dicts/dict_places_s2_f'+fold+'_'+ns2+'_dl'+dlambda.replace('.','')+'.npz'


	dict_imnet = folder+'/dicts/dict_imnet_s1_s2_f'+fold+'_'+ns1+ns2+'_dl'+dlambda.replace('.','')+'.npz'
	dict_places = folder+'/dicts/dict_places_s1_s2_f'+fold+'_'+ns1+ns2+'_dl'+dlambda.replace('.','')+'.npz'

	pca_places_s1 = folder+'/pca/pca_places_s1_f'+fold+'.json'	
	pca_places_s2 = folder+'/pca/pca_places_s2_f'+fold+'.json'

	pca_imnet_s1 = folder+'/pca/pca_imnet_s1_f'+fold+'.json'
	pca_imnet_s2 = folder+'/pca/pca_imnet_s2_f'+fold+'.json'	


	places_config_file = folder+'/PLACES.cfg'
	imnet_config_file = folder+'/IMNET.cfg'	
		
	Config_places = ConfigParser.ConfigParser()
	Config_places.read(places_config_file)
	Config_imnet = ConfigParser.ConfigParser()
	Config_imnet.read(imnet_config_file)


	selectedImgs = ConfigSectionMap('img_dataset',Config_places)['txt']
	poolScript = ConfigSectionMap('scripts',Config_places)['poolscript']
	svmScript = ConfigSectionMap('scripts',Config_places)['svmscript']
	concatScript = ConfigSectionMap('scripts',Config_places)['concatscript']
	stackScript = ConfigSectionMap('scripts',Config_places)['stackscript']
	pcaScript = ConfigSectionMap('scripts',Config_places)['pcascript']
	dictScript = ConfigSectionMap('scripts',Config_places)['dictscript']
	saveScript = ConfigSectionMap('scripts',Config_places)['savescript']
	cdictScript = ConfigSectionMap('scripts',Config_places)['cdictscript']

	cnn_places = ConfigSectionMap('features',Config_places)['scale0']
	features_places = [ConfigSectionMap('features',Config_places)['scale1'],ConfigSectionMap('features',Config_places)['scale2']] 
	features_imnet = [ConfigSectionMap('features',Config_imnet)['scale1'],ConfigSectionMap('features',Config_imnet)['scale2']] 

	num_cores = multiprocessing.cpu_count()


	scales = ['1','2']	
	trained_feat = ['places','imnet']

	
	calls = []
	callspca = []
	callsdict = []
	callsfeats =[]

	#create folders
	
	print "Creating folders..."
	if not os.path.isdir(folder+'/pca'):
		os.system('mkdir '+folder+'/pca')

	if not os.path.isdir(folder+'/cnn'):
		os.system('mkdir '+folder+'/cnn')

	if not os.path.isdir(folder+'/dicts'):
		os.system('mkdir '+folder+'/dicts')

	if not os.path.isdir(folder+'/svm'):
		os.system('mkdir '+folder+'/svm')

	if not os.path.isdir(folder+'/sc_feats'):
		os.system('mkdir '+folder+'/sc_feats')
	

	if not os.path.isdir(folder+'/PLACES_feats'):
		os.system('mkdir '+folder+'/PLACES_feats')


	if not os.path.isdir(folder+'/IMNET_feats'):
		os.system('mkdir '+folder+'/IMNET_feats')
	

	print "Saving Features..."

	os.system('python '+saveScript+' --cfg '+folder+'/PLACES.cfg --input '+selectedImgs+' -s 0 -o '+folder+'/PLACES_feats/PLACES_227 -r 227')
	
	for i in scales:
		print "Scale ", i

		if i == '1':
			
			rsize = '451'

		elif i == '2':
			
			rsize = '899'


		for j in trained_feat:

			if j == 'places':

				call_feat = 'python '+saveScript+' --cfg '+folder+'/PLACES.cfg --input '+selectedImgs+' -s '+i+' -o '+folder+'/PLACES_feats/PLACES_'+rsize+' -r '+rsize
				callsfeats.append(call_feat)

			if j == 'imnet':
				
				call_feat = 'python '+saveScript+' --cfg '+folder+'/IMNET.cfg --input '+selectedImgs+' -s '+i+' -o '+folder+'/IMNET_feats/IMNET_'+rsize+' -r '+rsize
				callsfeats.append(call_feat)

	if len(callsfeats) > 0:
		print "Saving Feats"
		Parallel(n_jobs=num_cores)(delayed(os.system)(i) for i in callsfeats)
		print "Done"
 

	print "Stacking CNN Features..."

	if not os.path.isfile(folder+'/cnn/cnn_'+mode+'_f'+fold+'.npz'):
		os.system('python '+stackScript+' --cfg '+folder+'/PLACES.cfg --fold '+fold+' --mode '+mode.title()+' --output '+folder+'/cnn/cnn_'+mode+'_f'+fold)
		print "Done"
	
	#PCA
	
	print "Performing PCA"


	for i in scales:
		print 'scale ', i

		for j in trained_feat:
			print j

			if j == 'places' and not os.path.isfile(folder+'/pca/pca_places_s'+i+'_f'+fold+'.json'):	
				call_pca = 'python '+pcaScript+' --cfg '+places_config_file+' -d 1000 -s '+i+' -f '+fold+' -o '+folder+'/pca/pca_places_s'+i+'_f'+fold+'.json'
				callspca.append(call_pca)

			if j == 'imnet' and not os.path.isfile(folder+'/pca/pca_imnet_s'+i+'_f'+fold+'.json'):

				call_pca = 'python '+pcaScript+' --cfg '+imnet_config_file+' -d 1000 -s '+i+' -f '+fold+' -o '+folder+'/pca/pca_imnet_s'+i+'_f'+fold+'.json'	
				callspca.append(call_pca)
	if len(callspca) > 0:
		print "Performing PCA"
		Parallel(n_jobs=num_cores)(delayed(os.system)(i) for i in callspca)
		print "Done"
	
	
	print "Building Dictionary"
	#Dictionary
	for i in scales:

		if i == '1':
			dsize = ns1
			rsize = '451'
			

		elif i == '2':
			dsize = ns2
			rsize = '899'

		for j in trained_feat:

			
			if j == 'places':
				
				if i == '1':
					dict_ = dict_places_s1

				elif i == '2':
					dict_ = dict_places_s2				

				if not os.path.isfile(dict_):

					call_dict = 'python '+dictScript+' --cfg '+places_config_file+' -s '+i+' -o '+os.path.splitext(dict_)[0]+' -f '+fold+' -n '+dsize+' -r '+rsize+' -l '+dlambda+' --pca '+folder+'/pca/pca_places_s'+i+'_f'+fold+'.json' + ' --cnn PLACES'
					callsdict.append(call_dict)				

			if j == 'imnet': 

				if i == '1':
					dict_ = dict_imnet_s1

				elif i == '2':
					dict_ = dict_imnet_s2	

				if not os.path.isfile(dict_):

					call_dict = 'python '+dictScript+' --cfg '+imnet_config_file+' -s '+i+' -o '+os.path.splitext(dict_)[0]+' -f '+fold+' -n '+dsize+' -r '+rsize+' -l '+dlambda+' --pca '+folder+'/pca/pca_imnet_s'+i+'_f'+fold+'.json' ' --cnn IMNET'
					callsdict.append(call_dict)

	if len(callsdict) > 0:
		print "Performing Dictionaries"
		Parallel(n_jobs=num_cores)(delayed(os.system)(i) for i in callsdict)
		print "Done"
	


	print "Concatenating Dictionaries"

	if not os.path.isfile(dict_imnet):
		os.system('python '+cdictScript+' --input1 '+dict_imnet_s1+' --input2 '+dict_imnet_s2+' --output '+os.path.splitext(dict_imnet)[0])

	if not os.path.isfile(dict_places):
		os.system('python '+cdictScript+' --input1 '+dict_places_s1+' --input2 '+dict_places_s2+' --output '+os.path.splitext(dict_places)[0])


	
	#SPARSE CODING
	for i in scales:

		for j in trained_feat:

		
			if j == 'places' and not os.path.isfile(folder+'/sc_feats/places_s'+i+'_'+mode+'_pca_f'+fold+'_'+meth+'_'+L.replace('.','')+'_d'+ns1+ns2+'_dl'+dlambda.replace('.','')+'.npz'):
				
				print "call PLACES"	
				call_str = 'python '+poolScript+' --cfg '+places_config_file+' -d '+dict_places+' --pca '+folder+'/pca/pca_places_s'+i+'_f'+fold+'.json -o '+folder+'/sc_feats/places_s'+i+'_'+mode+'_pca_f'+fold+'_'+meth+'_'+L.replace('.','')+'_d'+ns1+ns2+'_dl'+dlambda.replace('.','')+' -f '+fold+' -m '+meth+' -j max -l '+L+' -t '+mode.title()+' -s '+i			
				calls.append(call_str)
				print call_str				


			if j == 'imnet' and not os.path.isfile(folder+'/sc_feats/imnet_s'+i+'_'+mode+'_pca_f'+fold+meth+'_'+L.replace('.','')+'_d'+ns1+ns2+'_dl'+dlambda.replace('.','')+'.npz'):
			
				print "call IMNET"	
				call_str = 'python '+poolScript+' --cfg '+imnet_config_file+' -d '+dict_imnet+' --pca '+folder+'/pca/pca_imnet_s'+i+'_f'+fold+'.json -o '+folder+'/sc_feats/imnet_s'+i+'_'+mode+'_pca_f'+fold+meth+'_'+L.replace('.','')+'_d'+ns1+ns2+'_dl'+dlambda.replace('.','')+' -f '+fold+' -m '+meth+' -j max -l '+L+' -t '+mode.title()+' -s '+i
				calls.append(call_str)
				print call_str

	
	
	if len(calls) > 0:
		print "Performing Sparse Coding"
		Parallel(n_jobs=num_cores)(delayed(os.system)(i) for i in calls)
		print "Done"

	
	print "Concatenating features"

	if not os.path.isfile(folder+'/sc_feats/featFull_'+mode+'_pca_f'+fold+meth+'_'+L.replace('.','')+'d_'+ns1+ns2+'_dl'+dlambda.replace('.','')+'_.csv'):
	
		#os.system('python '+concatScript+' --input1 '+folder+'/cnn/cnn_'+mode+'_f'+fold+'.npz --input2 '+folder+'/sc_feats/places_s1_'+mode+'_pca_f'+fold+'_'+meth+'_'+L.replace('.','')+'_d'+ns1+ns2+'_dl'+dlambda.replace('.','')+'.npz --input3 '+folder+'/sc_feats/imnet_s2_'+mode+'_pca_f'+fold+meth+'_'+L.replace('.','')+'_d'+ns1+ns2+'_dl'+dlambda.replace('.','')+'.npz --output '+folder+'/sc_feats/featFull_'+mode+'_pca_f'+fold+meth+'_'+L.replace('.','')+'d_'+ns1+ns2+'_dl'+dlambda.replace('.','')+'.csv')
		input1  = folder+'/cnn/cnn_'+mode+'_f'+fold+'.npz'
		input2  = folder+'/sc_feats/places_s1_'+mode+'_pca_f'+fold+'_'+meth+'_'+L.replace('.','')+'_d'+ns1+ns2+'_dl'+dlambda.replace('.','')+'.npz'
		input3  = folder+'/sc_feats/places_s2_'+mode+'_pca_f'+fold+'_'+meth+'_'+L.replace('.','')+'_d'+ns1+ns2+'_dl'+dlambda.replace('.','')+'.npz'
		input4  = folder+'/sc_feats/imnet_s1_'+mode+'_pca_f'+fold+meth+'_'+L.replace('.','')+'_d'+ns1+ns2+'_dl'+dlambda.replace('.','')+'.npz'
		input5  = folder+'/sc_feats/imnet_s2_'+mode+'_pca_f'+fold+meth+'_'+L.replace('.','')+'_d'+ns1+ns2+'_dl'+dlambda.replace('.','')+'.npz'
		output_ = folder+'/sc_feats/featFull_'+mode+'_pca_f'+fold+meth+'_'+L.replace('.','')+'d_'+ns1+ns2+'_dl'+dlambda.replace('.','')+'_.csv'
		os.system('python ' + concatScript + ' --input1 ' + input1 + ' --input2 ' + input2 + ' --input3 ' + input3 + ' --input4 ' + input4 + ' --input5 ' + input5 + ' --output '+ output_)
	print "Done"
	
	
	
	print mode+"ing..."

	#feat_full = folder+'/sc_feats/featFull_'+mode+'_pca_f'+fold+meth+'_'+L.replace('.','')+'d_'+ns1+ns2+'_dl'+dlambda.replace('.','')+'.csv'
	featfull5 = folder+'/sc_feats/featFull_'+mode+'_pca_f'+fold+meth+'_'+L.replace('.','')+'d_'+ns1+ns2+'_dl'+dlambda.replace('.','')+'_.csv'
	svm_str = 'python '+svmScript+' --input '+ featfull5 + ' --label '+folder+'/sc_feats/places_s1_'+mode+'_pca_f'+fold+'_'+meth+'_'+L.replace('.','')+'_d'+ns1+ns2+'_dl'+dlambda.replace('.','')+'_label.csv.npz -o '+folder+'/svm/svm-f'+fold+'_lambda'+L.replace('.','')+'_m'+meth+'_d'+ns1+ns2+'_dl'+dlambda.replace('.','')+'_.pkl --mode '+mode

	if mode == 'Train':

		os.system(svm_str)

	elif mode == 'Test':

		save_file = output+'f_'+fold+'_lambda'+L.replace('.','')+'_m'+meth+'_d'+ns1+ns2+'_dl'+dlambda.replace('.','')+'.txt'
		os.system(svm_str+' >> '+save_file)
	















	
				

