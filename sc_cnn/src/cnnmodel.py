import numpy as np
import caffe, sys, os
import cv2

class CNN:

    def __init__(self, model_path, deploy_path, mean, crop = 227, layer = 'fc7'):
        
        
        
        self.net = caffe.Net(deploy_path, model_path, caffe.TEST)
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        
        self.transformer.set_mean('data', mean)
        self.transformer.set_transpose('data', (2, 0, 1))
        self.transformer.set_channel_swap('data', (2, 1, 0))
        self.transformer.set_raw_scale('data', 255.0)
        self.crop = crop
        self.image = []
        self.layer = layer
        caffe.set_mode_gpu()
        
        print "Mean:", mean

    def setCropSize(self, size):
        self.crop = size

    def setLayer(layer):
        self.layer = layer

    def setImageByPath(self, img_path):
        img = cv2.imread(img_path, 1)
        if img is None:
            print 'Warning: Image not readable or corrupted.'
        else:
            img = caffe.io.load_image(env_sample)
        self.image = img

    def setImage(self, img):
        self.image = img

    def extractFeatures(self):
        if len(self.image) == 0:
            print 'Warning: No image detected. Features not extracted.'
            return None
        else:
            self.net.blobs['data'].reshape(1, 3, self.crop, self.crop)
            self.net.blobs['data'].data[...] = self.transformer.preprocess('data', self.image)
            self.net.forward()
            features = self.net.blobs[self.layer].data.copy()
	

            features = np.reshape(features, (features.shape[0], -1))[0]
		    
            if cv2.norm(features, cv2.NORM_L2) > 0:
                features = features / cv2.norm(features, cv2.NORM_L2)
            return features.tolist()

