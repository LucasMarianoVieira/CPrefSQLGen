#!/usr/bin/python -u
# -*- coding: utf-8 -*-
'''
Tuple and Preference generation
'''

import csv
import os
import random
import file_handler

# Parameter values related to generation of table data
# Max value for attributes
MAX_VALUE = 63
# Min value for attributes
MIN_VALUE = 0

# Preference rules format
RULE_STRING = 'IF A1 = {c1} AND A2 = {c2} THEN A3 = {b} BETTER A3 = {w} {i}'
RULE_REWRITE_STRING = 'IF (0 <= {a1} <= {n}) THEN (0 <= {a2} <= {x}) BETTER ({x} < {a2} <= {n})'
# Query
QUERY = '''SELECT {t} * FROM r
ACCORDING TO PREFERENCES
{p};'''

def gen_records(tup_number, att_number):
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

def gen_rule_rewrite(rule_dict):
    '''
    Convert rule dictionary into rule in string format
    For rule rewriting
    '''
    return RULE_REWRITE_STRING.format(a1=rule_dict['A1'],
                              a2=rule_dict['A2'],
                              x=rule_dict['X'],
                              n=rule_dict['N'])

def gen_rules_rewrite(n_rules, n_max):
    '''
    Generate preference rules
    For rule rewriting
    '''
    # Interval max value
    n = n_max
    # Interval split point
    x = n // 2.0
    # Preference level
    current_level = 1
    
    # Build rules list
    rules_list = []
    for _ in range(n_rules):
        rule_dict = {}
        rule_dict['A1'] = 'A'+str(current_level)
        rule_dict['A2'] = 'A'+str(current_level+1)

        rule_dict['X'] = x
        rule_dict['N'] = n

        current_level += 1

        rules_list.append(gen_rule_rewrite(rule_dict))
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
                              p = prefs)
    return complete_query
