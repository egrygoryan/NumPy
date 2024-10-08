import numpy as np

def generate_array(row_nums = 6):
    rng = np.random.default_rng()

    # generate rand values for matrix
    transaction_ids = np.arange(1000, 1000 + row_nums)
    user_ids = rng.integers(1, 6, row_nums)
    product_ids = rng.integers(1, 4, row_nums)
    quantities = rng.integers(0, 50, row_nums)
    prices = np.round(rng.uniform(1.00, 100.00, row_nums), 2)
    timestamps = np.arange('2024-07', row_nums, dtype='datetime64[D]')

    # used structured type instead of just array
    # had problems because of date type, while stacking got exception
    tr_type = np.dtype([
        ('transaction_id', 'i4'),
        ('user_id', 'i4'),
        ('product_id', 'i4'),
        ('quantity', 'i4'),
        ('price', 'f2'),
        ('timestamp', np.dtype('datetime64[s]'))
    ])

    # create the structured array
    transactions = np.empty(row_nums, dtype=tr_type)

    # fill the structured array with generated data
    transactions['transaction_id'] = transaction_ids
    transactions['user_id'] = user_ids
    transactions['product_id'] = product_ids
    transactions['quantity'] = quantities
    transactions['price'] = prices
    transactions['timestamp'] = timestamps

    return transactions

def total_revenue(transactions):
    return np.round(np.sum(transactions['quantity'] * transactions['price']),2)

def unique_users_num(transactions):
    return len(np.unique(transactions['user_id']))

def most_purchased_product(transactions):
    product_ids = transactions['product_id']
    quantities = transactions['quantity']
    
    # obrain unique product_id
    unique_product_ids = np.unique(product_ids)
    
    # store unique product_ids as key with initial qty as 0
    total_qty_per_product = {product_id: 0 for product_id in unique_product_ids}
    
    # iterate through each unique product
    for product_id in unique_product_ids:
        # create mask for array where we will get quantities for provided product_id
        mask = product_ids == product_id
        # apply mask and write aggregated sum of qties into key
        total_qty_per_product[product_id] = np.sum(quantities[mask])
    
    # get max qty value
    max_quantity = max(total_qty_per_product.values())
    
    # retrieve all product_ids with the maximum quantity
    # convert values into py ints
    most_purchased = [int(product_id) for product_id, qty in total_qty_per_product.items() if qty == max_quantity]
    
    return most_purchased

def prices_from_float_to_int(transactions):
    changed_type = np.dtype([
        ('transaction_id', 'i4'),
        ('user_id', 'i4'),
        ('product_id', 'i4'),
        ('quantity', 'i4'),
        ('price', 'i4'),
        ('timestamp', np.dtype('datetime64[s]'))
    ])

    updated_transactions = np.empty(transactions.shape, dtype=changed_type)

    for field in transactions.dtype.names:
        updated_transactions[field] = transactions[field].astype(int) if field == 'price' else transactions[field]

    return updated_transactions

def show_types(transactions):
    print(f'{transactions.dtype}', 'types\n')

def product_quantity_only(transactions):
    return np.array(np.column_stack((transactions['product_id'], transactions['quantity'])));

def transaction_per_user(transactions):
    # find unique users and get their count of transactions
    user_ids, transactions_count = np.unique(transactions['user_id'], return_counts=True)

    # stacking cols for convenience
    return np.column_stack((user_ids, transactions_count))

def filter_transactions(transactions, filter, field_name='quantity'):
    # generic implementation for masking functionality
    # gathers: Masked Array Function, Filter Transactions Function, User Transactions Function

    # check for the fiel presence
    if field_name not in transactions.dtype.names:
        return
    
    #create mask from custom condition which is declared in lambda
    mask = filter(transactions[field_name])

    return transactions[np.array(mask)]

def increase_all_prices(transactions, percentage):
    #update all prices
    increased_prices = transactions['price'] * (1 + percentage / 100)

    # return updated_transactions
    transactions['price'] = increased_prices
    return transactions

def revenue_comparison(transactions, start_date1, end_date1,
                       start_date2, end_date2):
    prices = transactions['price'] 
    quantities = transactions['quantity'] 
    dates = transactions['timestamp']

    revenue = prices * quantities

    mask1 = (dates >= np.datetime64(start_date1)) & (dates <= np.datetime64(end_date1))
    mask2 = (dates >= np.datetime64(start_date2)) & (dates <= np.datetime64(end_date2))
    
    #take revenue for diff range
    total_revenue1 = np.sum(revenue[mask1])
    total_revenue2 = np.sum(revenue[mask2])
    
    return total_revenue1, total_revenue2

def date_range_slicing(transactions, start_date, end_date):
    dates = transactions['timestamp']
    mask = (dates >= np.datetime64(start_date)) & (dates <= np.datetime64(end_date))

    return transactions[np.array(mask)]

def top_products(transactions, top):
    product_ids = transactions['product_id']
    quantities = transactions['quantity']
    prices = transactions['price']
    
    # revenue for a transaction
    revenues = quantities * prices
    
    # obtain unique product_id
    unique_product_ids = np.unique(product_ids)
    
    # calculate total revenue per product
    total_revenue_per_product = {}
    for product_id in unique_product_ids:
        mask = product_ids == product_id
        total_revenue_per_product[product_id] = np.sum(revenues[mask])
    
    # sort products by their revenues desc
    sorted_product_ids = sorted(total_revenue_per_product.keys(), key=lambda x: total_revenue_per_product[x], reverse=True)

    # take top x product IDs
    top_product_ids = sorted_product_ids[:top]
    
    # check if top products are in product_id column
    # i didn't come up with an idea, how to show in desc order 
    # sometimes isin() just takes range and isn't strict to provided values
    mask_top_products = np.isin(product_ids, top_product_ids)
    
    # apply mask to transactions
    return transactions[mask_top_products][::-1]

def print_array(arr, msg="Transformed transactions"):
    print(f"{msg}\n{arr}\n")


def main():
    # used 6 rows for brevity
    array = generate_array(6)
    print_array(array, "initial")

    total = total_revenue(array)
    print(f'{total}\n , total revenue')
    assert total > 0, "Invalid total calculation"

    unique_users = unique_users_num(array)
    print_array(unique_users, "unique users")
    assert unique_users > 0, "Users can't be absent"

    most_purchased = most_purchased_product(array)
    print_array(most_purchased, "Most purchased product Id")

    # used hardcoded 3 for brevity
    # can be applied any value for related shape
    top_products_id = top_products(array, top=3)
    print_array(top_products_id, "transactions of the top X products by revenue")

    show_types(array)

    cast_types = prices_from_float_to_int(array)
    print_array(cast_types, "casted float to int")

    price_quant_arr =  product_quantity_only(array)
    print_array(price_quant_arr, "only prices and q-ties")
    assert price_quant_arr.shape[1] == 2, "Invalid shape of price_quantity arr"

    all_users_transactions = transaction_per_user(array)
    print_array(all_users_transactions, "transactions for all users")
    assert all_users_transactions.shape > (0,0), "Transactions can't be absent"

    qty_equals_0 = filter_transactions(array, lambda x: x == 0)
    print_array(qty_equals_0, 'transactions with qty == 0')

    increased_prices = increase_all_prices(array, 20)
    print_array(increased_prices, "increased by 20%")

    qty_greater_1 = filter_transactions(array, lambda x: x > 1)
    print_array(qty_greater_1, "transactions with qty > 1")

    #date range for comparison
    start_date1 = '2024-07-01'
    end_date1 = '2024-07-02'
    start_date2 = '2024-07-03'
    end_date2 = '2024-07-04'
    compare_revenue = revenue_comparison(array, start_date1, end_date1, start_date2, end_date2)
    print(f'{compare_revenue}\n')

    user_transactions = filter_transactions(array, filter=lambda x: x == 1, field_name='user_id')
    print_array(user_transactions, "transactions for user, hardcoded first user")

    sliced_dates = date_range_slicing(array, start_date2, end_date2)
    print_array(sliced_dates, "only transactions within certain date range")

if __name__ == '__main__':
    main()