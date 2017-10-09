import numpy as np

def Lyapunov(u, v, lat, dlat, dlon):
    '''
    Calculate Lyapunov exponent
    
    u, v: 2D array of wind
    lat: 1D array of latitude, for estimating grid size
    dlat, dlon: scalar
    '''
    s_lat = 110.574e3 * dlat
    s_lon = 111.320e3 * np.cos(lat/180*np.pi) * dlon
    du = (np.roll(u,1,axis=-1)-np.roll(u,-1,axis=-1))
    dv = (np.roll(v,1,axis=-2)-np.roll(v,1,axis=-2))
    L = (np.abs(du)+np.abs(dv))/(s_lon+s_lat)[:,np.newaxis]
    return L