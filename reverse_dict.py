# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 11:38:28 2020

@author: Callum
"""
import string

def reverse_dict(d):
    rev = {}
    for key in d.keys():
        for val in d[key]:
            if val in rev.keys():
                #rev[val] = [rev[val], key] 
                rev[val].append(key)
            else:
                rev[val] = [key]
    return rev


#d={'move': ['liikuttaa'], 'hide': ['piilottaa', 'salata'], 'six': ['kuusi'], 'fir': ['kuusi']}
#print(reverse_dict(d))

def find_matching(l, s):
    val = list(enumerate([s in x for x in l]))
    return list(h[0] for h in val if h[1] == True)
    
#print(find_matching(["sensitive", "engine", "rubbish", "comment"], "en"))

def two_dice():
    v = [(i,j) for i in range(1,7) for j in range(1,7) if i + j == 5]
    for c in v:
        print(c)
    
#two_dice()

def transform(s1,s2):
    a = map(int, s1.split())
    b = map(int, s2.split())
    z = zip(a,b)
    return list(x[0]*x[1] for x in z)
   
    
#print(transform("1 5 3", "2 6 -1"))

def positive_list(L):
    return list(filter(lambda x: x>0, L))

#print(positive_list([2,-2,0,1,-7]))

def acronyms(s):
    sl = s.split()
    sl2 = [x.strip(string.punctuation) for x in sl] 
    return list(filter(lambda y: len(y)>1 and y.isupper(), sl2))

#print(acronyms("""For the purposes of the EU General Data Protection Regulation (GDPR), the controller of your personal information is International Business Machines Corporation (IBM Corp.), 1 New Orchard Road, Armonk, New York, United States, unless indicated otherwise. Where IBM Corp. or a subsidiary it controls (not established in the European Economic Area (EEA)) is required to appoint a legal representative in the EEA, the representative for all such cases is IBM United Kingdom Limited, PO Box 41, North Harbour, Portsmouth, Hampshire, United Kingdom PO6 3AU."""))

def sum_equation(l):
    if l == "":
        return "0 = 0"
    else:
        return " + ".join(str(c) for c in l) + f" = {sum(l)}"

print(sum_equation([1,2,3]))