#!/usr/bin/env python3
# -*- encoding: utf8 -*-

import os
import sys
import argparse

from file_op import TestData, gen_test_data, get_gt, write_to_file

from sinobotocr.cv2_helper import *
from sinobotocr.cv2_helper2 import *
from sinobotocr.my_pdf2img import *

logger = get_my_logger()
db_name = 'test.db'

def get_statistic_result(data_list, result_path):

    data_list.reverse()
    for d in data_list:
        if d.total_num:
            percentage = float(d.total_num - d.error_num)/d.total_num
        else:
            percentage = 0.0
	
        content = "%+6s/%-6s %.2f%% %s\n" % (str(d.error_num), str(d.total_num), percentage*100,  d.relative_path)
        #content = 'total_num: ' + str(d.total_num) + ' error_num: ' + str(d.error_num) + ' percentage: ' + str(percentage) + ' ' + d.relative_path + '\n'
        #content = str(percentage) + ' ' + d.relative_path + '\n'
        write_to_file(result_path, content)


def rec_img(path):

    logger.error("Get image from pdf from %s" % path)
    dest_file = getImageFromPDF(path)
    base_name = os.path.basename(dest_file)
    filename, file_extension = os.path.splitext(base_name)
    
    # Step 1: 图像预处理
    logger.error("step_1_pre_processing_image ...")
    orig, canny = step_1_pre_processing_image(dest_file)
    
    # Step 2: 定位并提取表格部分
    logger.error("step_2_location_table ...")
    table       = step_2_location_table(orig, canny)
    save_processed_image(table,   "/tmp/table_"  + filename + ".png")
    
    # Step 3: 提取表格中每一行的文本
    logger.error("step_3_find_text_lines ...")
    text_blocks = step_3_find_text_lines_v2(table, filename)
    
    # Step 4: 识别表格中每一行的文本，并查找关键字极其取值
    logger.error("step_4_read_keyword_and_value ...")
    areas, ztgz = step_4_read_keyword_and_value_v2(text_blocks, filename)
    
    ret = {}
    ret['filename']  = path
    if len(areas) == 2:
        ret['heji1'] = areas[0]
        ret['heji2'] = areas[1]
    else:
        ret['heji1'] = "0.0"
        ret['heji2'] = "0.0"
    
    ret['ztgz']      = ztgz
    ret['confident'] = 0.8
    ret['Status']    = "OK"
    ret['ErrDesc']   = ""
    
    # print(ret['filename'], " # ", ret['heji1'], " / ", ret['heji2'] ,"ztgz:",ztgz)
    # logger.error(" --- wgb:  %s, %s / %s, ztgz : %s" % (str(ret['filename']), str(ret['heji1']), str(ret['heji2']), ztgz))

    return ret

def get_result(test_data, gt, ret, flag):
    if flag == "all":
        if gt[0] == ret['ztgz']  and float(gt[1]) == float(ret['heji1']) and float(gt[2]) == float(ret['heji2']):
            return True
        else:
            return False
    if flag == "heji":
        if float(gt[1]) == float(ret['heji1']) and float(gt[2]) == float(ret['heji2']):
            return True
        else:
            return False
    if flag == "ztgz":
        if gt[0] == ret['ztgz']:
            return True
        else:
            return False

'''
def calc_error_num(test_data_list):
    error_num = 0

    for test_data in test_data_list:
        if test_data.child_path:
           for tes
'''

def setup_train_args(parser):
    parser.add_argument("-r", "--root", default=False, help='root path of data')
    parser.add_argument("-t", "--result", default=False, help='result path')
    # all, heji, and ztgz
    parser.add_argument("-f", "--flag", default="heji", help="result compare flag")

def usage():
    print("Usage: ")
    print(" python regression.py --root <pdf directory> --result <result file full path> --flag <compare flag> ")
    print("   pdf directory, say, /tmp/test")
    print("   result file,   say, /tmp/result")
    print("   compare flag,  say, one of [all, heji, ztgz]")
    
def main():
    parser = argparse.ArgumentParser()
    setup_train_args(parser)
    args = parser.parse_args()

    if args.root == False or args.result == False:
        usage()
        return

    test_data_list, level = gen_test_data(args.root)

    for test_data in test_data_list:

        if test_data == test_data_list[0]:
            pre_level = test_data.level
            level_error_num = np.zeros((pre_level,), dtype=np.int)

        if test_data.files:
            # test_data is of type TestData
            print("-----path: %s------" % (test_data.relative_path))
            for f in test_data.files:

                path = f['pdf']
                gt_path = f['gt']
                gt = get_gt(gt_path)

                try:
                    ret = rec_img(path)
                    if not get_result(test_data, gt, ret, args.flag):
                        test_data.error_num += 1
                        write_to_file(args.result+'_files', path + '    # ')
                        content_rec = 'rec: ' + '[' + ret['ztgz'] + ',' + ret['heji1'] + ',' + ret['heji2'] + ']'
                        content_gt = '; gt: ' + '[' + gt[0] + ',' + gt[1] + ',' + gt[2] + ']\n'
                        
                        write_to_file(args.result+'_files', content_rec + content_gt)
                        write_to_file(args.result+'_files', '\n')

                except Exception as e:
                    print(str(e))

        ######## calc error_num
        index = test_data.level - 1
        if pre_level <= test_data.level:
            level_error_num[index] += test_data.error_num
        elif pre_level > test_data.level:
            test_data.error_num = np.sum(level_error_num[index + 1:])
            level_error_num[index] += test_data.error_num
            level_error_num[index + 1:] = 0

        if test_data.level == 1:
            level_error_num[:] = 0

        #print("path: %s, pre_level: %d, level: %d, error_num: %d" % (root, pre_level, test_data.level, test_data.error_num))
        pre_level = test_data.level
        ######## calc error_num

    get_statistic_result(test_data_list, args.result)

if __name__ == '__main__':
    main()

