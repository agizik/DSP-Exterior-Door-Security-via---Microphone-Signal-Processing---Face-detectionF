import numpy as np
from numpy.fft import fft, ifft, fft2, ifft2, fftshift, rfft
 
def cross_correlation_using_fft(x, y):
    f1 = fft(x)
    f2 = fft(np.flipud(y))
    cc = np.real(ifft(f1 * f2))
    return fftshift(cc)

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return (x)


def normalize( input_block ):    
    in_abs = np.abs(input_block)
    normilized = input_block/np.max(in_abs)        
    return (normilized)

def dft(normilized , BLOCKLEN):    
    sfft = rfft(normilized , BLOCKLEN)
    return (sfft)

def where(len_have , len_lookingfor, order):    
    true_order = int(order*len_lookingfor/len_have)
    return (true_order)

