# Project #

This code is based on the paper [Towards Semantic Fast-Forward and Stabilized Egocentric Video](http://www.verlab.dcc.ufmg.br/wp-content/uploads/2016/10/Final_Draft_ECCVW_2016_Towards_Semantic_Fast_Forward_and_Stabilied_Egocentric_Videos.pdf) on the __First International Workshop on Egocentric Perception, Interaction and Computing__ at __European Conference on Computer Vision__ (EPIC@@ECCV 2016). The goal of the program is to stabilize a fast-forward version of a video, using the dropped frames to reconstruct distorted images during the processing. 

## Contact ##

### Authors ###

* Guilherme Nascimento - MSc student - UFMG - guilherme[]@dcc.ufmg.br
* Camila Laranjeira - MSc student - UFMG - camila[]@dcc.ufmg.br
* Vinicius Braz - Undergraduate Student - UFMG - vinicius[]@dcc.ufmg.br
* Anisio Lacerda - MSc student - UFMG - anisio[]@dcc.ufmg.br
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

* OpenCV 3.2.0 _(Tested with 2.4.9 and 2.4.13)
* Caffe 1.0.0
* Spams 2.5
* CUDA 8.0 (GPU version only)
* cuDNN v5 (GPU version only)
* Numpy, Scikit Image, Scikit Learn, Scipy, Pickle


### Usage ###
Config File: 

Example of Usage:
 python run_test.py -c  
            user@computer:<project_path/build>: < Program_name > < Settings_file > [-h] [Range_min = 0 ] [Range_max = num_frames ]

Example 1: Run VideoStabilization using Help option.

            user@computer:<project_path/build>: ./VideoStabilization -h 

Example 2: Run VideoStabilization in the Experiment_1 processing the whole video. 
            
            user@computer:<project_path/build>: ./VideoStabilization Experiment_1.xml

Example 3: Run VideoStabilization in the Experiment_1 processing from the 150 frame until the last one. 

            user@computer:<project_path/build>: ./VideoStabilization Experiment_1.xml 150 

Example 4: Run VideoStabilization in the Experiment_1 processing from the 150 frame until the frame 490. 

            user@computer:<project_path/build>: ./VideoStabilization Experiment_1.xml 150 490

## Citation ##

If you are using it to academic purpose, please cite: 

M. M. Silva, W. L. S. Ramos, J. P. K. Ferreira, M. F. M. Campos, E. R. Nascimento, __Towards semantic fast-forward and stabilized egocentric videos__, in: European Conference on Computer Vision Workshops, Springer International Publishing, Amsterdam, NL, 2016, pp. 557–571. doi:10.1007/978-3-319-46604-0_40.

### Bibtex entry ###

> @InBook{Silva2016,  
>            Title     = {Towards Semantic Fast-Forward and Stabilized Egocentric Videos},  
>            Author    = {Silva, Michel Melo and Ramos, Washington Luis Souza and Ferreira,Joao Pedro Klock and Campos, Mario Fernando Montenegro and Nascimento, Erickson Rangel},  
>            Editor    = {Hua, Gang and J{\'e}gou, Herv{\'e}},  
>            Pages     = {557--571},  
>            Publisher = {Springer International Publishing},  
>            Year      = {2016},  
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
