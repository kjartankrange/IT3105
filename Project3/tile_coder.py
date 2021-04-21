



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
            tile = create_tiling(feature_range_tile, no_tiles, offset[j])
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
    tiling_indexes = np.linspace(start,end,tiles_per_feature+1)[1:-1] + offset #ommits the first and last value
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

from math import sqrt
def compute_offsets(feature_ranges, no_bins):
    offsets = []
    offset_step = []
    for feature_range_i in feature_ranges:
        start = feature_range_i[0]   ## assume 2_dim feature ranges
        end = feature_range_i[1]

        l = max(start-end, end-start)
        step = l/no_bins
        offset_step.append(step)
    for i in range(no_bins):
        offsets_i = []
        for j in range(len(feature_ranges)):
            offset_feature_j = offset_step[j]*i
            offsets_i.append(offset_feature_j)
        offsets.append(offsets_i)
    return offsets


def get_flat_state(feature):
    feature_ranges = [[-1.2, 0.6], [-0.07, 0.07]]
    bins = 9
    offsets = compute_offsets(feature_ranges, bins)

    number_tilings = 8
    tilings = create_tilings(feature_ranges, number_tilings, bins, offsets)

    codes = get_tile_coding(feature, tilings)
    flat_state = [item for sublist in codes for item in sublist]
    return flat_state


