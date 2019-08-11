#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import division
import re
import math
import heapq


def preprocess():
    L = []                                           # type: List[List[str]]
    fo = open("collection-100.txt")
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'     # remove all the blanks and punctuations
    for line in fo.readlines():
        line = line.strip()
        line = line.lower()
        line = re.sub(r, '', line)
        if line:
            L.append(line.split())
    for i in range(len(L)):                          # delete the ending 's'
        for j in L[i]:
            if j.endswith("s"):
                x = L[i].index(j)
                L[i][x] = j[0:len(j) - 1]
    for i in range(len(L)):                          # remove the words less than 4 characters
        for j in L[i]:
            if len(j) < 4:
                L[i][L[i].index(j)] = ""
    for i in range(len(L)):
        while '' in L[i]:
            L[i].remove('')
    fo.close()
    return L


def find_documents(t):
    lis = []
    for i in range(len(L_all)):
        if t in L_all[i]:
            v = []
            v.append(i)
            for j in range(len(L_all[i])):
                if (j not in v[1:]) & (L_all[i][j] == t):
                    v.append(j)
            lis.append(v)
    return lis


def create_an_index():
    seq = []
    for i in range(len(L_all)):
        for j in L_all[i]:
            if j not in seq:
                seq.append(j)
    inverted_file = dict.fromkeys(seq)
    for i in inverted_file:
        inverted_file[i] = find_documents(i)
    return inverted_file


def compute_weight(l):
    tfreq = []
    dfreq = []
    weight = []
    for i in range(len(l)):
        tfreq.append(dict.fromkeys(l[i]))
        for j in tfreq[i]:
            tfreq[i][j] = l[i].count(j)

    for i in range(len(l)):
        dfreq.append(dict.fromkeys(l[i]))
        for k in dfreq[i]:
            num = 0
            for n in range(len(l)):
                if k in l[n]:
                    num += 1
            dfreq[i][k] = num

    for i in range(len(l)):
        weight.append(dict.fromkeys(l[i]))
        for j in weight[i]:
            weight[i][j] = (tfreq[i][j] / max(tfreq[i].values())) * math.log((100/dfreq[i][j]), 2)

    unique = []
    for i in range(len(tfreq)):
        num = 0
        for j in tfreq[i]:
            if tfreq[i][j] == 1:
                num += 1
        unique.append(num)
    return [weight, unique]


def similarity(q_, d):
    dic_q = dict.fromkeys(q_)
    up = 0
    a = 0
    b = 0
    for i in dic_q:
        dic_q[i] = 1
        if i in d:
            up += dic_q[i]*d[i]
        a += math.pow(dic_q[i], 2)
    for j in d:
        b += math.pow(d[j], 2)
    ans = up / (math.sqrt(a)*math.sqrt(b))
    return ans


def get_top3(q, w):
    s = []
    for i in range(len(w)):
        s.append(similarity(q, w[i]))
    top = heapq.nlargest(3, s)
    x = []
    y = []
    for i in range(3):
        for j in range(len(s)):
            if (s[j] == top[i]) & (j not in x):
                x.append(j)
                y.append(top[i])
    return [x[0:3], y[0:3]]


def compute_L2norm(w):
    norm = []
    for i in range(len(w)):
        num = 0
        for j in w[i]:
            num += math.pow(w[i][j],2)
        norm.append(math.sqrt(num))
    return norm


def get_5high(d):
    top = heapq.nlargest(5, d.values())
    highest = []
    for i in range(5):
        for j in d:
            if (d[j] == top[i]) & (~(j in highest)):
                highest.append(j)
    return highest[0:5]


def display(ind, sim):
    print "DID", ind+1
    print("5 highest weight keywords:")
    highest = get_5high(weight[ind])
    for i in range(5):
        lis = inverted_file[highest[i]]
        print highest[i], "->|",
        for j in range(len(lis)):
            print 'D', lis[j][0]+1, ":",
            for k in lis[j][1:]:
                print k, ",",
            print"|",
        print""
    print "number of unique words:", unique[ind]
    print "L2norm:", norm[ind]
    print "Similarity:", sim


query = open("query-10.txt")                   # read the queries
q = []
r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
for line in query.readlines():
    line = line.strip()
    line = line.lower()
    line = re.sub(r, '', line)
    if line:
        q.append(line.split())


L_all = preprocess()
inverted_file = create_an_index()
[weight, unique] = compute_weight(L_all)
norm = compute_L2norm(weight)


for k in range(len(q)):
    print "query", k+1, ":", q[k], "------------------------------------------------------------------------------"
    [index, sim] = get_top3(q[k], weight)
    for i in range(len(index)):
        display(index[i], sim[i])

query.close()
