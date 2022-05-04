#-*- coding:utf-8 -*-
"""make_change_1.py
 
"""
from __future__ import print_function
import sys,re,codecs
import digentry  

class Change(object):
 def __init__(self,lnum,line,newline,page):
  self.lnum = lnum
  self.line = line
  self.newline = newline
  self.page = page

def write_changes(fileout,changes):
 outrecs=[]
 for change in changes:
  outarr=[]
  lnum = change.lnum
  line = change.line
  page = change.page
  newline = change.newline
  outarr.append(';Page %s' % page)
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

def make_changes(entries,entriesab):
 changes = []
 for ientry,entry in enumerate(entries):
  entryab = entriesab[ientry]
  key = 'pc'
  val = entry.metad[key]
  valab = entryab.metad[key]
  if val == valab:
   continue
  lnum = entry.linenum1
  line = entry.metaline
  oldpc = '<pc>%s' % val
  newpc = '<pc>%s' % valab
  newline = line.replace(oldpc,newpc)
  page = val # not needed
  change = Change(lnum,line,newline,page)
  changes.append(change)
 return changes

if __name__=="__main__":
 filein = sys.argv[1] # bop csl-orig
 fileab = sys.argv[2] # bop ab
 fileout = sys.argv[3] #  

 entries = digentry.init(filein)
 #Ldict = digentry.Entry.Ldict
 digentry.Entry.Ldict = {}
 entriesab = digentry.init(fileab)
 #Ldictab = digentry.Entry.Ldict

 changes = make_changes(entries,entriesab)
 write_changes(fileout,changes)

 
