import datetime as dt  # Python standard library datetime  module
import numpy as np
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import matplotlib.pyplot as plt

# from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid

_dir = "E:/data/wam/2015/"
nc_filename = "E:/data/wam/2015/wam_t1.nc"

nc_fid = Dataset(nc_filename, 'r')

lon_size = nc_fid.dimensions['LONGITUDE']
lat_size = nc_fid.dimensions['LATITUDE']
time_size = nc_fid.dimensions['TIME']

variables_shape = nc_fid.variables['HS'].shape

hs_data = nc_fid.variables['HS']

points = [(0.870513, 3.26071), (2.97327, 4.09434), (0.443304,
                                                    5.80299), (1.70339, 8.73356), (2.97425, 4.09276), (-0.333543,
                                                                                                       4.90165),
          (-0.0688949, 2.9334), (-0.90427, 1.52768), (-4.36736,
                                                      2.74788), (-3.80912, -1.11971), (-3.12773, -0.995164)]

buoys = {}
buoys["Northern Baltic Proper"] = (0.870513, 3.26071)
buoys["Gulf of Finland"] = (2.97327, 4.09434)
buoys["Bothnian Sea"] = (0.443304, 5.80299)
buoys["Bay of Bothnia"] = (1.70339, 8.73356)
buoys["Helsinki"] = (2.97425, 4.09276)
buoys["Finngrundet"] = (-0.333543, 4.90165)
buoys["Huvudskär Ost"] = (-0.0688949, 2.9334)
buoys["Knolls Grund"] = (-0.90427, 1.52768)
buoys["Väderöarna"] = (-4.36736, 2.74788)
buoys["Darss Sill"] = (-3.80912, -1.11971)
buoys["Arkona"] = (-3.12773, -0.995164)

dlon = 0.08270216
dlat = 0.082758665

lon = np.arange(-5.6666665, 5.17, dlon)
lat = np.arange(-2, 9.93, dlat)


def get_surrounding_points(_val, _data):
    for _i in range(len(_data)):
        if _data[_i] > _val:
            return _i - 1, _i


def get_neighbouring_points(_tuple, _lon, _lat):
    lon1_ind, lon2_ind = get_surrounding_points(_tuple[0], _lon)
    lat1_ind, lat2_ind = get_surrounding_points(_tuple[1], _lat)
    return [lon1_ind, lon2_ind], [lat1_ind, lat2_ind]


def get_distance(_p1, _p2):
    return np.math.sqrt((_p1[0] - _p2[0]) ** 2 + (_p1[1] - _p2[1]) ** 2)


def get_avg_value(_point, _lon_ind, _lat_ind, _data, _lon, _lat):
    _p1_ind = _lat_ind[0], _lon_ind[0]
    _p2_ind = _lat_ind[0], _lon_ind[1]
    _p3_ind = _lat_ind[1], _lon_ind[1]
    _p4_ind = _lat_ind[1], _lon_ind[0]
    _p1 = (_lon[_lon_ind[0]], _lat[_lat_ind[0]])
    _p2 = (_lon[_lon_ind[1]], _lat[_lat_ind[0]])
    _p3 = (_lon[_lon_ind[1]], _lat[_lat_ind[1]])
    _p4 = (_lon[_lon_ind[0]], _lat[_lat_ind[1]])
    _v1 = _data[_p1_ind]
    _v2 = _data[_p2_ind]
    _v3 = _data[_p3_ind]
    _v4 = _data[_p4_ind]
    _normal = (_v1 + _v2 + _v3 + _v4) / 4
    _d1 = get_distance(_point, _p1)
    _d2 = get_distance(_point, _p2)
    _d3 = get_distance(_point, _p3)
    _d4 = get_distance(_point, _p4)
    _w1 = (1/_d1)/(1/_d1+1/_d2+1/_d3+1/_d4)
    _w2 = (1/_d2)/(1/_d1+1/_d2+1/_d3+1/_d4)
    _w3 = (1/_d3)/(1/_d1+1/_d2+1/_d3+1/_d4)
    _w4 = (1/_d4)/(1/_d1+1/_d2+1/_d3+1/_d4)
    _weighted_mean = (_w1 * _v1 + _w2 * _v2 + _w3 * _v3 + _w4 * _v4)/(_w1+_w2+_w3+_w4)

    return _weighted_mean


def plot_buoy_data(_name, _point, _lon, _lat):
    _values = []
    lon_ind, lat_ind = get_neighbouring_points(_point, lon, lat)
    for _hs_field in hs_data:
        _values.append(get_avg_value(_point, lon_ind, lat_ind, _hs_field, _lon, _lat))

    plt.plot(_values, label=_name)
    plt.legend(bbox_to_anchor=(.2, .95), loc='upper center', borderaxespad=0.)
    plt.savefig(_dir+_name)
    plt.clf()


for name, point in buoys.items():
    plot_buoy_data(name, point, lon, lat)

# lon_ind, lat_ind = get_neighbouring_points((0.870513, 3.26071), lon, lat)
#
# i = 0
# _values = []
# for _hs_field in hs_data:
#     _values.append(get_avg_value((0.870513, 3.26071), lon_ind, lat_ind, _hs_field, lon, lat))
#
# plt.plot(range(len(_values)), _values)
# plt.show()

# lats = nc_fid.variables['lat'][:]  # extract/copy the data
# lons = nc_fid.variables['lon'][:]
# time = nc_fid.variables['time'][:]
# air = nc_fid.variables['air'][:]  # shape is time, lat, lon as shown above

i = 1
