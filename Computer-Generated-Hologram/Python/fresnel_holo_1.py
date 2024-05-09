import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class Fresnel:

    def __init__(self):
        pass

    def padding(self, g):
        M, N = g.shape
        m = max(M,N)
        a = int(np.log2(m)+1)
        A = 2**a
        t = np.zeros((A,A))
        t[int(A/2-M/2) : int(A/2+M/2), int(A/2-N/2) : int(A/2+N/2)] = g[:,:]
        t = t/np.max(t)
        return t

    def fresnel(self, g, lambda_=1e-9, d=1):
        M, N = g.shape
        dxs = np.sqrt(lambda_ * d / M)
        dys = np.sqrt(lambda_ * d / N)
        xs = dxs * np.array(range(-int(M/2),+int(M/2)))
        ys = dys * np.array(range(-int(N/2),+int(N/2)))
        Ys, Xs = np.meshgrid(ys, xs)
        
        dx, dy = dxs, dys
        x, y = xs, ys
        Y, X = np.meshgrid(y, x)

        # random noise
        g = g * 2 * np.pi * np.random.rand(M, N)
        
        g = g * np.exp(1j * np.pi / lambda_ / d * (Xs**2 + Ys**2))

        g = np.fft.fftshift(g)
        g = np.fft.fft2(g)
        g = np.fft.fftshift(g)

        g = g * (1 / 1j / lambda_ / d) * np.exp(1j * 2 * np.pi * d / lambda_) \
            * np.exp(1j * np.pi / lambda_ / d * (X**2 +Y**2))
        
        # regularization
        g = g / np.max(np.abs(g))
        return g
        
    def plane_wave(self, g, theta=np.pi/18, lambda_=1e-9, d=1):
        M, N = g.shape
        dx = np.sqrt(lambda_ * d / M)
        dy = np.sqrt(lambda_ * d / N)
        x = dx * np.array(range(-int(M/2),+int(M/2)))
        y = dy * np.array(range(-int(N/2),+int(N/2)))
        Y, X = np.meshgrid(y, x)
        
        return np.exp(1j * 2 * np.pi / lambda_ * X * np.sin(theta))

    def record(self, g, r):
        holo = np.square(np.abs(g + r))
        return holo

    def reconstruct(self, holo, p):
        holo = holo - np.mean(holo)
        rec = self.fresnel(holo * p)
        return rec

if __name__ == '__main__':
    img_path = "/Users/makisbea/Labs/Computer-Generated-Hologram/Images/rikka.png"

    img = Image.open(img_path)
    img = img.convert('L')
    g = np.array(img)

    f = Fresnel()
    g = f.padding(g)
    g = f.fresnel(g)

    # record
    r = f.plane_wave(g, theta=np.pi/10)
    holo = f.record(g, r)
    # reconstruct
    p = f.plane_wave(g, theta=-np.pi/10)
    recon = f.reconstruct(holo, p)

    plt.figure(1)
    plt.imshow(np.abs(recon), 'gray')
    plt.show()