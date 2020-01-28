#!/usr/bin/python -u
# -*- coding: utf-8 -*-
'''
File and Directory handling
'''

import csv
import os

from gen import get_id, get_data_id, get_util_id


# =============================================================================
# Generic directories and files
# =============================================================================
MAIN_DIR = 'main'
DATA_DIR = 'data'
QUERY_DIR = 'queries'
OUT_DIR = 'out'
SUMMARY_DIR = 'summary'
RESULT_DIR = 'result'
DIR_LIST = [MAIN_DIR, DATA_DIR, QUERY_DIR, ENV_DIR, OUT_DIR, DETAIL_DIR,
            SUMMARY_DIR, RESULT_DIR]

def _create_directory(directory):
    '''
    Create a directory if it does not exists
    '''
    if not os.path.exists(directory):
        os.mkdir(directory)

def write_to_csv(filename, attribute_list, record_list):
    '''
    Store record list into a CSV file
    '''
    # Check if file does not exists
    if not os.path.isfile(filename):
        # Store data to file
        print("writing csv data...")
        data_file = open(filename, 'w')
        writer = csv.DictWriter(data_file, attribute_list, delimiter=',')
        writer.writeheader()
        writer.writerows(record_list)
        data_file.close()

def append_to_csv(filename, attribute_list, record_list):
    '''
    Append record list into a CSV file
    '''
    data_file = open(filename, 'a')
    writer = csv.DictWriter(data_file, attribute_list, delimiter=',')
    writer.writerows(record_list)
    data_file.close()

def write_to_txt(filename, text):
    '''
    Store record list into a CSV file
    '''
    # Check if file does not exists
    if not os.path.isfile(filename):
        print("writing to text file...")
        #Store data to file
        out_file = open(filename, 'w')
        out_file.write(text)
        out_file.close()

def write_result_file(filename, record_list, key_field):
    '''
    Write to a result file
    '''
    # Check if there exists records to be stored
    if len(record_list):
        # Get the field list
        field_list = [field for field in record_list[0].keys()
                      if field != key_field]
        # Sort the field list
        field_list.sort()
        # Put key field in the beginning of field list
        field_list.insert(0, key_field)
        write_to_csv(filename, field_list, record_list)
