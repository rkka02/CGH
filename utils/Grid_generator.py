import numpy as np

class Grid_generator:

    def generate_grid(shape, sampling_interval):
        H, W = shape
        dx, dy = sampling_interval
        x = dx * np.array(range(-W//2, +W//2))
        y = -dy * np.array(range(-H//2, +H//2))

        Y, X = np.meshgrid(y, x)
        return Y, X