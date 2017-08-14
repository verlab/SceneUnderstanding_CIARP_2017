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

def maxPool(mat, axis = 1):
	return mat.max(axis = axis)

#def maxPool(mat,axis = 1):
#
#	return mat.max(axis = axis)

        
#def meanPool(mat,axis = 1):

#	return abs(mat).mean(axis = axis)
	
#def medianPool(mat, axis = 1)

#	return mat.median(axis = axis)
	
#def LLC(mat)#todo

#	pass


