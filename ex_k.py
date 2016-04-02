# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import commands
from collections import Counter



def read_file(file_name):
    index = pd.Index(['flight','game','ice_cream', 'likelihood'])
    frame = pd.read_table(file_name, names=index)
    
    return frame
    
def classify(dataset, k, inx):
    sub = (inx - dataset[['flight','game','ice_cream']]) ** 2
    normal_diff = sub / sub.max(axis=0)
    diff_square = np.sum(normal_diff, axis=1)
    diff = np.sqrt(diff_square)
    diff_normal = diff / diff.max(axis=0)
    indice = diff.argsort()[-k:]
    
    return dataset.ix[indice,'likelihood'].value_counts()

#dataset = read_file('datingTestSet.txt')
#print classify(dataset, 20, [14488,7.153469,1.673904]).index[0]


#def train_file_digit(test_file, k):
#    test = pd.read_fwf(test_file,header=None, widths=[1] * 32)
#    a, b = commands.getstatusoutput(\
#    'ls /home/kfc/machineLearning/trainingDigits')
#    result_list = []
#    b = b.split('\n')
#    for item in b:
#        data = (pd.read_fwf('/home/kfc/machineLearning/trainingDigits/' + item, header=None, widths=[1] * 32))        
#        diff = (data == test).sum().sum()
#        result_list.append([diff, item[0]])
#    print result_list
#    result_frame = DataFrame(result_list, columns=['distance', 'number'])
#    indice = result_frame['distance'].argsort()[:k]
#    return result_frame.ix[indice, 'number'].value_counts()
    
def train_file_digit():
#    test = pd.read_fwf(test_file,header=None, widths=[1] * 32)
    a, b = commands.getstatusoutput(\
    'ls /home/kfc/machineLearning/trainingDigits')    
    b = b.split('\n')
    training_set = {}
    for item in b:
        training_set[item] = (pd.read_fwf('/home/kfc/machineLearning/trainingDigits/' + item, \
        header=None, widths=[1] * 32))
    training_set = pd.Panel(training_set) 
    print training_set
    return training_set
    
def classify_1(k, training_set):
    a, test_files = commands.getstatusoutput(\
    'ls /home/kfc/machineLearning/testDigits')
    test_files = test_files.split('\n')
    
    count = np.empty(len(test_files))
    
    
    for i, test_file in enumerate(test_files):
        test = pd.read_fwf('/home/kfc/machineLearning/testDigits/' + test_file,\
        header=None, widths=[1] * 32)
        
        result_list = []
        for key in training_set.keys():
            diff = (training_set[key] == test).sum().sum()
            result_list.append([diff, key[0]])
        
        result_frame = DataFrame(result_list, columns=['distance', 'number'])
        indice = result_frame['distance'].argsort()[-k:]
    
        result = result_frame.ix[indice, 'number'].value_counts().index[0]
        count[i] = result == test_file[0]
        print test_file[0], result, count[i]
        
    p = sum(count)/float(count.size)
    print count.size, 'test case', sum(count), 'right', p    
        
    return p
    
#train_file_digit()
print classify_1(30, train_file_digit())