import numpy as np

def maxPool(mat,axis = 1):

	return mat.max(axis=axis)

        
def meanPool(mat,axis = 1):

	return abs(mat).mean(axis=axis)
	
def medianPool(mat, axis = 1)

	return mat.median(axis=axis)
	
def LLC(mat)#todo

	pass


