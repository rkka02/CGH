from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt

# An algorithm which is used to retrieve a phase distribution of a target image.
def gs_algorithm(img, iters=30):
    
    H, W = img.shape
    # 일회성
    phase_s = np.random.rand(H,W)
    phase_f = np.ones((H,W))
    # 계속 씀
    amp_s = np.sqrt(img)
    amp_f = np.ones((H,W))

    signal_s = amp_s * np.exp(1j * phase_s)

    for i in range(iters):
        signal_f = np.fft.fft2(signal_s)
        phase_f = np.angle(signal_f)
        signal_f = amp_f * np.exp(1j * phase_f)

        signal_s = np.fft.ifft2(signal_f)
        phase_s = np.angle(signal_s)
        signal_s = amp_s * np.exp(1j * phase_s)

    return phase_f

def recover(phase):
    return np.fft.ifft2(np.exp(1j*phase))

if __name__ == '__main__':

    iters = 30

    img_path = "C:\Lab\CGH\Images\goose.jpg"
    img = Image.open(img_path)
    img = img.convert('L')
    img = np.array(img)

    phase = gs_algorithm(img, 50)

    re = recover(phase)

    plt.figure(1)
    plt.imshow(img)
    plt.title('original image')

    plt.figure(2)
    plt.imshow(phase)
    plt.title('phase mask')

    plt.figure(3)
    plt.imshow(np.abs(re))
    plt.title('recovered image')

    plt.show()