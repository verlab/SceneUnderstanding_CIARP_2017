from keras.models import *
from keras.layers import *
from keras.optimizers import *
from keras.layers.core import *
import sys,os,cv2
from keras import regularizers
import numpy as np
import theano
from theano import tensor as T
from keras import backend as K
from keras.regularizers import Regularizer
import theano
import pickle

def kl_divergence(p, p_hat):

	return (p * K.log(p/ p_hat)) + ((1-p) * K.log((1-p) /(1-p_hat)))

class ActivityRegularizer(Regularizer):
    def __init__(self, l1=0.1, l2=0.1):
        self.l1 = l1
        self.l2 = l2
	self.uses_learning_phase = False

    def set_layer(self, layer):
        self.layer = layer

    def __call__(self, loss):

	
        output = self.layer.output
	p_hat = K.sum(K.mean(K.abs(output), axis=0))
	
        #loss += self.l1 * K.sum(K.mean(K.abs(output), axis=0))
        #loss += self.l2 * K.sum(K.mean(K.square(output), axis=0))
        return loss

    def get_config(self):
        return {"name": self.__class__.__name__,
                "l1": self.l1,
                "l2": self.l2}



class SparseActivityRegularizer(Regularizer):

    def __init__(self, l1=0., l2=0., p=0.001, slambda=0.001):

	self.uses_learning_phase = False
	self.l2 = l2
	self.l1 = l1
	self.p = p
	self.slambda = slambda

    def set_layer(self, layer):
        self.layer = layer

    def __call__(self, loss):
	
	for i in range(len(self.layer.inbound_nodes)):

		output = self.layer.output[i]
		p_hat = K.sum(K.mean(output, axis=0))
		loss += self.slambda*kl_divergence(self.p, p_hat)
		#print "output:",self.slambda, p_hat

	return loss

    def get_config(self):
        return {"name": self.__class__.__name__, 
		"p":self.p,
		"l1":self.l1,
		"l2":self.l2,
		"slambda":self.slambda}

def sampling(args):
    z_mean, z_log_var,batch_size,latent_dim = args
    epsilon = K.random_normal(shape=(batch_size, latent_dim), mean=0.)
    return z_mean + K.exp(z_log_var / 2) * epsilon

def vae_loss(x, x_decoded_mean):
    xent_loss = original_dim * objectives.binary_crossentropy(x, x_decoded_mean)
    kl_loss = - 0.5 * K.sum(1 + z_log_var - K.square(z_mean) - K.exp(z_log_var), axis=-1)
    return xent_loss + kl_loss


def buildVAE(X,dict_size,model_output):


	batch_size = 256
	original_dim = X.shape[1]
	latent_dim = 50
	intermediate_dim = X.shape[1]/2
	nb_epoch = 200

	x = Input(batch_shape=(batch_size, original_dim))
	h = Dense(intermediate_dim, activation='relu')(x)
	z_mean = Dense(latent_dim)(h)
	z_log_var = Dense(latent_dim)(h)

	z = Lambda(sampling, output_shape=(latent_dim,))([z_mean, z_log_var,batch_size,latent_dim])

	# we instantiate these layers separately so as to reuse them later
	decoder_h = Dense(intermediate_dim, activation='relu')
	decoder_mean = Dense(original_dim, activation='sigmoid')
	h_decoded = decoder_h(z)
	x_decoded_mean = decoder_mean(h_decoded)

	vae = Model(x, x_decoded_mean)
	vae.compile(optimizer='rmsprop', loss=vae_loss)
	
	vae.fit(x_train, x_train, shuffle=True,  nb_epoch=nb_epoch, batch_size=batch_size)
	
	with open(model_output, 'wb') as outfile:
        	pickle.dump(vae, outfile, pickle.HIGHEST_PROTOCOL)



def buildAE(X,dict_size,model_output):

	
	input_sample = Input(shape=(X.shape[1],))
	encoded = Dense(dict_size, activation='linear')(input_sample)
	encoded = Dense(dict_size/2, activation='linear')(encoded)
	encoded = Dense(dict_size/4, activation='linear')(encoded)
	decoded = Dense(dict_size/2,activation='linear')(encoded)
	decoded = Dense(dict_size,activation='linear')(decoded)	
	decoded = Dense(X.shape[1],activation='linear')(decoded)

	autoencoder = Model(input=input_sample, output=decoded)


	#autoencoder.compile(loss='binary_crossentropy', optimizer=SGD(lr=0.3, momentum=0.5))
	autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
	autoencoder.fit(X, X, nb_epoch=1000, batch_size=256,verbose=True,shuffle=True)

	sys.setrecursionlimit(10000)

	with open(model_output, 'wb') as outfile:
        	pickle.dump(autoencoder, outfile, pickle.HIGHEST_PROTOCOL)

	
def loadModel(weights_path):

	with open(weights_path, 'rb') as infile:
        	return pickle.load(infile)


def returnAEncoding(X,encoder):

	#Enc = Sequential()
	#Enc.add(encoder)
	#Enc.compile(loss = "mean_squared_error", optimizer = "sgd")
	#Enc.fit(X.transpose(),X.transpose())
	
	#encoder_func = K.function([Enc.layers[0].input], [Enc.layers[1].output])
	#encoder_output = encoder_func([X.transpose()])[0]

	get_feature = K.function([encoder.layers[0].input, K.learning_phase()], encoder.layers[4].output)
	feat = get_feature([X.transpose(),0]) # 0 -> train=false
	print feat,X
	return feat.transpose()



	

