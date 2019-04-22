import os
import sys
import numpy as np

class TestData():
    def  __init__(self):
        self.upper_path = ''

        self.upper_obj = None
        self.child_obj = []

        self.full_path = ''
        self.relative_path = ''
        self.level = 0

        self.files = []
        self.total_num = 0
        self.all_error_num = 0
        self.heji_error_num = 0
        self.ztgz_error_num = 0

def write_to_file(filepath, content):
    f = open(filepath, 'a+', encoding='utf-8')
    f.write(content)
    f.close


def get_gt(path):
    gt = []

    for line in open(path, encoding='utf-8'):
        gt.append(line.strip('\n'))
    
    return gt

def find_upper_and_child(test_data_list):
    for test_data in test_data_list:
        for data in test_data_list:
            if test_data.upper_path == data.full_path:
                test_data.upper_obj = data
            
            if data.upper_path == test_data.full_path:
                test_data.child_obj.append(data)
    
def gen_test_data(root_path):
    test_data_list = []
    file_counter = 0
    pre_level = 0
    level = 0

    top = root_path.split("/")[-1]
    if not top.strip():
        top = root_path.split("/")[-2]
        hasslash = True
    else:
        hasslash = False
    for root, dirs, files in os.walk(root_path, topdown = False): 
            test_data = TestData()

            test_data.upper_path = os.path.split(root)[0]
            test_data.full_path = root
            if hasslash:
                test_data.relative_path = top+root[len(root_path)-1:]
            else:
                test_data.relative_path = top+root[len(root_path):]
            test_data.level = test_data.relative_path.count('/')

            relativetop = test_data.relative_path.split("/")[0]
            # the first time coming in this loop
            if not len(test_data_list):
                pre_relativetop = test_data.relative_path.split("/")[0]
                pre_level = test_data.level 
                level_total_num = np.zeros((pre_level + 2,), dtype=np.int)

            if (relativetop != pre_relativetop) and (root!=root_path):
                level_total_num[:] = 0
            if level < test_data.level:
                level = test_data.level

            for f in files:
                filepath, tempfilename = os.path.split(f);
                shotname, extension = os.path.splitext(tempfilename);

                file_dict = dict()

                if extension.lower()  == '.pdf':
                    corresponding_gt_file = os.path.join(root, shotname + '.gt.txt')
                    if os.path.exists(corresponding_gt_file):
                        file_dict['pdf'] = os.path.join(root, tempfilename)
                        file_dict['gt'] = corresponding_gt_file
                        test_data.files.append(file_dict)

                        test_data.total_num = test_data.total_num + 1
                    else:
                        raise Exception("pdf %s does not have corresponding gt.txt file, check your training data file!" % shotname)
               
            index = max(0, test_data.level - 1)
            if root != root_path:
                if pre_level <= test_data.level:
                    level_total_num[index] += test_data.total_num
                elif pre_level > test_data.level:
                    tmp_total_num = np.sum(level_total_num[index + 1:])
                    if tmp_total_num != 0:
                        test_data.total_num = tmp_total_num
                        level_total_num[index] += test_data.total_num
                        level_total_num[index + 1:] = 0
                    else:
                        test_data.total_num = level_total_num[index]
            else:
                if test_data.total_num == 0:
                    tmp_total_num = np.sum(level_total_num[index + 1:])
                    if tmp_total_num != 0:
                        test_data.total_num = tmp_total_num
                        level_total_num[index] += test_data.total_num
                        level_total_num[index + 1:] = 0
                    else:
                        test_data.total_num = level_total_num[index]
                else:
                    level_total_num[index] += test_data.total_num

            pre_relativetop = relativetop
            test_data_list.append(test_data)
            pre_level = test_data.level

    return test_data_list, level

#root = '/home/luhya/Documents/src/xy_train_data/calamari-regression/test_data'
#test_data_list, level = gen_test_data(root)
#print(level)
#print(test_data_list)

#path = '/home/luhya/Documents/src/xy_train_data/calamari-regression/test_data/number/handwriting/NH50620_107BC418850PIC24D6EAD66180543FF975AE9B28BEF.gt.txt'
#gt = get_gt(path)
#print(gt)
