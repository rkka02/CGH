import numpy as np
from utils.Grid_generator import Grid_generator

class Wave_generator:
    def planewave(shape, sampling_interval, lambda_=633e-9, theta=0):
        H, W = shape
        dy, dx = sampling_interval
        Y, X = Grid_generator.generate_grid((H, W), (dy, dx))

        return np.exp(1j * 2 * np.pi / lambda_ * X * np.sin(theta))