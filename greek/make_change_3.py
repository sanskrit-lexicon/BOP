#-*- coding:utf-8 -*-
"""make_change_3.py
 
"""
from __future__ import print_function
import sys,re,codecs
import digentry  

class Change(object):
 def __init__(self,lnum,line,newline,metaline):
  self.lnum = lnum
  self.line = line
  self.newline = newline
  self.metaline = metaline

def write_changes(fileout,changes):
 outrecs=[]
 for change in changes:
  outarr=[]
  lnum = change.lnum
  line = change.line
  newline = change.newline
  metaline = change.metaline
  metaline = re.sub(r'<k2>.*$','',metaline)
  outarr.append('; %s' % metaline)
  outarr.append('%s old %s' %(lnum,line))
  outarr.append(';')
  outarr.append('%s new %s' %(lnum,newline))
  outarr.append('; ---------------------------')
  outrecs.append(outarr)
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
    for out in outarr:
     f.write(out+'\n')
 print(len(changes),"changes written to",fileout)

def check_entries_L(Ldict,Ldictab):
 s = set(Ldict.keys())
 sab = set(Ldictab.keys())
 diff1 = s.difference(sab)
 print('in L not in Lab',diff1)
 diff2 = sab.difference(s)
 print('in Lab not in L',diff2)

def greek_instances(entry):
 a = []
 for line in entry.datalines:
  b = re.findall(r'<lang n="greek">.*?</lang>',line)
  for x in b:
   a.append(x)
 return a

def make_changes(entries,entriesab):
 changes = []
 for ientry,entry in enumerate(entries):
  entryab = entriesab[ientry]
  greeks = greek_instances(entry)
  greeksab = greek_instances(entryab)
  if len(greeks) != 1:
   continue
  if len(greeksab) != 1:
   continue
  found = False
  for iline,line in enumerate(entry.datalines):
   b = re.findall(r'<lang n="greek">.*?</lang>',line)
   if b != []:
    found = True
    break
  assert found
  lnum = entry.linenum1 + iline + 1
  gold = greeks[0]
  gnew = greeksab[0]
  newline = line.replace(gold,gnew)
  metaline = entry.metaline
  change = Change(lnum,line,newline,metaline)
  changes.append(change)
 return changes

if __name__=="__main__":
 filein = sys.argv[1] # bop csl-orig
 fileab = sys.argv[2] # bop ab
 fileout = sys.argv[3] #  

 entries = digentry.init(filein)
 digentry.Entry.Ldict = {}
 entriesab = digentry.init(fileab)

 changes = make_changes(entries,entriesab)
 write_changes(fileout,changes)

 
