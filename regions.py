def load_regions():
    all_region = {}
    f = open('regions.txt', 'r', encoding='UTF-8')
    for line in f.readlines():
        tmp = line.split('\t')
        all_region[tmp[0]] = tmp[1]
    return all_region