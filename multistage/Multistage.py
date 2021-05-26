import itertools
import pandas as pd

SUPPORT_S = 2


def get_data():
    df = pd.read_csv('online_retail.csv', sep=';', nrows=1000)
    df: pd.DataFrame = df[df['CustomerID'].notna()]
    return df


def get_index_from_dict(dictionary):
    return len(dictionary.keys())+1


df = get_data()

stock_dictionary = {}
# stock_dictionary = {
#     'id': 1,
#     'stock': '10AA',
#     'count': 3
# }
customer_dictionary = {}
# customer_dictionary = {
#     'stocks':['stock'],
#     'combinations':[]
# }

# PASS #1
for index, row in df.iterrows():
    customer = int(row['CustomerID'])
    stock = row['StockCode']

    if customer not in customer_dictionary:
        customer_dictionary[customer] = set()
    customer_dictionary[customer].add(stock)

    if stock not in stock_dictionary:
        stock_dictionary[stock] = {
            'id': get_index_from_dict(stock_dictionary),
            'stock': stock,
            'count': 0
        }
    stock_dictionary[stock]['count'] += 1


# PASS #2
combination_dictionary = {}
# combination_dictionary = {
#     'combination': (1, 3),
#     'count': 2,
#     'hash1': 5,
#     'hash2': 6
# }

hash1_dict = {}
# hash1_dict = {
#     'subsets': set(),
#     'count':0
# }
hash2_dict = {}

for stocks in customer_dictionary.values():
    for subset in itertools.combinations(stocks, 2):
        if subset not in combination_dictionary:
            try:
                combination_dictionary[subset] = {
                    'combination': subset,
                    'count': 0,
                    'hash1': (stock_dictionary[subset[0]]['id'] + stock_dictionary[subset[1]]['id']) % len(
                        stock_dictionary.keys()),
                    'hash2': (stock_dictionary[subset[0]]['id'] + 2 * stock_dictionary[subset[1]]['id']) % len(
                        stock_dictionary.keys())
                }
            except:
                print((stock_dictionary[subset[0]]['id'] + stock_dictionary[subset[1]]['id']))
                print('dd')
                print('dd')
                print('dd')

            combination_dictionary[subset]['count'] += 1

for subset_item in combination_dictionary.values():
    count = subset_item['count']
    hash1 = subset_item['hash1']
    hash2 = subset_item['hash2']
    subset = subset_item['combination']
    if hash1 not in hash1_dict:
        hash1_dict[hash1] = {
            'subsets': set(),
            'count': 0
        }
    if hash2 not in hash2_dict:
        hash2_dict[hash2] = {
            'subsets': set(),
            'count': 0
        }
    hash1_dict[hash1]['subsets'].add(subset)
    hash1_dict[hash1]['count'] += count

    hash2_dict[hash2]['subsets'].add(subset)
    hash2_dict[hash2]['count'] += count

hash1_to_delete = []
for hash1_key in hash1_dict.keys():
    if hash1_dict[hash1_key]['count'] <= SUPPORT_S:
        hash1_to_delete.append(hash1_key)

hash2_to_delete = []
for hash2_key in hash2_dict:
    if hash2_dict[hash2_key]['count'] <= SUPPORT_S:
        hash2_to_delete.append(hash2_key)

for to_delete in hash1_to_delete:
    del hash1_dict[to_delete]

for to_delete in hash2_to_delete:
    del hash2_dict[to_delete]

# PASS #3
all_true_combinations = set()

for hash1_key in hash1_dict.keys():
    hash1_item = hash1_dict[hash1_key]

    new_list = []

    for index, combination in enumerate(hash1_item['subsets']):
        if stock_dictionary[combination[0]]['count'] > SUPPORT_S and \
                stock_dictionary[combination[1]]['count'] > SUPPORT_S:
            new_list.append(combination)

    hash1_item['subsets'] = new_list
    all_true_combinations = all_true_combinations | set(new_list)

for hash2_key in hash2_dict.keys():
    hash2_item = hash2_dict[hash2_key]

    new_list = []

    for index, combination in enumerate(hash2_item['subsets']):
        if stock_dictionary[combination[0]]['count'] > SUPPORT_S and \
                stock_dictionary[combination[1]]['count'] > SUPPORT_S:
            new_list.append(combination)

    hash2_item['subsets'] = new_list
    all_true_combinations = all_true_combinations | set(new_list)

print('SINGLETONS')
for i in stock_dictionary.keys():
    if stock_dictionary[i]['count'] > SUPPORT_S:
        print(f'(\'{i}\')')

print('DOUBLETONS')
for i in all_true_combinations:
    print(i)