#!/usr/bin/python -u
# -*- coding: utf-8 -*-
'''
Tuple and Preference generation
'''

import csv
import os
import random

# Experiment parameters
ATT = 'att'
TUP = 'tup'
DEL = 'del'
INS = 'ins'
RUL = 'rul'
LEV = 'lev'
IND = 'ind'
TOP = 'top'
ALGORITHM = 'algorithm'

# Parameter values related to generation of table data
# Max value for attributes
MAX_VALUE = 63
# Min value for attributes
MAX_VALUE = 0
# List of attributes number for testing
ATTRIBUTE_LIST = [8, 16, 32, 64]
# List of tuples number
TUPLE_LIST = [500, 1000, 2000, 4000, 8000]
# Maximum tuple number
TUPLE_MAX = TUPLE_LIST[-1]
# Top-k variation (-1 for best operator)
TOPK_LIST = [-1, 125, 250, 500, 1000]

# Default top-k
TOPK_DEFAULT = -1
# Default tuples number
TUPLE_DEFAULT = 1000
# Default attributes number
ATTRIBUTE_DEFAULT = 8
# Default iteration number
ITERATION_DEFAULT = 100

# Parameter values related to preference queries
# List of rules number
RULE_LIST = [2, 4, 8, 16, 32]
# Default rules number
RULE_DEFAULT = 8
# List of levels
LEVEL_LIST = [1, 2, 4, 8]
# Default level
LEVEL_DEFAULT = 2
# Indifferent attributes list
INDIFF_LIST = [0, 1, 2, 4]
# Default indifferent attributes
INDIFF_DEFAULT = 4

#Interval operators
INTERVAL_OPERATORS = {
    'eq' : '=',
    'neq' : '<>',
    'gt' : '>',
    'lt' : '<',
    'ge' : '>=',
    'le' : '<=',
}

# Preference rules format
RULE_STRING = 'IF A1 = {c1} AND A2 = {c2} THEN A3 = {b} BETTER A3 = {w} {i}'
# Query
QUERY = '''SELECT {t} * FROM r
ACCORDING TO PREFERENCES
{p};'''

def gen_insert_records(tup_number, att_number):
    '''
    Generate records
    '''
    # List of records
    rec_list = []
    # Loop to count the tuples number
    for _ in range(tup_number):
        # new tuple record
        new_record = {}
        # List of attributes
        att_list = ['A' + str(number + 1) for number in range(att_number)]
        # Generate each attribute value
        for att in att_list:
            new_record[att] = random.randint(0, MAX_VALUE)
        # Append record into list of records
        rec_list.append(new_record)
    # Return built record list
    return rec_list
    
def gen_rule(rule_dict):
    '''
    Convert rule dictionary into rule in string format
    '''
    return RULE_STRING.format(c1=rule_dict['COND1'],
                              c2=rule_dict['COND2'],
                              b=rule_dict['BEST'],
                              w=rule_dict['WORST'],
                              i=rule_dict['INDIFF'])

def gen_rules(n_rules, level, ind):
    '''
    Generate preference rules
    '''
    # Preference level
    current_level = 0
    # Values for attributes of rule condition
    cond1 = 1
    cond2 = 1
    # Preferred value
    pref_value = 1
    # Indifferent attributes
    indiff_list = []
    # Build list of indifferent attributes
    indiff_str = ''
    # First indiferent attribute
    ind_start=4;
    if ind > 0:
        # Indifferent attributes start in A4
        for att_cont in range(ind):
            indiff_list.append('A' + str(att_cont + ind_start))
        indiff_str = '[' + ', '.join(indiff_list) + ']'
    # Build rules list
    rules_list = []
    for _ in range(n_rules):
        rule_dict = {}
        rule_dict['COND1'] = cond1
        rule_dict['COND2'] = cond2
        rule_dict['BEST'] = pref_value
        pref_value += 1
        rule_dict['WORST'] = pref_value
        current_level += 1
        # Check if maximum level have been reached
        if current_level == level:
            current_level = 0
            pref_value = 1
            cond2 += 1            
        # Check if maximum values have been reached
        if cond2 > MAX_VALUE:
            cond1 += 1
            if cond1 > MAX_VALUE:
                cond1 = 1
            cond2 = 1
        rule_dict['INDIFF'] = indiff_str
        rules_list.append(gen_rule(rule_dict))
    return rules_list 

def gen_query(n_rules, level, ind, top):
    '''
    Generate a preference query
    '''
    rules = gen_rules(n_rules, level, ind)
    topk = ''
    if top>-1 :
        topk = 'TOP('+str(top)+')'

    prefs = '\nAND\n'.join(rules)  
    complete_query = QUERY.format(t = topk,
                              p = rules)
    return complete_query

def get_query_id(n_rules,level,ind,top):
    '''
    Return a query ID for given parameters
    '''
    operation = 'best'
    if top != -1:
        operation = TOP + str(top)
    return RUL + str(n_rules) + \
        LEV + str(level) + \
        IND + str(ind) + \
        operation

def get_experiment_id(exp_conf):
    '''
    Return the ID of an experiment
    '''
    return get_table_id(exp_conf) + get_query_id(exp_conf)
