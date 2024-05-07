# coding=utf-8
""" cmp_authpy
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 print(len(lines),"lines read from",filein)
 return lines

def write_lines(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for line in lines:
   f.write(line+'\n')  
 print(len(lines),"written to",fileout)


class Change(object):
 def __init__(self,metaline,lnum,line,newline):
  self.metaline = metaline
  self.lnum = lnum
  self.line = line
  self.newline = newline

class Change1:
 def __init__(self,metaline,line,newline):
  self.metaline = metaline
  self.line = line
  self.newline = newline

class Change2:
 def __init__(self,metaline,list1,list2):
  self.metaline = metaline
  self.list1 = list1
  self.list2 = list2
 
def merge_lines(lines,joinchar=' '):
 out = joinchar.join(lines)
 return out

def group_entries(groups):
 entries = []
 for igroup,group in enumerate(groups):
  if group[0].startswith('<L>'):
   entries.append(igroup)
 return entries

def get_auth_nums_regex(auths):
 # auths [A,B,...,Z]
 auths0 = auths  # [0:3]
 a = '|'.join(auths0)  # A|B|...|Z
 b = r'\b(%s)' % a
 c = b + ' ([0-9 ._]+\.)'
 regex = c
 if False: # dbg
  print('auths=',auths0)
  print('regex=',regex)
  #exit(1)
 return regex

def get_auth_nums(s,regex):
 a = re.findall(regex,s) # a list of pairs
 b = [x + ' ' + y for (x,y) in a]
 if False:
  if a != []:
   print('get_auth_nums')
   print('a=',a)
   print('b=',b)
   exit(1)
 return a

def compare_1(groups1,groups2,auths):
 regex = get_auth_nums_regex(auths)
 dbg = False
 changes = []
 notok = 0
 nok = 0
 entries1 = group_entries(groups1)
 entries2 = group_entries(groups2)
 assert len(entries1) == len(entries2)
 if dbg: print(len(entries1),"entries in 'compare'")
 for ientry,e1 in enumerate(entries1):
  e2 = entries2[ientry]
  group1 = groups1[e1]
  group2 = groups2[e2]
  assert group1[0] == group2[0] # metaline
  metaline = group1[0]
  datalines1 = group1[1:-1]
  datalines2 = group2[1:-1]
  data1 = merge_lines(datalines1)
  data2 = merge_lines(datalines2)
  data1a = get_auth_nums(data1,regex)
  data2a = get_auth_nums(data2,regex)
  if data1a == data2a:
   nok = nok + 1
   continue
  # data differs
  notok = notok + 1
  change = Change2(metaline,data1a,data2a)
  changes.append(change)
 print(nok,'entries the same')
 print(notok,'entries differ')
 return changes

def get_auth_nums_regex_4(auths):
 # auths [A,B,...,Z]
 a = '|'.join(auths)  # A|B|...|Z
 b = r'\b(%s)' % a
 c = b + ' ([0-9 .IV]+\.)' # only diff from get_auth_nums_regex
 regex = c
 if True: # dbg
  print('auths=',auths)
  print('regex=',regex)
  #exit(1)
 return regex

def compare_4(groups1,groups2,auths):
 regex = get_auth_nums_regex_4(auths)
 dbg = False
 changes = []
 notok = 0
 nok = 0
 entries1 = group_entries(groups1)
 entries2 = group_entries(groups2)
 assert len(entries1) == len(entries2)
 if dbg: print(len(entries1),"entries in 'compare'")
 for ientry,e1 in enumerate(entries1):
  e2 = entries2[ientry]
  group1 = groups1[e1]
  group2 = groups2[e2]
  assert group1[0] == group2[0] # metaline
  metaline = group1[0]
  datalines1 = group1[1:-1]
  datalines2 = group2[1:-1]
  data1 = merge_lines(datalines1)
  data2 = merge_lines(datalines2)
  data1a = get_auth_nums(data1,regex)
  data2a = get_auth_nums(data2,regex)
  if data1a == data2a:
   nok = nok + 1
   continue
  # data differs
  notok = notok + 1
  change = Change2(metaline,data1a,data2a)
  changes.append(change)
 print(nok,'entries the same')
 print(notok,'entries differ')
 return changes

def write_outrecs(fileout,outrecs):
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')  
 print(len(outrecs),"cases written to",fileout)
 
def print_outrecs(outrecs):
 for outarr in outrecs:
  for out in outarr:
   print(out)

def write_changes_1(fileout,changes):
 outarr=[]
 nauthdiff = 0
 for change in changes:
  metaline = change.metaline
  metaline = re.sub(r'<k2>.*$','',metaline)
  list1 = change.list1
  list2 = change.list2
  n1 = len(list1)
  n2 = len(list2)
  nmax = max(n1,n2)
  for i in range(nmax):
   if i < n1:
    auth1,nums1 = list1[i]
    a1 = '%s %s' % (auth1,nums1)    
   else:
    a1 = 'NA'
    auth1 = 'NA'
   if i < n2:
    auth2,nums2 = list2[i]
    a2 = '%s %s' % (auth2,nums2)    
   else:
    a2 = 'NA'
    auth2 = 'NA'
   if a1 == a2:
    flag = 'EQ'
   else:
    flag = 'NEQ'
   if auth1 != auth2:
    flag = flag + 'A'
   if False: # prior version
    out = '%s %s %s %s %s' %(i+1,metaline,a1,flag,a2)
    outarr.append(out)
   else:
    if i == 0:
     outarr.append('* ' + metaline)
    out = '%s %s %s %s' %(i+1,a1,flag,a2)
    outarr.append(out)
    
    
 write_lines(fileout,outarr)

def init_groups(lines):
 groups = []
 inentry = False
 nentry = 0
 for iline,line in enumerate(lines):
  if line.startswith('<L>'):
   inentry = True
   group = [line]
  elif line.startswith('<LEND>'):
   group.append(line)
   groups.append(group)
   nentry = nentry + 1
   inentry = False
  elif not inentry:
   group = [line]
   groups.append(group)
  else: # inentry == True
   group.append(line)
 print(len(groups),"groups",nentry,"entries")
 return groups

def change_groups_2(groups1,groups2,auths):
 # revise groups1 in place
 regex = get_auth_nums_regex(auths)
 dbg = False
 nchg = 0
 notok = 0
 nok = 0
 entries1 = group_entries(groups1)
 entries2 = group_entries(groups2)
 assert len(entries1) == len(entries2)
 if dbg: print(len(entries1),"entries in 'compare'")
 for ientry,e1 in enumerate(entries1):
  e2 = entries2[ientry]
  group1 = groups1[e1]
  group2 = groups2[e2]
  assert group1[0] == group2[0] # metaline
  metaline = group1[0]
  datalines1 = group1[1:-1]
  datalines2 = group2[1:-1]
  data1 = merge_lines(datalines1,'\n')
  data2 = merge_lines(datalines2,' ')
  # data1a = get_auth_nums(data1,regex)
  # data2a = get_auth_nums(data2,regex)
  data1a = re.findall(regex,data1) # list of pairs
  data2a = re.findall(regex,data2)
  if data1a == data2a:
   nok = nok + 1
   continue
  # data differs
  notok = notok + 1
  if dbg:
   print('difference at %s' % metaline)
   print(len(data1a),data1a)
   print(len(data2a),data2a)

  new_data1 = revise_auth_nums_2(data1,data1a,data2a)
  if new_data1 == None:
   # difference occurs at line break. Cannot handle
   print(metaline,' new_data1 is None')
   print()
   continue
  nchg = nchg + 1
  # unmerge newdata1
  new_datalines1 = new_data1.split('\n')
  new_group1 = []
  new_group1.append(group1[0])  # metaline
  for x in new_datalines1:
   new_group1.append(x)
  new_group1.append(group1[-1]) # LEND
  groups1[e1] = new_group1
 print(nok,'entries the same')
 print(notok,'entries differ')
 print(nchg,'entries changed')

def revise_auth_nums_2(data1,data1a,data2a):
 dbg = True
 ans = []
 newdata1 = data1
 for i,ls1 in enumerate(data1a):
  ls2 = data2a[i]
  auth1,nums1 = ls1
  auth2,nums2 = ls2
  if auth1 != auth2:
   print('revise_auth_nums_2: auths differ',ls1,ls2)
   continue
  if nums1.replace(' ','') != nums2.replace(' ',''):
   print('revise_auth_nums_2: nums differ',ls1,ls2)
   continue
  old = '%s %s' %(auth1,nums1)
  new = '%s %s' %(auth2,nums2)
  # newdata1 = newdata1.replace(old,new)
  newdata1 = re.sub('\b' + old,new,newdata1)
 return newdata1

def change_groups_3(groups1,groups2,auths):
 # revise groups1 in place
 regex = get_auth_nums_regex(auths)
 # variant of get_auth_nums_regex
 a = '|'.join(auths)  # A|B|...|Z
 b = r'\b(%s)' % a
 c = b + '( [0-9 ._]+\.)?$'
 regex1 = c
 # regex2
 regex2 = '^([0-9 .]+\.)'

 dbg = False
 nchg = 0
 notok = 0
 nok = 0
 entries1 = group_entries(groups1)
 entries2 = group_entries(groups2)
 assert len(entries1) == len(entries2)
 if dbg: print(len(entries1),"entries in 'compare'")
 for ientry,e1 in enumerate(entries1):
  e2 = entries2[ientry]
  group1_orig = groups1[e1]
  group1 = revise_group_3(group1_orig,regex1,regex2)
  group2 = groups2[e2]
  assert group1[0] == group2[0] # metaline
  metaline = group1[0]
  datalines1 = group1[1:-1]
  datalines2 = group2[1:-1]
  data1 = merge_lines(datalines1,'\n')
  data2 = merge_lines(datalines2,' ')
  # data1a = get_auth_nums(data1,regex)
  # data2a = get_auth_nums(data2,regex)
  data1a = re.findall(regex,data1) # list of pairs
  data2a = re.findall(regex,data2)
  if data1a == data2a:
   nok = nok + 1
   continue
  # data differs
  notok = notok + 1
  if dbg:
   print('difference at %s' % metaline)
   print(len(data1a),data1a)
   print(len(data2a),data2a)

  new_data1 = revise_auth_nums_2(data1,data1a,data2a)
  if new_data1 == None:
   # difference occurs at line break. Cannot handle
   continue
  nchg = nchg + 1
  # unmerge newdata1
  new_datalines1 = new_data1.split('\n')
  new_group1 = []
  new_group1.append(group1[0])  # metaline
  for x in new_datalines1:
   new_group1.append(x)
  new_group1.append(group1[-1]) # LEND
  groups1[e1] = new_group1
 print(nok,'entries the same')
 print(notok,'entries differ')
 print(nchg,'entries changed')

def revise_group_3(group,regex1,regex2):
 ngroup = len(group)
 # group1 a copy of group
 group1 = []
 for line in group:
  group1.append(line)
 newlines = []
 for i,line in enumerate(group1):
  if i == 0:
   #newlines.append(line)
   continue
  if (i+1) == ngroup:
   # newlines.append(line)
   continue
  nextline = group1[i+1]
  m1 = re.search(regex1,line)
  m2 = re.search(regex2,nextline)
  if m1 == None:
   continue
  if m2 == None:
   continue
  extra = m2.group(1)
  newnextline = re.sub(regex2,'',nextline)
  newnextline = newnextline.strip()
  group1[i+1] = newnextline
  newline = line + ' ' + extra
  group1[i] = newline
 return group1

def init_auth(filein):
 lines = read_lines(filein)
 auths = [line.split('\t')[0] for line in lines]
 print(len(auths),"auth abbreviations from file",filein)
 return auths

def write_groups(fileout,groups):
 outarr = []
 for group in groups:
  for x in group:
   outarr.append(x)
 write_lines(fileout,outarr)
 
if __name__=="__main__":
 option = sys.argv[1]
 fileauth = sys.argv[2]
 filein = sys.argv[3] # xxx.txt cdsl
 filein1 = sys.argv[4] # xxx.txt AB
 fileout = sys.argv[5] #
 auths = init_auth(fileauth)
 lines_cdsl = read_lines(filein)
 lines_ab = read_lines(filein1)
 groups_cdsl = init_groups(lines_cdsl)
 # write_groups(fileout,groups_cdsl) dbg: check fileout same as filein
 # exit(1)
 groups_ab = init_groups(lines_ab)
 maxdiff = None
 if option == '1':
  changes = compare_1(groups_cdsl,groups_ab,auths)
  write_changes_1(fileout,changes)
 elif option == '2':
  # revise groups_cdsl
  change_groups_2(groups_cdsl,groups_ab,auths)
  write_groups(fileout,groups_cdsl)
 elif option == '3':
  # revise groups_cdsl
  change_groups_3(groups_cdsl,groups_ab,auths)
  write_groups(fileout,groups_cdsl)
 if option == '4': # R. Schl.
  auths0 = ['R. Schl.' , 'PAN.', 'RAM. ed. Ser.',
            'RAM. Schl.', 'RAM.', 'GITA-GOV.',
            'Pott.', 'Graff']
  changes = compare_4(groups_cdsl,groups_ab,auths0)
  write_changes_1(fileout,changes)
 else:
  print('unknown option',option)
  
