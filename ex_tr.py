# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 11:49:26 2016

@author: kfc
"""

from pandas import Series, DataFrame
import pandas as pd

from math import log

def grab_dataset(filename):
    dataset = pd.read_table(filename, \
        header=None, names=['age', 'prescript', 'astigmatic', 'tearRate', 'choice'])
    return dataset
    
def calc_shannon_ent(count_data):
#    count_data = dataset.ix[:,'choice'].value_counts()
    feature_index = count_data.index
    entry_num = count_data.values.sum()
    shannon_ent = 0.0
    for item in feature_index:
        prob = count_data[item] / float(entry_num)
        shannon_ent -= prob * log(prob, 2)
    return shannon_ent

def choose_feature(dataset):
    features = dataset.columns[:-1]
    base_ent = calc_shannon_ent(dataset['choice'].value_counts())
    ent_gain = Series(index=features)
    for feature in features:
        new_ent = 0.0
        feat_list = dataset[feature].value_counts()
        prob = feat_list / float(sum(feat_list))
        for feat in feat_list.index:
            tmp_ent = calc_shannon_ent(dataset.ix[dataset[feature] == feat]['choice'].value_counts())       
            new_ent -= prob[feat] * tmp_ent
        ent_gain[feature] = base_ent - new_ent
    ent_gain.sort_values(inplace=True)
    return ent_gain.index[0]
    
def createtree(dataset):
    choice_count = dataset['choice'].unique()
    if choice_count.size == 1:
        return choice_count[0]
    elif dataset.shape[1] == 1:
        return dataset['choice'].value_counts().index[0]
    else:
        bestfeature = choose_feature(dataset)
        tree = {bestfeature:{}}
        split_choice = dataset[bestfeature].value_counts()
        for value in split_choice.index:
            tree[bestfeature][value] = createtree(\
            dataset.ix[dataset[bestfeature] == value,:].drop(bestfeature,axis=1))
    return tree
        
def save_tree(tree, filename):
    import pickle
    f = open(filename, 'w')
    pickle.dump(tree, filename)
    f.close

def grab_tree(filename):
    import pickle
    f = open(filename)
    return pickle.load(filename)

def classify(tree, testlist):
    feat = tree.keys()[0]
    next_tree = tree[feat]
    if type(next_tree) == type(dict()):
        return next_tree[testlist[feat]]
    else:
        return next_tree[testlist[feat]] 
    return classify(tree[feat][test_feat])
    
def main():
    dataset = grab_dataset('lenses.txt')
#    print dataset
#    print calc_shannon_ent(dataset['choice'].value_counts())
#    print choose_feature(dataset)
    print classify(createtree(dataset),\
    {'age': 'young', 'prescript': 'myope', 'astigmatic': 'no', 'tearRate': 'reduced'})
if __name__=='__main__':
    main()