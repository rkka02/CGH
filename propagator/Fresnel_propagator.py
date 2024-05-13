import numpy as np
from utils.Grid_generator import Grid_generator

class Fresnel_propagator:
    def propagate(image, from_sampling_interval, lambda_=633e-9, d=1, random_noise=False, regularization=True):
        H, W = image.shape

        dy_from, dx_from = from_sampling_interval

        dx_to = lambda_ * d / W / dx_from
        dy_to = lambda_ * d / H / dy_from

        Y_from, X_from = Grid_generator.generate_grid((H, W), (dy_from, dx_from))
        Y_to, X_to = Grid_generator.generate_grid((H, W), (dy_to, dx_to))
        
        # random noise
        if random_noise:
            image = image * 2 * np.pi * np.random.rand(H, W)
        
        image = image * np.exp(1j * np.pi / lambda_ / d * (X_from**2 + Y_from**2))

        image = np.fft.fftshift(image)
        image = np.fft.fft2(image)
        image = np.fft.fftshift(image)

        image = image * (1 / 1j / lambda_ / d) * np.exp(1j * 2 * np.pi * d / lambda_) \
            * np.exp(1j * np.pi / lambda_ / d * (X_to**2 +Y_to**2))
        
        # regularization
        if regularization == True:
            imax = np.max(np.abs(image))
            imin = np.min(np.abs(image))
            image = 2 * image / (imax - imin)
            
        return image