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
import sys, os, random
import cv2,csv
import getopt



sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from iocsv import *

def powerNorm(vec):


	pN = sum


def writeCSV(mat,pathname):

    #output_arr = np.asarray(mat)
    output_arr = np.asarray(mat).astype('float')
    output_arr = np.float64(output_arr)
    np.savetxt(pathname,output_arr,delimiter=' ')


def readCSV(pathname):

    mat = []

    with open(pathname,'rb') as mat_file:

        reader = csv.reader(mat_file, delimiter=' ')

        for i in reader:

            row = filter(None,i)
            row_ = np.array(row).astype('float')
            mat.append(row_)


    dict_mat_fortran = np.asfortranarray(mat).astype('double')
    print dict_mat_fortran.dtype

    return dict_mat_fortran


if __name__ == '__main__':
	
	
	with_3 = False
	output = 'features.csv'

	#Concat Features
	
	try:
      		opts, args = getopt.getopt(sys.argv[1:],'i1:i2:i3:o:',['input1=','input2=','output='])
   	
	except getopt.GetoptError:
     		 print 'Need configuration file to execute.'
     		 sys.exit(2)
	
	for opt, arg in opts:

		if opt in ('-i1','--input1'):

			featarg1 = arg

		if opt in ('-i2','--input2'):

			featarg2 = arg


		if opt in ('-o','--output'):

			output = arg


	
	dict1= readNPY(featarg1).transpose()
	dict2 = readNPY(featarg2).transpose()
	
	print dict1.shape, dict2.shape
	
	
	multi_Train = np.concatenate((dict1, dict2), axis=1)
	print multi_Train.shape
		
	writeNPY(multi_Train.transpose(),output)
	

