# Configuration Files


In this section is described how to set the parameters for training and testing.


#### img_dataset

This is the paths of the main image directory. 

The *path* remains to the image directory which must be organized as: DIRECTORY > IMG CLASSES > IMG_FILES.

The *txt* remains to a file that contains a list of all images from the directory. The file is organized as:

```
class0/image_0.png
class0/image_1.png
class0/image_2.png
...
class40/image_20.png
class40/image_21.png
class40/image_22.png
```


#### features

This is the destination paths for each scale from the algorithm. For each destination directory it is saved *npy* files for each image, which contains stacked  FC or PCA features according to the respective scale.

So, the index *X* on *scaleX* remains to the cardinal number of the scale, from few to a higher number of image subdivisions.

#### folds

You can also determine the number of folds for experiment execution. For this purpose it is necesary to run *kfold.py* script and set the paths for each file. The samples are listed for training, testing, dictionary and pca steps.

#### cnn_models

This section contains the Caffe files. So you need to set the caffemodel, deploy and mean files. The crop size (it depends of network architecture) and the layer to extract the features are also necessary (See the example files). 

#### img_set

This section contains the number of subdivisions and stride size for the feature extraction process. So, "scaleX: N" is the NxN divisions over the image for the X scale (e.g scale0 is the first scale, with 1x1 subdivision while scale1 is the second scale with 2x2 subdivisions).

The stride follows almost the same idea but related to the crop dimensions. So, "stride1: 2" is a stride which performs a X,Y step with half of the crop size (<crop size width>/2,<crop size height>/2).

#### params

These parameters are related to the Dictionary Building and sparse coding process. 

*dict_sizes* are the numbers of clusters for each scale (spaced by a blank space).

*lasso* contains the λ parameters (sparsity constraint) for each scale by using LARS to solve the LASSO(L1) problem for sparse-coding. Use this configuration only if you use the Lasso for codification.

*omp* contains the λ parameters (sparsity constraint) for each scale by using OMP to solve the L0 problem for sparse-coding. Use this configuration only if you use the L0 for codification. (recommended)

If you wish to use PCA for dimension reduction, use the "with_pca: True" (Recommended). Also, for each scale you can define the number of principal components (default: 1000)

#### scripts

Finally, this section contains the list of each step performed by the method. It is not recommended to change this section, unless if you desire to add or change the implementation.
