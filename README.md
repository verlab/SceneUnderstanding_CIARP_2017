# Project #

This code is based on the paper __A Robust Indoor Scene Recognition Method based on Sparse Representation__ on the __22nd Iberoamerican Congress on Pattern Recognition__ (CIARP 2017). The goal of this software is to build a robust representation of scene images, that conveys global as well as local information, for the task of scene recognition. We  built  an  over-complete dictionary  whose  base  vectors  are feature vectors extracted from fragments of a scene, and the final representation of an image is a linear combination of the visual features of objects’ fragments. 


## Contact ##

### Authors ###

* Guilherme Nascimento - MSc student - UFMG - guigonasc@gmail.com
* Camila Laranjeira - MSc student - UFMG - mila.laranjeira@gmail.com
* Vinicius Braz - Undergraduate Student - UFMG - viniciusbraz30@gmail.com
* Anisio Lacerda - Co-Advisor - UFMG - anisiom@gmail.com
* Erickson R. Nascimento - Advisor - UFMG - erickson@dcc.ufmg.br


### Institution ###

Federal University of Minas Gerais (UFMG)  
Computer Science Department  
Belo Horizonte - Minas Gerais -Brazil 

### Laboratory ###

__VeRLab:__ Laboratory of Computer Vison and Robotics   
http://www.verlab.dcc.ufmg.br

## Program ##

### Dependencies ###

* [OpenCV 3.2.0](http://docs.opencv.org/3.3.0/)
* [Caffe 1.0.0](http://caffe.berkeleyvision.org/)
* [Spams 2.5](http://spams-devel.gforge.inria.fr/downloads.html)
* [CUDA 8.0 (GPU version only)](https://developer.nvidia.com/cuda-toolkit)
* [cuDNN v5 (GPU version only)](https://developer.nvidia.com/cudnn)
* Numpy, Scikit Image, Scikit Learn, Scipy, Pickle


### Usage ###
Config File: 

Run runtest.py using the following parameters:
-f: Main folder where are all the files necessary for program execution;
-o: Where the output file will be stored. Default = root folder provided in -f, but can be changed;
-k: train test split;                
-m: operation mode;
-d: Scale dictionary size 1;
-e: Scale dictionary size 2;
-l: lambda value;
-t: minimization method;
-j: lambda value.

Example of Usage:
 python run_test.py -f /root/output -o /root/output/result_ -k 4 -m train -d 603 -e 3283 -l 0.1 -t OMP -j 0.03 
 
## Citation ##

If you are using it to academic purpose, please cite: 

G. Nascimento, C. Laranjeira, V. Braz, A. Lacerda, E. R. Nascimento, __A Robust Indoor Scene Recognition Method based on Sparse Representation__, in: 22nd Iberoamerican Congress on Pattern Recognition -- e o resto?, Springer International Publishing, Amsterdam, NL, 2016, pp. 557–571. doi:10.1007/978-3-319-46604-0_40.


### Bibtex entry ###

> @InBook{Silva2016,  
>            Title     = { Robust Indoor Scene Recognition Method based on Sparse Representation},  
>            Author    = {Nascimento, Guilherme and Laranjeira, Camila and Braz,Vinicius and Lacerda, Anisio and Nascimento, Erickson Rangel},  
>            Editor    = {Hua, Gang and J{\
e}gou, Herv{\'e}},  
>            Pages     = {557--571},  
>            Publisher = {Springer International Publishing},  
>            Year      = {2017},  
>            Address   = {Cham},  
>            Booktitle = {Computer Vision -- ECCV 2016 Workshops: Amsterdam, The Netherlands, October 8-10 and 15-16, 2016, Proceedings, Part I},  
>            Doi       = {10.1007/978-3-319-46604-0_40},  
>            ISBN      = {978-3-319-46604-0},  
>            Url       = {http://dx.doi.org/10.1007/978-3-319-46604-0_40}  
> }

### Coming Soon ###
Project Page
Docker
Documentation

###### Enjoy it. ######
