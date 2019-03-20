import os

from get_ztgz import gen_big_table, gen_get_value, focus_words
big_table = gen_big_table()
get_value = gen_get_value(big_table)

lines = open('data.txt').read().split('\n')
datas = list(map(lambda x:x.split('==>'), lines))

table_file = open("table.txt", "w")
lines = []
for key in big_table:
    line = key + "==>" + big_table[key] + "\n"
    lines.append(line)
table_file.writelines(lines)

total = len(datas)
count_o = 0
count_f = 0
count_v = 0
for rec,gt in datas:
    if rec == '' or gt == '':
        continue
    rec_f = focus_words(rec)
    gt_f = focus_words(gt)
    rec_v = get_value(rec_f)
    gt_v = get_value(gt_f)
    if rec == gt:
        count_o += 1
    if rec_f == gt_f:
        count_f += 1
    if rec_v == gt_v:
        count_v += 1
    else:
        print(rec, '>>', rec_v, "=\=", gt_v)
        pass
print('==================================')
print(round(count_o / total * 100, 2), '%')
print(round(count_f / total * 100, 2), '%')
print(round(count_v / total * 100, 2), '%')