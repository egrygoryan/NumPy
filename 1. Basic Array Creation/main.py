import numpy as np

def print_array(arr, msg=None):
    print(f"{msg}\n{arr}" if msg is not None else arr)

def main():
    one_D = np.arange(1, 11, dtype="int16")

    two_D = np.arange(1,10, dtype="int16").reshape(3,3)
    
    index_3_elem= one_D[2]
    print(index_3_elem)

    slicing = two_D[:2, :2]
    print_array(slicing, "slicing first 2 rows + columns")

    addition = 5 + one_D
    print_array(addition, "adding 5 to each element of array")

    multi = 2 * two_D
    print_array(multi, "multiplication by 2 to matrix")

if __name__ == '__main__':
    main()