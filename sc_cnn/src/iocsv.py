import numpy as np
import csv

def writeNPY(mat,pathname,labels=''):

    output_arr = np.asarray(mat).astype('float')
    output_arr = np.float64(output_arr)


    if labels == '':
    	np.savez_compressed(pathname,output_arr)

    else:

	np.savez_compressed(pathname,a=output_arr,b=labels)	

def readNPY(pathname):

    mat = np.load(pathname)
    feat_mat = np.array(mat['arr_0'])
    mat.close()
    #dict_mat_fortran = np.asfortranarray(mat).astype('double')
    return np.asfortranarray(feat_mat).astype('double')#dict_mat_fortran


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

def ConfigSectionClasses(section,Config):

	Config.optionxform = str
	options = Config.options(section)
	mat_classes = []

	dict1 = {}

	for i in sorted(options):

		dict1[i] = Config.get(section,i).split(' ')


	return dict1


def ConfigSectionMap(section,Config):
   
    #Config.optionxform = str
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

