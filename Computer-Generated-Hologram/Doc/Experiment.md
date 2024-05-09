## Experiment

### Before Experiment

Before experimenting, it's best to understand common image formats and their fundamentals. Understanding the pixel level of an image will help you experiment better and give you a better understanding of the fundamentals of image processing.

Here are some examples of images you should pay more attention to the suffix of the image, and the size of the image, so that you can work with the image later.

![64×64-test.bmp](../Res/image64/test.bmp)

<img src="../Res/image256/lena.png" alt="256×256-lena.png" style="zoom:50%;" />

### Fourier Hologram

Circuitous Phase Type Hologram/Fourier Hologram is Binary hologram.

#### DataSet

For this experiment we used this image for testing

![64×64-test.bmp](../Res/image64/test.bmp)

#### Experimental Principle

Please read this [Doc](Fourier_Hologram/README.md)ument.

#### Experimental Procedure

Two ways to do experiments are provided here, Matlab or Python, and you can choose the familiar way to run the code.

- Run the `fourier_hologram.m` or `fourier_hologram.py`, They are in the Python and Matlab folders respectively.
- Then you will get Circuitous Phase Type Hologram/Fourier Hologram below.

![](../Matlab/result/fh_test_CGH.bmp)

+ Finally, after running the program, you can get the reproduced graph and compare it with the original image.

![](../Matlab/result/fh_test_recover.bmp)

### Kinoform

#### DataSet

For this experiment we used this image for testing

![256×256-lena.png](../Res/image256/lena.png)

#### Experimental Principle

Please read this [Doc](Kinoform/README.md)ument.

#### Experimental Procedure

Two ways to do experiments are provided here, Matlab or Python, and you can choose the familiar way to run the code.

- Run the `kinoforms.m` or `kinoforms.py`, They are in the Python and Matlab folders respectively.
- Then you will get Kinoform below.

![](../Python/result/ki_lena_CGH.bmp)

- Finally, after running the program, you can get the reproduced graph and compare it with the original image.

![](../Python/result/ki_lena_recover.bmp)

### Off Axis Interference Hologram

#### DataSet

For this experiment we used this image for testing

<img src="../Res/imageO/pku.jpg" style="zoom:50%;" />

#### Experimental Principle

Please read this [Doc](Interference_Hologram/README.md)ument.

#### Experimental Procedure

Two ways to do experiments are provided here, Matlab or Python, and you can choose the familiar way to run the code.

- Run the `offaxis_interference_hologram.m` or `offaxis_interference_hologram.py`, They are in the Python and Matlab folders respectively.
- Then you will get Off Axis Interference Hologram below.

![](../Python/result/oaih_pku_CGH.bmp)

- Finally, after running the program, you can get the reproduced graph and compare it with the original image.

![](../Python/result/oaih_pku_recover.bmp)





