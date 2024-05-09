#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project :Computer-Generated-Hologram 
@File    :angular_spectrum.py
@Author  :JackHCC
@Date    :2022/10/5 14:10 
@Desc    :

'''
from PIL import Image
import numpy as np
from scipy.fftpack import fft2, fftshift, ifft2
import matplotlib.pyplot as plt


def format_img(img):
    # img = img ** 0.5
    format_img = img * 255
    format_img = format_img.astype(np.uint8)
    return format_img


def asm(input_image, z, pitch, lambda_, mu=1, cut=True, direction="forward", band_limit=True):
    input_image = np.array(input_image)
    h, w = input_image.shape
    height, width = h * mu, w * mu
    u0 = 1 / width / pitch
    v0 = 1 / height / pitch

    pad_img = np.zeros((height, width))
    yy = v0 * np.array(range(-height // 2, height // 2))
    xx = u0 * np.array(range(-width // 2, width // 2))
    x, y = np.meshgrid(xx, yy)

    pad_img[height//2-h//2:height//2+h//2, width//2-w//2:width//2+w//2] = input_image
    if direction == "forward":
        trans = np.exp(1j * 2 * np.pi / lambda_ * z * np.sqrt(1 - np.power(lambda_ * x, 2) - np.power(lambda_ * y, 2)))
    else:
        trans = np.exp(-1j * 2 * np.pi / lambda_ * z * np.sqrt(1 - np.power(lambda_ * x, 2) - np.power(lambda_ * y, 2)))

    if band_limit:
        x_limit = 1 / np.sqrt(np.power(2 * 1 / width / pitch * z, 2) + 1) / lambda_
        y_limit = 1 / np.sqrt(np.power(2 * 1 / height / pitch * z, 2) + 1) / lambda_
        trans[np.abs(x) > x_limit] = 0
        trans[np.abs(y) > y_limit] = 0


    final = fftshift(ifft2(fftshift(trans * fftshift(fft2(fftshift(pad_img))))))
    if cut:
        final = final[height//2-h//2:height//2+h//2, width//2-w//2:width//2+w//2]

    return final


def asm_shift(input_image, z, pitch, lambda_, mu=1, cut=True, direction="forward", band_limit=True, shift=True):
    input_image = np.array(input_image)
    h, w = input_image.shape
    height, width = h * mu, w * mu
    u0 = 1 / width / pitch
    v0 = 1 / height / pitch

    pad_img = np.zeros((height, width))
    yy = v0 * np.array(range(-height // 2, height // 2))
    xx = u0 * np.array(range(-width // 2, width // 2))
    x, y = np.meshgrid(xx, yy)

    pad_img[height // 2 - h // 2:height // 2 + h // 2, width // 2 - w // 2:width // 2 + w // 2] = input_image
    if direction == "forward":
        trans = np.exp(1j * 2 * np.pi / lambda_ * z * np.sqrt(1 - np.power(lambda_ * x, 2) - np.power(lambda_ * y, 2)))
    else:
        trans = np.exp(-1j * 2 * np.pi / lambda_ * z * np.sqrt(1 - np.power(lambda_ * x, 2) - np.power(lambda_ * y, 2)))

    if band_limit:
        x_limit = 1 / np.sqrt(np.power(2 * 1 / width / pitch * z, 2) + 1) / lambda_
        y_limit = 1 / np.sqrt(np.power(2 * 1 / height / pitch * z, 2) + 1) / lambda_
        trans[np.abs(x) > x_limit] = 0
        trans[np.abs(y) > y_limit] = 0


    if shift:
        final = ifft2(trans * fftshift(fft2(pad_img)))
    else:
        final = ifft2(trans * fft2(pad_img))

    if cut:
        final = final[height // 2 - h // 2:height // 2 + h // 2, width // 2 - w // 2:width // 2 + w // 2]

    return final


if __name__ == "__main__":
    p = np.zeros((1024, 1024))
    p[256:768, 256:768] = 1

    # image_path = "../../Res/Set5/GTmod12/butterfly.png"
    # p = Image.open(image_path, mode="r")
    # # convert RGB image to Gray image
    # p = p.convert("L")

    plt.figure(1)
    plt.imshow(p, cmap="gray")

    pitch = 8 * pow(10, -3)
    z = pitch * 1024 * 200
    lambda_ = 638 * pow(10, -6)

    final = asm(p, z, pitch, lambda_, band_limit=False)
    final_limit = asm(p, z, pitch, lambda_, band_limit=True)

    final_show = np.abs(final)
    final_show /= np.max(final_show)
    final_show = format_img(final_show)
    plt.figure(2)
    plt.imshow(final_show, cmap="gray")

    final_limit_show = np.abs(final_limit)
    final_limit_show /= np.max(final_limit_show)
    plt.figure(3)
    plt.imshow(final_limit_show, cmap="gray")
    plt.show()




