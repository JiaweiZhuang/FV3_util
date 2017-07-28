import numpy as np
import pandas as pd
import xarray as xr
from collections import OrderedDict

def extract(logfile, var_list, thin=48, pos=3):
    """
    logfile: str
    
    var_list: a list of variable names
    
    thin: should thin more at shorter time step
          48 = one value per day at C48
    
    pos: 3 = the maximum value (the 4-th word in a line)
         6 = the minimum value (the 7-th word in a line)
    """
        
    # Data are hold as ordered dictionary
    # key - values are
    # 'plume01' - a list of max/min value timeseries
    # 'plume02' - a list ...
    data_dict = OrderedDict()
    for varname in var_list:
        data_dict[varname]=[]
    
    # scan by line
    with open(logfile, 'r') as fi:        
        for ln in fi:
            for varname in var_list:
                # to be safe, match 2 patterns
                if varname in ln and 'max =' in ln:
                    # get the pos+1-th word
                    data_dict[varname].append(ln.split()[pos]) 
                
    # thin the data and convert to numpy array 
    for varname in var_list:
        data_dict[varname] = np.array(data_dict[varname][::thin],
                                      dtype=np.float32)
                    
    # convert the dict from extract() to one-dimenisional DataSet
    ds = pd.DataFrame.from_dict(data_dict).to_xarray().\
         rename(dict(index='time'),inplace=True)
    
    return ds


def extract_Vs(maindir, var_list, Hres, Vres_list, thin=48, pos=3, suffix='_std.log'):
    """
    Process logfiles from different vertical resolutions
    """

    ds_Vs_arr = [] # list if timeseries at vertical different resolutions

    print('\n open:', end=' ')
    for Vres in Vres_list:
        logfile = 'C{0}L{1}'.format(Hres,Vres)+suffix
        print(logfile, end=' ')
        ds_Vs_arr.append( extract(maindir+logfile, var_list,
                                  thin=thin, pos=pos) )

    ds_Vs = xr.concat(ds_Vs_arr, dim='Vres')
    ds_Vs["Vres"]=np.array(Vres_list)
    return ds_Vs


def extract_HsVs(maindir, var_list, Hres_list, Vres_list, 
                 thin_base=48, pos=3, suffix='_std.log'):
    """
    Process logfiles from different horizontal and vertical resolutions
    """

    ds_HsVs_arr = [] # list of timeseries at different horizontal and vertical resolutions

    for Hres in Hres_list:
        
        # thin more at higher horizontal resolutiom (more time steps)
        ds_HsVs_arr.append( extract_Vs(maindir, var_list, Hres, Vres_list ,
                                       thin=np.int(thin_base*Hres/48),
                                       pos=pos,suffix=suffix
                                      ) 
                          )

    ds_HsVs = xr.concat(ds_HsVs_arr, dim='Hres')
    ds_HsVs["Hres"]=np.array(Hres_list)
    
    return ds_HsVs