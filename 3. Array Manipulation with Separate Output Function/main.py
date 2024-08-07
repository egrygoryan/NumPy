import numpy as np

def transpose(array):
    return np.transpose(array)

def reshape(array, shape:tuple):
    return np.reshape(array, shape)

def split(array, chunks, axis):
    return np.array_split(array, chunks, axis)

def combine(arrays: tuple, axis):
    return np.concatenate(arrays, axis)

def print_array(dest_arr, msg="Transformed arr"):
    print(f"{msg}: {dest_arr}\n")

def main():
    # create arr
    rng = np.random.default_rng()
    array = rng.integers(low=1, high=5, size=(6,6))
    print_array(array, 'Init state')

    # transpose
    transposed = transpose(array)
    print_array(transposed, 'transposed')

    # reshape
    reshaped = reshape(array, (3, 12))
    print_array(reshaped, 'reshaped to 3 x 12')

    # split into 2 chunks by cols
    splitted = split(reshaped, chunks=2, axis=1)
    print_array(splitted[0], 'first chunk')
    print_array(splitted[1], 'second chunk')

    # stack one arr onto another
    combined= combine(splitted, axis=0)
    print_array(combined, 'combined')

    # Assertions for verification
    assert transposed.shape == (6, 6), 'Transposed shape doesnt match to expected'
    assert reshaped.shape == (3, 12), 'Invalid reshaped array'
    assert combined.shape == (6, 6), 'Combined shape doesnt match to expected'
    assert len(splitted) == 2, 'Invalid number of chunks'

if __name__ == '__main__':
    main()