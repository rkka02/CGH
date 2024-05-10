import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class Fresnel:

    def __init__(self):
        pass

    def padding(self, g):
        H, W = g.shape
        m = max(H,W)
        a = int(np.log2(m)+3)
        A = 2**a
        t = np.zeros((A,A))
        t[int(A/2-H/2) : int(A/2+H/2), int(A/2-W/2) : int(A/2+W/2)] = g[:,:]
        t = t/np.max(t)
        return t

    def fresnel(self, g, lambda_=633e-9, d=1):
        H, W = g.shape
        dxs = np.sqrt(lambda_ * d / H)
        dys = np.sqrt(lambda_ * d / W)
        xs = dxs * np.array(range(-int(H/2),+int(H/2)))
        ys = dys * np.array(range(-int(W/2),+int(W/2)))
        Ys, Xs = np.meshgrid(ys, xs)
        
        dx, dy = dxs, dys
        x, y = xs, ys
        Y, X = np.meshgrid(y, x)

        # random noise
        g = g * 2 * np.pi * np.random.rand(H, W)
        
        g = g * np.exp(1j * np.pi / lambda_ / d * (Xs**2 + Ys**2))

        g = np.fft.fftshift(g)
        g = np.fft.fft2(g)
        g = np.fft.fftshift(g)

        g = g * (1 / 1j / lambda_ / d) * np.exp(1j * 2 * np.pi * d / lambda_) \
            * np.exp(1j * np.pi / lambda_ / d * (X**2 +Y**2))
        
        # regularization
        g = g / np.max(np.abs(g))
        return g
        
    def plane_wave(self, g, theta=0, lambda_=633e-9, d=1):
        H, W = g.shape
        dx = np.sqrt(lambda_ * d / H)
        dy = np.sqrt(lambda_ * d / W)
        x = dx * np.array(range(-int(H/2),+int(H/2)))
        y = dy * np.array(range(-int(W/2),+int(W/2)))
        Y, X = np.meshgrid(y, x)
        
        return np.exp(1j * 2 * np.pi / lambda_ * X * np.sin(theta))
    
    def spherical_wave(self, g, x_shift=0, y_shift=0, lambda_=633e-9, d=1):
        H, W = g.shape
        dx = np.sqrt(lambda_ * d / H)
        dy = np.sqrt(lambda_ * d / W)
        x = dx * np.array(range(-int(H/2),+int(H/2)))
        y = dy * np.array(range(-int(W/2),+int(W/2)))
        Y, X = np.meshgrid(y, x)

        return (1 / 1j / lambda_ / d) * np.exp(1j * np.pi / lambda_ / d * ((X-dx*x_shift)**2+(Y-dy*y_shift)**2))
        # return np.exp(1j * np.pi / lambda_ / d * ((X-dx*H*x_shift)**2+(Y-dy*H*y_shift)**2))
    
    def record(self, g, r):
        holo = np.square(np.abs(g + r))
        return holo

    def reconstruct(self, holo, p):
        holo = holo - np.mean(holo)
        rec = self.fresnel(holo * p)
        return rec

if __name__ == '__main__':
    img_path = "C:\Lab\CGH\Computer-Generated-Hologram\Images\goose.jpg"

    img = Image.open(img_path)
    img = img.convert('L')
    g = np.array(img)

    f = Fresnel()
    g = f.padding(g)
    g = f.fresnel(g)

    # record
    r = f.plane_wave(g, theta=np.pi/5)
    holo = f.record(g, r)
    # reconstruct
    p = f.plane_wave(g, theta=np.pi/5)
    recon = f.reconstruct(holo, p)

    plt.figure(1)
    plt.imshow(holo, 'gray')
    plt.title('hologram')

    plt.figure(2)
    plt.imshow(np.log(1+np.abs(np.fft.fftshift(np.fft.fft2(holo)))))
    plt.title("Fourier transform of the hologram")

    plt.figure(3)
    plt.imshow(np.abs(recon), 'gray')
    plt.title('reconstructed image')



    plt.show()