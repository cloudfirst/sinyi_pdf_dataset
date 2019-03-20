import os

from get_ztgz_2 import compare_words, focus_words, find_most_like

lines = open('data.txt').read().split('\n')
lines2 = open('data2.txt').read().split('\n')
lines.extend(lines2)
datas = list(map(lambda x:x.split('==>'), lines))
for data in datas:
    if len(data) != 2:
        print(data, len(data))

total = len(datas)
count_o = 0
count_f = 0
count_v = 0

for rec,gt in datas:
    # if rec == '' or gt == '':
    #     continue
    rec_f = focus_words(rec)
    gt_f = focus_words(gt)
    rec_v = find_most_like(rec_f)
    if rec == gt:
        count_o += 1
    if rec_f == gt_f:
        count_f += 1
    if rec_v == gt_f:
        count_v += 1
    else: 
        print(rec_f, '==>', rec_v, '=\=', gt_f)
    if rec_f != rec_v:
        print(rec_f, "==", gt_f, rec_v)

print('==================================')
print(round(count_o / total * 100, 2), '%')
print(round(count_f / total * 100, 2), '%')
print(round(count_v / total * 100, 2), '%')