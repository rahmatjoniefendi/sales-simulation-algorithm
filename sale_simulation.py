def get_cdf(probabilistic):
    cdf = []
    old_item = 0
    
    for p in probabilistic:
        cdf.append(p + old_item)
        old_item += p
        
    return [round(c, 2) for c in cdf]

def represent_range(cdf):
    cdf = cdf.copy()
    cdf.insert(0, 0)
    r = []
    for i in range(len(cdf)-1):
        r.append(('{} < R <= {}'.format(cdf[i], cdf[i+1])))
    return r

def get_range(cdf):
    cdf = cdf.copy()
    cdf.insert(0, 0)
    r = []
    for i in range(len(cdf)-1):
        r.append([cdf[i], cdf[i+1]])
    return r

def get_in_range_index(rg, random):
    index = -1
    for i in range(len(rg)):
        if random >= rg[i][0] and random <= rg[i][1]:
            index = i
            return index

def get_probabilistic_of_demand(demand, key):
    probabilistic = []
    for i in range(len(demand[key])):
        probabilistic.append(demand[key][i][1])

    return probabilistic

def get_number_of_demand(demand, key):
    probabilistic = []
    for i in range(len(demand[key])):
        probabilistic.append(demand[key][i][0])

    return probabilistic

def get_gross_income(price, demand, price_random, demand_random):
    gross_income = []
    for pr, dr in zip(price_random, demand_random):
        rp = get_in_range_index(get_range(get_cdf(price.values())), pr)
        ip = 0
        for h in range(len(price_random)):
            if ip == rp:
                probabilistic = get_probabilistic_of_demand(demand, list(demand.keys())[h])
                cdf = get_cdf(probabilistic)
                rd = get_in_range_index(get_range(cdf), dr)

                number_of_demand = get_number_of_demand(demand, list(price.keys())[h])

                result = int(list(price.keys())[h]) * number_of_demand[rd]
                gross_income.append(result)
            ip += 1

    return sum(gross_income)

def get_array_gross_income(price, demand, price_random, demand_random):
    gross_income = []
    for pr, dr in zip(price_random, demand_random):
        rp = get_in_range_index(get_range(get_cdf(price.values())), pr)
        ip = 0
        for h in range(len(price_random)):
            if ip == rp:
                probabilistic = get_probabilistic_of_demand(demand, list(demand.keys())[h])
                cdf = get_cdf(probabilistic)
                rd = get_in_range_index(get_range(cdf), dr)

                number_of_demand = get_number_of_demand(demand, list(price.keys())[h])

                result = int(list(price.keys())[h]) * number_of_demand[rd]
                gross_income.append(result)
            ip += 1

    return gross_income

def get_total_gross_income(target, price, demand, price_random, demand_random):
    total = get_gross_income(price, demand, price_random, demand_random) - target
    return total

def create_price_table(price):

    cdf = get_cdf(price.values())
    r = represent_range(cdf)

    print('                                        PRICE')
    print('+--------------------+--------------------+--------------------+--------------------+')
    print('|{}|{}|{}|{}|'.format('DEMAND'.ljust(20), 'PROBABILISTIC'.ljust(20), 'CDF'.ljust(20), 'BATAS RI'.ljust(20)))
    print('+--------------------+--------------------+--------------------+--------------------+')
    
    for k, v, c, r in zip(price.keys(), price.values(), cdf, r):
        print('|{}|{}|{}|{}|'.format(str(k).ljust(20),
                                     str(v).ljust(20),
                                     str(c).ljust(20),
                                     str(r).ljust(20))
              )

    print('+--------------------+--------------------+--------------------+--------------------+\n\n')

def create_demand_table(demand):

    for d in demand.keys():
        print('                                     PRICE OF ' + d)
        print('+--------------------+--------------------+--------------------+--------------------+')
        print('|{}|{}|{}|{}|'.format('DEMAND'.ljust(20), 'PROBABILISTIC'.ljust(20), 'CDF'.ljust(20), 'BATAS RI'.ljust(20)))
        print('+--------------------+--------------------+--------------------+--------------------+')
        ic = 0
        probabilistic = get_probabilistic_of_demand(demand, d)
        for i in demand[d]:
            print('|{}|{}|{}|{}|'.format(str(i[0]).ljust(20),
                                        str(i[1]).ljust(20),
                                        str(get_cdf(probabilistic)[ic]).ljust(20),
                                        str(represent_range(
                                            get_cdf(probabilistic))[ic]).ljust(20)
                                        )
                  )
            ic += 1
        print('+--------------------+--------------------+--------------------+--------------------+\n\n')


def show_gross_income_process(price, demand, price_random, demand_random):
    for pr, dr in zip(price_random, demand_random):
        rp = get_in_range_index(get_range(get_cdf(price.values())), pr)
        ip = 0        
        for h in range(len(price_random)):
            if ip == rp:
                probabilistic = get_probabilistic_of_demand(demand, list(demand.keys())[h])
                cdf = get_cdf(probabilistic)
                rd = get_in_range_index(get_range(cdf), dr)

                number_of_demand = get_number_of_demand(demand, list(price.keys())[h])
                result = int(list(price.keys())[h]) * number_of_demand[rd]

                print('R{} = {} ------> HARGA JUAL = {}          GROSS INCOME = {} * {}'.format('',
                                                                                                pr,
                                                                                                int(list(price.keys())[h]),
                                                                                                'HJ',
                                                                                                'D'
                                                                                                )
                      )
                print('R{} = {} ------> DEMAND     = {}                       = {} * {}'.format('',
                                                                                                dr,
                                                                                                number_of_demand[rd],
                                                                                                int(list(price.keys())[h]),
                                                                                                number_of_demand[rd]))
                
                print('                                                       = {}\n\n'.format(result))

            ip += 1


def show_gross_income_final_process(price, demand, price_random, demand_random):
    gross_income = get_array_gross_income(price, demand, price_random, demand_random)
    print('GROSS INCOME = {}'.format(' + '.join([str(gi) for gi in gross_income])))
    print('             = {}\n\n'.format(sum(gross_income)))


def show_total_gross_income_process(target, price, demand, price_random, demand_random):
    gross_income = get_array_gross_income(price, demand, price_random, demand_random)
    total_gross_income = sum(gross_income) - target
    
    print('TOTAL GROSS INCOME = {} - {}'.format(sum(gross_income), target))
    print('                   = {}\n\n'.format(total_gross_income))


def demo():
    harga_jual = {
        '1000' : 0.25,
        '2000' : 0.25,
        '3000' : 0.30,
        '4000' : 0.10,
        '5000' : 1.10
    }

    permintaan = {
        
        '1000' : [
            [100, 0.25],
            [110, 0.15],
            [130, 0.15],
            [170, 0.20],
            [180, 0.25],
        ],

        '2000' : [
            [110, 0.25],
            [120, 0.25],
            [140, 0.25],
            [150, 0.25],
        ],

        '3000' : [
            [120, 0.40],
            [150, 0.35],
            [170, 0.25],
        ],
        
        '4000' : [
            [100, 0.20],
            [120, 0.20],
            [130, 0.15],
            [140, 0.15],
            [160, 0.30]
        ],

        '5000' : [
            [110, 0.25],
            [120, 0.25],
            [130, 0.25],
            [140, 0.25],
        ],
    }


    random_harga_jual = [
        0.7031,
        0.4922,
        0.9062,
        0.9453,
        0.6094,
        0.8984,
        0.8125,
        0.3516,
        0.5156,
        0.3047
    ]

    random_permintaan = [
        0.1641,
        0.7891,
        0.4141,
        0.0391,
        0.6641,
        0.2891,
        0.9141,
        0.5391,
        0.1641,
        0.7891
    ]

    target = 0
    
    create_price_table(harga_jual)
    
    create_demand_table(permintaan)

    print('-------------------------------------------------------------------------------------------------------\n')
    
    show_gross_income_process(harga_jual, permintaan, random_harga_jual, random_permintaan)
    
    print('-------------------------------------------------------------------------------------------------------\n')
    
    show_gross_income_final_process(harga_jual, permintaan, random_harga_jual, random_permintaan)
    
    print('-------------------------------------------------------------------------------------------------------\n')
    
    show_total_gross_income_process(target, harga_jual, permintaan, random_harga_jual, random_permintaan)
    
    print('-------------------------------------------------------------------------------------------------------\n')
    
if __name__ == '__main__':
    demo()