import numpy as np

# for brevity function also contain an axis as a param

def save_to(array, filename):
    ext = filename.split('.')[-1]
    
    if ext == 'txt':
        np.savetxt(filename, array, fmt='%d')
    elif ext == 'csv':
        np.savetxt(filename, array, delimiter=',', fmt='%d')
    elif ext in ['npy', 'npz']:
        np.save(filename, array)
    else:
        raise ValueError(f"Invalid file format {ext}. Use 'txt', 'csv', 'npy', or 'npz' instead.")

def load_from(filename, dtype=int):
    ext = filename.split('.')[-1]
    
    if ext == 'txt':
        return np.loadtxt(filename, dtype)
    elif ext == 'csv':
        return np.loadtxt(filename, dtype, delimiter=',')
    elif ext in ['npy', 'npz']:
        return np.load(filename)
    else:
        raise ValueError(f"Invalid file format {ext}. Use 'txt', 'csv', 'npy', or 'npz' instead.")
    
def sum(array, axis=None):
    return np.sum(array, axis)

def mean(array, axis=None):
    return np.mean(array, axis)

def median(array, axis=None):
    return np.median(array, axis)

def std(array, axis=None):
    return np.std(array, axis)

def print_array(dest_arr, source_arr=None, msg="Transformed arr"):
    if source_arr is not None:
        print(f"Original arr: {source_arr}\n")
    print(f"{msg}: {dest_arr}\n")

def main():
    # create array
    rng = np.random.default_rng()
    array = rng.integers(low=1, high=11, size=(5,5))
    
    # save arr into different formats
    save_to(array, 'output.txt')
    save_to(array, 'output.csv')
    save_to(array, 'output.npy')

    # load arr from different formats
    txt = load_from('output.txt')
    csv = load_from('output.csv')
    npy = load_from('output.npy')

    # print loaded arrays
    print_array(txt, source_arr=array, msg="arr from txt")
    print_array(csv, source_arr=array, msg="arr from csv")
    print_array(npy, source_arr=array, msg="arr from npy")

    # assert arrays are the same
    assert np.array_equal(array, txt), "Txt doesn't match to source arr"
    assert np.array_equal(array, csv), "CSV doesn't match to source arr"
    assert np.array_equal(array, npy), "Binary doesn't match to source arr"

    # calculate agg. func
    arr_sum = sum(array)
    arr_mean = mean(array)
    arr_median_axis0 = median(array, axis=0)
    arr_std_axis1 = std(array, axis=1)

    # print results
    print_array(dest_arr=arr_sum, msg="Sum of arr")
    print_array(dest_arr=arr_mean, msg="Mean of arr")
    print_array(dest_arr=arr_median_axis0, msg="Median for cols")
    print_array(dest_arr=arr_std_axis1, msg="Std for rows")

    #assert agg func are the same
    assert arr_sum == np.sum(csv), "Sum doesn't match"
    assert arr_mean == np.mean(npy), "Mean doesn't match"
    assert np.array_equal(arr_median_axis0, np.median(txt, axis=0)), "Median doesn't match"
    assert np.array_equal(arr_std_axis1, np.std(csv, axis=1)), "STD doesn't match"


if __name__ == '__main__':
    main()