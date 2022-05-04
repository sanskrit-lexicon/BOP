#-*- coding:utf-8 -*-
"""prep5.py
 
"""
from __future__ import print_function
import sys,re,codecs
import digentry  


def write(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for iline,line in enumerate(lines):
   f.write(line+'\n')
 print(len(lines),"records written to",fileout)

def check_entries_L(Ldict,Ldictab):
 s = set(Ldict.keys())
 sab = set(Ldictab.keys())
 diff1 = s.difference(sab)
 print('in L not in Lab',diff1)
 diff2 = sab.difference(s)
 print('in Lab not in L',diff2)

def check_metaline(entries,entriesab):
 nprob = 0
 for ientry,entry in enumerate(entries):
  entryab = entriesab[ientry]
  if entry.metaline != entryab.metaline:
   lnum = entry.linenum1
   print('%s old %s' %(lnum,entry.metaline))
   print('%s new %s' %(lnum,entryab.metaline))
   print(';')
   nprob = nprob + 1
   continue
   # rest of code not needed
   keys = list(entry.metad.keys())
   keysab = list(entryab.metad.keys())
   assert keys == keysab
   diffvals = []
   for key in keys:
    val = entry.metad[key]
    valab = entryab.metad[key]
    if val != valab:
     diffvals.append('%s: %s != %s' %(key,val,valab))
   print(diffvals)
   #print('%s != %s' %(entry.metaline ,entryab.metaline))
   nprob = nprob + 1
 print('check_metaline finds %s differences' % nprob)

def empty_lang(entry):
 a = []
 for line in entry.datalines:
  b = re.findall(r'></lang>',line)
  for x in b:
   a.append(x)
 return not (a == [])
 
def mark_ab(entries,entriesab):
 nprob = 0
 for ientry,entry in enumerate(entries):
  entryab = entriesab[ientry]
  assert entry.metaline == entryab.metaline
  flag = empty_lang(entry)
  if flag:
   entryab.keep = True
   nprob = nprob + 1
  else:
   entryab.keep = False
 print(nprob,'entries marked with empty lang tags')

def write_marked(entriesab,fileout):
 nout = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for entry in entriesab:
   if not entry.keep:
    continue
   nout = nout + 1
   outarr = []
   outarr.append('* TODO %s' % entry.metaline)
   for line in entry.datalines:
    outarr.append(line)
   outarr.append(entry.lend)
   for out in outarr:
    f.write(out+'\n')
 print(nout,"records written to",fileout)
 
if __name__=="__main__":
 filein = sys.argv[1] # bop csl-orig
 fileab = sys.argv[2] # bop ab
 fileout = sys.argv[3] #  

 entries = digentry.init(filein)
 Ldict = digentry.Entry.Ldict
 digentry.Entry.Ldict = {}
 entriesab = digentry.init(fileab)
 Ldictab = digentry.Entry.Ldict

 #check_entries_L(Ldict,Ldictab)
 #check_metaline(entries,entriesab)
 mark_ab(entries,entriesab)
 write_marked(entriesab,fileout)

 
