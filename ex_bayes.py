import numpy as np
from collections import Counter
from pandas import DataFrame, Series
import pandas as pd
import random

def extract_file():

    ham, nham, testcase_h = read_dir('./email/ham/')
    spam, nspam, testcase_s = read_dir('./email/spam/')
    ham_frame = DataFrame(ham[:,1], index=ham[:,0], columns=['time'], dtype=int)
    spam_frame = DataFrame(spam[:,1], index=spam[:,0], columns=['time'], dtype=int)
    return ham_frame, nham, spam_frame, nspam, testcase_h + testcase_s + ['hi']


def read_dir(dir):
    import commands
    import re

    file_list = commands.getoutput('ls ' + dir)
    files = file_list.split('\n')

    random.shuffle(files)

    test = []
    for file in files[:5]:
        raw_data = []
        f = open(dir + file)
        content = f.read()
        raw_data.extend(re.findall('[a-zA-Z]+', content))
        data = [word.lower() for word in raw_data]
        test.append(data)

    file_number = len(files[5:])

    raw_data = []
    for file in files[5:]:
        f = open(dir + file)
        content = f.read()
        raw_data.extend(re.findall('[a-zA-Z]+', content))
    data = [word.lower() for word in raw_data]
    data = Counter(data)
    data_set = data.most_common()
    return np.array(data_set), file_number, test

def train_nbo(ham_frame, nham, spam_frame, nspam):
    p_ham = nham / float(nham + nspam)
    p_spam = nspam / float(nham + nspam)

    ham_frame['p_word_ham'] = ham_frame['time'] / sum(ham_frame['time'])
    spam_frame['p_word_spam'] = spam_frame['time'] / sum(spam_frame['time'])
    return p_ham, p_spam, ham_frame, spam_frame

def classify(test, p_ham, p_spam, ham_frame, spam_frame):
    p_word_ham = ham_frame.ix[test[test.isin(ham_frame.index)], 'p_word_ham']
    p_words_ham = np.sum(np.log(p_word_ham.values))

    p_word_spam = spam_frame.ix[test[test.isin(spam_frame.index)], 'p_word_spam']
    p_words_spam = np.sum(np.log(p_word_spam.values))

    p_ham_words = p_words_ham + np.log(p_ham)
    p_spam_words = p_words_spam + np.log(p_spam)

    if p_ham_words > p_spam_words:
        return 'spam'
    else:
        return 'ham'

def main():
    for i in range(10):
        ham_frame, nham, spam_frame, nspam, testcase = extract_file()
        p_ham, p_spam, ham_frame, spam_frame = train_nbo(ham_frame, nham, spam_frame, nspam)

        result = []
        for test in testcase:
            result.append(classify(Series(test), p_ham, p_spam, ham_frame, spam_frame))

        print result
    print testcase[-1]

if __name__ == '__main__':
    main()
