import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class Kinoform:

    def __init__(self):
        self.pix = 0.0064
        self.lambda_ = 0.532e-3  
        self.d = 1200

    def padding(self, g):
        H, W = g.shape
        m = max(H,W)
        a = int(np.log2(m)+2)
        A = 2**a
        t = np.zeros((A,A))
        t[int(A/2-H/2) : int(A/2+H/2), int(A/2-W/2) : int(A/2+W/2)] = g[:,:]
        t = t/np.max(t)
        return t
    
    def fresnel_object_to_slm(self, g):
        H, W = g.shape

        # kinoform : SLH으로 위상 변화시키는거라 픽셀크기 픽스시켜주는거
        Lx = H * self.pix
        Ly = W * self.pix
        dx = self.pix
        dy = self.pix
        x = dx * np.array(range(-int(H/2), +int(H/2)))
        y = dy * np.array(range(-int(W/2), +int(W/2)))
        Y, X = np.meshgrid(y, x)

        Lx0 = self.lambda_ * self.d / dx
        Ly0 = self.lambda_ * self.d / dy
        dxs = Lx0 / H
        dys = Ly0 / W
        xs = dxs * np.array(range(-int(H/2),+int(H/2)))
        ys = dys * np.array(range(-int(W/2),+int(W/2)))
        Ys, Xs = np.meshgrid(ys, xs)

        # random noise
        g = g * 2 * np.pi * np.random.rand(H, W)
        
        g = g * np.exp(1j * np.pi / self.lambda_ / self.d * (Xs**2 + Ys**2))

        g = np.fft.fftshift(g)
        g = np.fft.fft2(g)
        g = np.fft.fftshift(g)

        g = g * (1 / 1j / self.lambda_ / self.d) * np.exp(1j * 2 * np.pi * self.d / self.lambda_) \
            * np.exp(1j * np.pi / self.lambda_ / self.d * (X**2 +Y**2))
        
        # regularization
        # g = g / np.max(np.abs(g))
        return g        
    
    def kinoform(self, g):
        return np.angle(g)
        
    def reconstruct(self, kino):
        U0 = np.cos(kino - np.pi) + 1j * np.sin(kino - np.pi)

        H, W = kino.shape
        # kinoform : SLH으로 위상 변화시키는거라 픽셀크기 픽스시켜주는거
        Lx = H * self.pix
        Ly = W * self.pix
        dx = self.pix
        dy = self.pix
        x = dx * np.array(range(-int(H/2), +int(H/2)))
        y = dy * np.array(range(-int(W/2), +int(W/2)))
        Y, X = np.meshgrid(y, x)

        Lx0 = self.lambda_ * self.d / dx
        Ly0 = self.lambda_ * self.d / dy
        dxs = Lx0 / H
        dys = Ly0 / W
        xs = dxs * np.array(range(-int(H/2),+int(H/2)))
        ys = dys * np.array(range(-int(W/2),+int(W/2)))
        Ys, Xs = np.meshgrid(ys, xs)

        U0 = U0 * np.exp(-1j * np.pi / self.lambda_ / self.d * (X**2 + Y**2))
        
        U0 = np.fft.ifft2(U0)
        U0 = np.fft.ifftshift(U0)

        U0 = U0 * (-1 / 1j / self.lambda_ / self.d) * np.exp(-1j * 2 * np.pi / self.lambda_ / self.d) \
                * np.exp(-1j * np.pi / self.lambda_ / self.d * (Xs**2 + Ys**2))
        
        return U0

if __name__ == '__main__':
    img_path = "C:\Lab\CGH\Computer-Generated-Hologram\Images\goose.jpg"

    img = Image.open(img_path)
    img = img.convert('L')
    g = np.array(img)

    k = Kinoform()
    g = k.padding(g)
    g = k.fresnel_object_to_slm(g)
    kino = k.kinoform(g)
    
    g = k.reconstruct(kino)
    g = g / np.max(g) * 255

    
    plt.figure(1)
    plt.imshow(kino, 'gray')
    plt.title('kinoform')

    plt.figure(2)
    plt.imshow(np.abs(g), 'gray')
    plt.title('reconstructed image')

    plt.show()