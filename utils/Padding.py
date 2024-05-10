import numpy as np

class Padding:

    def padding(image_array, exponent_increment=1, regularization=True):
        H, W = image_array.shape
        m = max(H,W)
        exponent = int(np.log2(m) + exponent_increment)
        window_size = 2**exponent
        t = np.zeros((window_size, window_size))
        t[int((window_size-H)/2) : int((window_size+H)/2), int((window_size-W)/2) : int((window_size+W)/2)] = image_array[:,:]
        
        if regularization == True:
            t = t/np.max(t)
            
        return t