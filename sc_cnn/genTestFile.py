import sys
import os,random
import numpy as np
from random import shuffle
import getopt

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


if __name__ == "__main__":


	try:
      		opts, args = getopt.getopt(sys.argv[1:],'i:m:o:',['input=','mode=','output='])
   	
	except getopt.GetoptError:
     		 print 'Need configuration file to execute.'
     		 sys.exit(2)
	
	for opt, arg in opts:

		if opt in ('-i','--input'): #input cfg file
			
			input_file = arg

		if opt in ('-m','--mode'): #output folder
			
			mode = arg

		if opt in ('-o','--output'): #output folder
			
			output_file = arg


	samples = readSamples(input_file)
	classes = getClasses(samples)

	f = open(output_file,'wb')
	f.write('['+mode+']\n')

	for i in classes:


		f.write(i+': ')
		paths = ''

		for j in samples:

			cat = j.split('/')[0]
			scat = j.split('/')[1].replace('\n','').split('.')[0]


			if i == cat:

				paths = paths+scat+' '
		#print paths
		f.write(paths+'\n')


	f.close()


	




	
