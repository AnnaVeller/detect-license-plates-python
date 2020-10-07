def load_regions():
    all_region = []
    f = open('regions.txt', 'r', encoding='UTF-8')
    for line in f.readlines():
        tmp = line.split('\t')
        all_region.append(tmp[0])
    return all_region