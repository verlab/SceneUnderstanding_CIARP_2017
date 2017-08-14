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
import sys, os, spams, csv, time
def cod2sparseSOMP(D,X,L = 20, numThreads = -1):

    

    #D = np.asfortranarray(D / np.tile(np.sqrt((D*D).sum(axis=0)),(D.shape[0],1)))

    X_ = np.asfortranarray(X)
    D_ = np.asfortranarray(D)
    

    print "Using Simultaneous Orthogonal Matching Pursuit for sparse codification. Please wait..."



    init_time = time.time()
    ind_groups = np.array(xrange(0,X_.shape[1],1),dtype=np.int32)
    alpha = spams.somp(X=X_,D=D_,L=L,list_groups = ind_groups,numThreads = numThreads)

    end_time = time.time()

    t = end_time - init_time

    print "%f signals processed per second\n" %(float(alpha.shape[1]) / t)

    print "Total time: ", t, "seconds"

    A = alpha.todense()
    
    #print A[0]

    return A

def cod2sparseOMP(D,X,L = 20, numThreads = -1):

    

    #D = np.asfortranarray(D / np.tile(np.sqrt((D*D).sum(axis=0)),(D.shape[0],1)))

    X_ = np.asfortranarray(X)
    D_ = np.asfortranarray(D)
    

    print "Using Orthogonal Matching Pursuit for sparse codification. Please wait..."

    init_time = time.time()

    alpha = spams.omp(X_,D_,L=L,return_reg_path = False,numThreads = numThreads)

    end_time = time.time()

    t = end_time - init_time

    print "%f signals processed per second\n" %(float(alpha.shape[1]) / t)

    print "Total time: ", t, "seconds"

    A = alpha.todense()
    
    #print A[0]

    return A

def cod2sparseLASSO(dictionary,feat,lambdaLasso = 0.35, numThreads = -1):

    init_time = time.time()

    X_ = np.asfortranarray(feat)
    D_ = np.asfortranarray(dictionary)

    param = {
    'lambda1' : lambdaLasso    , # not more than 20 non-zeros coefficients
    'numThreads' : numThreads, # number of processors/cores to use; the default choice is -1
    # and uses all the cores of the machine
    'pos' : False,
    'mode' : spams.PENALTY}        # penalized formulation

    print "Using LASSO for sparse codification. Please wait..."

    alpha = spams.lasso(X_,D_,return_reg_path = False,verbose=True,**param)

    end_time = time.time()

    t = end_time - init_time

    print "%f signals processed per second\n" %(float(alpha.shape[1]) / t)

    print "Total time: ", t, "seconds"

    return alpha.todense()

