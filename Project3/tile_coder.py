



import numpy as np


def create_tilings(feature_range, number_of_tilings, tiles_per_tiling, offsets):
    """
    :param feature_range: on form [[x_start,x_end],[v_start,v_end]] for our feature (point)
    :param number_of_tilings: on form size. is the number of tiles to create
    :param tiles_per_tiling: on form size for our feature
    :param offsets: on form [offset, offset] for each tile
    :return: np array of tilings. WARNING: feature range must be one dimension only.
    """
    tilings = []
    for i in range(number_of_tilings):
        no_tiles = tiles_per_tiling
        offset = offsets[i]
        tiles = []
        for j in range(len(feature_range)):
            feature_range_tile = feature_range[j]
            tile = create_tiling(feature_range_tile, no_tiles, offset)
            tiles.append(tile)
        tilings.append(tiles)
    return np.array(tilings)






def create_tiling(feature_range, tiles_per_feature, offset):
    """

    :param feature_range: assumes array of shape [start, end]
    :param tiles_per_feature:
    :param offsets:
    :return: tiling for one feature
    """
    start = feature_range[0]
    end = feature_range[1]
    tiling_indexes = np.linspace(start,end,tiles_per_feature)[1:-1] + offset #ommits the first and last value
    return tiling_indexes

def get_tile_coding(feature, tilings):
    dims = len(feature)
    feature_codings = []
    for tiling in tilings:
        coding = []
        for i in range(dims):
            feat_i = feature[i]
            tiling_i = tiling[i]
            coding_i = np.digitize(feat_i, tiling_i)
            coding.append(coding_i)
        feature_codings.append(coding)
    return np.array(feature_codings)





feature = [0.2,1]

feature_ranges = [[0,1],[0.,1]]
number_tilings = 3
bins = 10
offsets = [0,0.2,0.4]

tilings = create_tilings(feature_ranges, number_tilings, bins, offsets)


coding = get_tile_coding(feature, tilings)

print(coding)
