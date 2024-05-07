# coding=utf-8
""" cmp_misc1.py
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

def compare_1(groups1,groups2,regex):
 #regex = re.compile(r'{%[^%]*%}')
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
  if not group1[0] == group2[0]:
   print('metaline problem: CDSL=%s, AB=%s' % (group1[0],group2[0]))
   exit(1)
  metaline = group1[0]
  datalines1 = group1[1:-1]
  datalines2 = group2[1:-1]
  data1 = merge_lines(datalines1)
  data2 = merge_lines(datalines2)
  #data1a = re.findall(regex,data1) # list of 
  #data2a = re.findall(regex,data2)
  data1a = data1.split()
  data2a = data2.split()
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

def write_changes_1_helper(list1,list2):
 n1 = len(list1)
 n2 = len(list2)
 arr = []
 ndiff = 0
 nmax = max(n1,n2)
 for i in range(nmax):
  if i < n1:
   a1 = list1[i]
  else:
   a1 = 'NA'
  if i < n2:
   a2 = list2[i]
  else:
   a2 = 'NA'
  if a1 == a2:
   flag = 'EQ'
  else:
   flag = 'NEQ'
  if flag == 'NEQ':
   ndiff = ndiff + 1
  if (ndiff == 1) and (flag == 'NEQ'):
   flag = 'NE1'
   index_first_diff = i
  #out = '%s %s %s %s' %(i+1,a1,flag,a2)
  arr.append((a1,a2,flag))
 return arr,index_first_diff

def write_changes_1(fileout,changes):
 outarr=[]
 ndiff = 0
 for ichange,change in enumerate(changes):
  metaline = change.metaline
  metaline = re.sub(r'<k2>.*$','',metaline)
  list1 = change.list1
  list2 = change.list2
  arr,ifirstdiff = write_changes_1_helper(list1,list2)
  i1 = max(ifirstdiff-5,0)
  i2 = min(ifirstdiff+5,len(arr))
  b1 = []
  b2 = []
  for i in range(i1,i2):
   b1.append(arr[i][0])
   b2.append(arr[i][1])
  outarr.append('* %s' % metaline)
  #print(b1)
  #print(b2)
  #exit(1)
  outarr.append('CD: %s' %( ' '.join(b1)))
  outarr.append('AB: %s' %( ' '.join(b2)))
  
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

def xchange_groups_1_helper(str1,str2):
 assert len(str1) == len(str2)
 n = len(str1)
 diffs = []
 a = []  # array of characters
 for i,c1 in enumerate(str1):
  c2 = str2[i]
  if c1 == c2:
   a.append(c1)
   continue
  if (c1 == '\n') and (c2 == ' '):
   a.append(c1)
   continue # insignificant difference
  diffs.append((i,c1,c2))
  a.append(c2)
 s = ''.join(a) # new string
 return diffs,s

def xchange_groups_1(groups1,groups2):
 # revise groups1 in place
 dbg = False
 nchg = 0
 notok = 0
 nok = 0
 entries1 = group_entries(groups1)
 entries2 = group_entries(groups2)
 assert len(entries1) == len(entries2)
 if dbg: print(len(entries1),"entries in 'compare'")
 nmisc = 0
 for ientry,e1 in enumerate(entries1):
  e2 = entries2[ientry]
  group1 = groups1[e1]
  group2 = groups2[e2]
  assert group1[0] == group2[0] # metaline
  metaline = group1[0]
  datalines1 = group1[1:-1]
  datalines2 = group2[1:-1]
  data1 = merge_lines(datalines1,'\n')
  data1_spc = merge_lines(datalines1,' ')
  data2 = merge_lines(datalines2,' ')
  if data1_spc == data2:
   nok = nok + 1
   continue
  if len(data1) != len(data2):
   # this module doesn't know about these diffs
   notok = notok + 1
   continue
  char_diffs,new_data1 = change_groups_1_helper(data1,data2)
 
  if len(char_diffs) != 1:
   if nmisc < 5:
    print(metaline,char_diffs)
   nmisc = nmisc + 1
   notok = notok + 1
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
 filein = sys.argv[2] # xxx.txt cdsl
 filein1 = sys.argv[3] # xxx.txt AB
 fileout = sys.argv[4] #
 lines_cdsl = read_lines(filein)
 lines_ab = read_lines(filein1)
 groups_cdsl = init_groups(lines_cdsl)
 groups_ab = init_groups(lines_ab)
 maxdiff = None
 if option == '1xxx':
  # revise groups_cdsl - first diff word
  change_groups_1(groups_cdsl,groups_ab)
  write_groups(fileout,groups_cdsl)
 elif option == '1':
  regex = re.compile(r'{%[^%]*%}')
  changes = compare_1(groups_cdsl,groups_ab,regex)
  write_changes_1(fileout,changes)
 elif option == '3':
  regex = re.compile(r'{#[^#]*#}')
  changes = compare_2(groups_cdsl,groups_ab,regex)
  write_changes_2(fileout,changes)
 elif option == '4':
  regex = re.compile(r'<lang.*?</lang>')
  changes = compare_2(groups_cdsl,groups_ab,regex)
  write_changes_2(fileout,changes)
 
 else:
  print('unknown option',option)
  
