import collections
c = collections.Counter()
for word in predict_list:
  c[word] += 1
ans = []
for num in list(c.most_common()):
  tmp = list(num[0])
  if len(tmp)==8 or len(tmp)==9:
    tmp_num = tmp[1:4]
    tmp_region = tmp[6:]
    tmp_literal = [tmp[0]]
    tmp_literal.extend(tmp[4:6])
    tmp_num = ''.join(map(str, tmp_num))    # должно быть числом
    tmp_region = ''.join(map(str, tmp_region))    # должно быть числом
    tmp_literal = ''.join(map(str, tmp_literal))    # должно быть буквами
    if tmp_num.isdigit() and tmp_literal.isalpha() and tmp_region.isdigit():
      if tmp_region in all_region:
        ans.append(num[0])

tmp_list = []   # список найденных номеров - неподходящие по правилам
all_numbers = collections.Counter()
for num in predict_list:
  if num in ans:
    all_numbers[num] += 1
    tmp_list.append(num)


r = list(map(lambda x: x[6:], tmp_list))
fl = list(map(lambda x: x[0], tmp_list))
sl = list(map(lambda x: x[4], tmp_list))
tl = list(map(lambda x: x[5], tmp_list))
fn = list(map(lambda x: x[1], tmp_list))
sn = list(map(lambda x: x[2], tmp_list))
tn = list(map(lambda x: x[3], tmp_list))

region = collections.Counter()
first_lit = collections.Counter()
second_lit = collections.Counter()
third_lit = collections.Counter()
first_num = collections.Counter()
second_num = collections.Counter()
third_num = collections.Counter()

for i in r:
  region[i] += 1
for i in fl:
  first_lit[i] += 1
for i in sl:
  second_lit[i] += 1
for i in tl:
  third_lit[i] += 1
for i in fn:
  first_num[i] += 1
for i in sn:
  second_num[i] += 1
for i in tn:
  third_num[i] += 1

detect_region = region.most_common(1)[0][0]
detect_first_lit = first_lit.most_common(1)[0][0]
detect_second_lit = second_lit.most_common(1)[0][0]
detect_third_lit = third_lit.most_common(1)[0][0]
detect_first_num = first_num.most_common(1)[0][0]
detect_second_num = second_num.most_common(1)[0][0]
detect_third_num = third_num.most_common(1)[0][0]


print('Варианты и кол-во')
print(first_lit.most_common())
print(first_num.most_common())
print(second_num.most_common())
print(third_num.most_common())
print(second_lit.most_common())
print(third_lit.most_common())
print(region.most_common(), '\n')

print("Список встречаемых номеров и их кол-во:")
print(list(c.most_common()), '\n')
print('Список подходящих номеров:')
print(list(all_numbers.most_common()), '\n')
print('ПРЕДПОЛАГАЕМЫЙ ОТВЕТ: ', detect_first_lit, detect_first_num, detect_second_num ,
      detect_third_num, detect_second_lit, detect_third_lit, detect_region, sep='')
print("правильный ответ: ", name)