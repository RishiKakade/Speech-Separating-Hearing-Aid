import itertools

import numpy as np

NUM_SPEAKERS = 4
MIN_ANGULAR_DISTANCE_FOR_NEW_SPEAKER = 30


def angular_diff(a: float, b: float) -> float:
    """
    More like a cost function over which we are optimizing
    """
    if (a is None) and (b is None):
        return 0
    elif (a is None) or (b is None):
        return 360  # Return max distance if one didn't exist

    angular_distance = 180.0 - abs((abs(a - b) % 360.0) - 180.0)
    if angular_distance > MIN_ANGULAR_DISTANCE_FOR_NEW_SPEAKER:
        return 360
    else:
        return angular_distance


def remap_voice_angles(old: np.array, new: np.array) -> np.array:
    old = np.array(old)
    new = np.array(new)
    diff = np.zeros((old.shape[0], new.shape[0]))
    for i, iv in enumerate(old):
        for j, jv in enumerate(new):
            diff[i][j] = angular_diff(iv, jv)

    costs = diff ** 2
    min_cost = np.Inf
    min_cost_indices = tuple(range(NUM_SPEAKERS))
    for indices in itertools.permutations(range(NUM_SPEAKERS)):
        cost = 0
        for col in range(NUM_SPEAKERS):
            cost += costs[col][indices[col]]
        if cost < min_cost:
            min_cost = cost
            min_cost_indices = indices
    # print("Min Cost Indices:", min_cost_indices)
    new_mapping = new[np.array(min_cost_indices)]
    for i in range(NUM_SPEAKERS):
        if new_mapping[i] is None:
            new_mapping[i] = old[i]

    return new_mapping, min_cost_indices


if __name__ == '__main__':
    old = np.array([1, 45, 270, None])
    new = np.array([57, None, 2, -95])

    print("Old", old)
    print("New", new)
    print("Difference:")
    colours = remap_voice_angles(old, new)
    print("Indices (colors) of new array", colours)

    old = np.array([1, 279, 100, 101])
    new = np.array([1, 99, 98, None])
    print("Old", old)
    print("New", new)
    colours = remap_voice_angles(old, new)
    print("Indices (colors) of new array", colours)

    print()
    print()
    old = np.array([1, 279, 100, 101, None, None])
    new = np.array([1, 99, 98, None, -90, None])
    NUM_SPEAKERS = 6
    print("Old", old)
    print("New", new)
    colours = remap_voice_angles(old, new)
    print("Indices (colors) of new array", colours)
