def load_regions():
    all_region = {}  # ключ - номер региона, значение - название региона
    f = open('regions.txt', 'r', encoding='UTF-8')
    for line in f.readlines():
        tmp = line.split('\t')
        all_region[tmp[0]] = tmp[1]
    return all_region


def which_regions(car_plate):
    if len(car_plate) > 6:  # А000АА777 - регион будет, если кол-во букв больше 6
        all_regions = load_regions()
        reg = car_plate[6:]
        return all_regions[reg]
    return "Didn't find region"
