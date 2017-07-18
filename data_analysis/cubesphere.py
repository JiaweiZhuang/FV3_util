import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


@xr.register_dataarray_accessor('cs')
@xr.register_dataset_accessor('cs')
class CubeSphereAccessor(object):
    def __init__(self, xarray_obj):
        self._obj = xarray_obj
        self._isCS = None

    @property
    def isCS(self):
        """ Check if this object contains enough Cube-sphere information

        Parameters
        ----------

        Returns
        -------
        isCS : bool
           
        """
        if self._isCS is None:

            dims = list(self._obj.dims)
            coords = list(self._obj.coords.keys())

            # just perform some basic checking
            if "tile" not in dims:
                self._isCS = False
                print("A cube-sphere object must contain the tile dimension")
                return
            else:
                if self._obj["tile"].size != 6:
                    self._isCS = False
                    print("The size of tile dimension must be 6")
                    return

            if "lon" not in coords:
                self._isCS = False
                print("A cube-sphere object must contain coordinate variable lon")
                return

            if "lat" not in coords:
                self._isCS = False
                print("A cube-sphere object must contain coordinate variable lat")
                return

            self._isCS = True

        return self._isCS

    def plot_CSlayer(self, ax=None, vmin=None, vmax=None, transform=ccrs.PlateCarree(), cbar=True):
        assert self.isCS, "not cube-sphere data!"

        # make sure 6 tiles have the same colorbar scale
        if vmax is None:
            vmax = self._obj.max()
        if vmin is None:
            vmin = self._obj.min()
        if ax is None:
            ax = plt.axes(projection=ccrs.PlateCarree())

        # mask cells near boundaries otherwise they will span the entire map
        mask = np.abs(self._obj["lon"] - 180) >= 5
        for i in range(6):
            self._obj.where(mask).isel(tile=i).plot.pcolormesh(ax=ax, transform=transform,
                                                        x='lon', y='lat', add_colorbar=(i == 0)and(cbar),
                                                        vmin=vmin, vmax=vmax, cmap='jet')
        ax.coastlines()
        ax.set_global()

    def meridional_mean(self, dlon=5, verbose=False):
        assert self.isCS, "not cube-sphere data!"

        lon_bins = np.arange(0, 361, dlon)
        lon_center = np.arange(1, 360, dlon)
        group = self._obj.groupby_bins('lon', lon_bins, labels=lon_center)
        if verbose:
            print("Dimension of each group:", list(group)[0][1].dims)
        meri_mean = group.mean(dim="stacked_tile_y_x")
        return meri_mean

    def zonal_mean(self, dlat=4, verbose=False):
        assert self.isCS, "not cube-sphere data!"

        lat_bins = np.arange(-90, 91, dlat)
        lat_center = np.arange(-89, 90, dlat)
        group = self._obj.groupby_bins('lat', lat_bins, labels=lat_center)
        if verbose:
            print("Dimension of each group:", list(group)[0][1].dims)
        zonal_mean = group.mean(dim="stacked_tile_y_x")
        return zonal_mean


def open_FV3data(dirname, prefix, verbose=False, restart=False):
    ''' Open the output of the online GFDL-FV3 model
    All FV3 output data have the name xxx.tile1.nc ~ xxx.tile6.nc, for example
    - atmos_static.tile1.nc ~ atmos_static.tile6.nc
    - atmos_daily.tile1.nc ~ atmos_daily.tile6.nc
    "atmos_static" should always exist and contain the grid information
    
    Parameters
    ----------
    dirname : str
        The directory containing FV3 output files.
    
    prefix : str
        The prefix of FV3 output tile files. For example, "atmos_daily"
    
    verbose : bool,optional
        Print filenames or not.

    Returns
    -------
    dataset : Dataset
        The newly created dataset.
        
    '''
    ds_arr = [None]*6
    for i in range(6):
        itile = str(i+1)

        filename = prefix+".tile"+itile+".nc"
        if verbose:
            print("opening", filename, end=", ")
        ds = xr.open_dataset(dirname+filename, decode_times=False)

        filename = "atmos_static"+".tile"+itile+".nc"
        if verbose:
            print("opening", filename)
        grid = xr.open_dataset(dirname+filename, decode_times=False)
        
        if restart:
            ds.rename(dict(xaxis_1="grid_xt",
                           yaxis_1="grid_yt",
                           zaxis_1="pfull",
                           Time="time"),
                      inplace=True)

        ds["lon"] = grid["grid_lont"]
        ds["lat"] = grid["grid_latt"]
        ds["lon_b"] = grid["grid_lon"]
        ds["lat_b"] = grid["grid_lat"]
        ds.set_coords(["lon", "lat", "lon_b", "lat_b"], inplace=True)

        ds_arr[i] = ds.copy()

    # combine 6 tiles into a single object
    ds_combine = xr.concat(ds_arr, dim='tile')
    ds_combine.rename(dict(grid_xt="x", grid_yt="y", grid_x="x_b", grid_y="y_b"), inplace=True)

    return ds_combine
