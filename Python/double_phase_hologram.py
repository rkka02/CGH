#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project :Computer-Generated-Hologram 
@File    :double_phase_hologram.py
@Author  :JackHCC
@Date    :2022/10/5 16:01 
@Desc    :Todo: DPH need fix bugs

'''
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from propagator.angular_spectrum import asm_shift, format_img


pitch = 8 * pow(10, -3)
lambda_ = 638 * pow(10, -6)
z = 400

# input the image path
# image_path = "../Res/Set5/GTmod12/butterfly.png"
image_path = "../Matlab/propagator/angular_spectrum/triss1024.png"
g = Image.open(image_path, mode="r")
# convert RGB image to Gray image
g = g.convert("L")
plt.figure(1)
plt.imshow(g, cmap="gray")
G = np.array(g)
G = G / 255
print(G)

M, N = G.shape

# 生成随机相位
B = np.random.rand(M, N)
object_ = G * np.exp(1j * 2 * np.pi * B)

# 带随机相位
final1 = asm_shift(object_, z, pitch, lambda_, mu=2)
# 仅振幅信息
final2 = asm_shift(G, z, pitch, lambda_, mu=2)

angle = np.angle(final2)
angle = np.mod(angle, 2 * np.pi)
amp = np.abs(final2)
amp = amp / np.max(amp)
coss = np.arccos(amp)

phase_1 = angle + coss
phase_2 = angle - coss

checkerboard_1 = np.zeros((M, N))

for i in range(M):
    for j in range(N):
        if np.mod(i + j, 2) == 0:
            checkerboard_1[i, j] = 1


checkerboard_2 = 1 - checkerboard_1

final2 = phase_1 * checkerboard_1 + phase_2 + checkerboard_2
final2 = np.mod(final2, 2 * np.pi) / (2 * np.pi)

angle_1 = np.angle(final1)
angle_1 = np.mod(angle_1, 2 * np.pi)
final1 = angle_1 / (2 * np.pi)

# 随机相位
plt.figure(2)
plt.imshow(final1, cmap="gray")

# 双相位
plt.figure(3)
plt.imshow(final2, cmap="gray")

final1 = np.exp(1j * 2 * np.pi * final1)
final2 = np.exp(1j * 2 * np.pi * final2)

image1 = asm_shift(final1, z, pitch, lambda_, mu=2, direction="backward", shift=False)
image2 = asm_shift(final2, z, pitch, lambda_, mu=2, direction="backward", shift=False)
image1, image2 = np.abs(image1), np.abs(image2)

image1 = image1 / np.max(image1)
image2 = image2 / np.max(image2)
image2 = format_img(image2)

plt.figure(4)
plt.imshow(image1, cmap="gray")

plt.figure(5)
plt.imshow(image2, cmap="gray")
plt.show()
