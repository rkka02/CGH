#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project :Computer-Generated-Hologram 
@File    :layer_based_method.py
@Author  :JackHCC
@Date    :2022/10/5 16:50 
@Desc    :

'''
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from propagator.angular_spectrum import asm_shift, format_img
image_path = "../Matlab/propagator/angular_spectrum/long.png"
image_path_depth = "../Matlab/propagator/angular_spectrum/longdep.png"
g = Image.open(image_path, mode="r")
# convert RGB image to Gray image
g = g.convert("L")
G = np.array(g)
G = G / 255

M, N = G.shape

g_dep = Image.open(image_path_depth, mode="r")
g_dep = g_dep.convert("L")
G_dep = np.array(g_dep)
G_dep = G_dep / 255

max_depth = np.max(G_dep)
min_depth = np.min(G_dep[G_dep > 0])

layer = 9
d = (max_depth - min_depth) / layer

pitch = 8 * pow(10, -3)
lambda_ = 639 * pow(10, -6)

yy = np.array(range(-M // 2, M // 2))
xx = np.array(range(-N // 2, N // 2))
y, x = np.meshgrid(yy * pitch, xx * pitch)

B = np.random.rand(M, N)

pad_img = np.zeros((M, N))
pad_img = pad_img.astype(complex)
part = np.zeros((M, N))

plt.figure(1)

for i in range(1, layer+1):
    part = G * ((G_dep >= (max_depth - i * d)) & (G_dep < (max_depth - (i - 1) * d)))
    plt.subplot(3, 3, i)
    plt.imshow(part, cmap="gray")
    part = part * np.exp(1j * 2 * np.pi * B)
    f = 300 + i * 5

    holo = asm_shift(part, f, pitch, lambda_, mu=2, shift=True)
    pad_img += holo

pad_img = np.angle(pad_img)
pad_img = np.mod(pad_img, 2 * np.pi) / (2 * np.pi)

plt.figure(2)
plt.imshow(pad_img, cmap="gray")

plt.show()
