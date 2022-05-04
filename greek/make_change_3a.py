#-*- coding:utf-8 -*-
"""make_change_3.py
 
"""
from __future__ import print_function
import sys,re,codecs
import digentry  

class Change(object):
 def __init__(self,lnum,line,newline,metaline,ngreeks):
  self.lnum = lnum
  self.line = line
  self.newline = newline
  self.metaline = metaline
  self.ngreeks = ngreeks
  
def write_changes(fileout,changes):
 outrecs=[]
 prevmeta = None
 for change in changes:
  outarr=[]
  lnum = change.lnum
  line = change.line
  newline = change.newline
  metaline = change.metaline
  metaline = re.sub(r'<k2>.*$','',metaline)
  if prevmeta != metaline:
   outarr.append('; --------------------------------------------------')
   outarr.append('; %s (%s greek phrases in entry)' % (metaline,change.ngreeks))
  else:
   outarr.append(';')
  prevmeta = metaline
  outarr.append('%s old %s' %(lnum,line))
  outarr.append('%s new %s' %(lnum,newline))
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

def greek_instances(entry,case='ab'):
 a = []
 for line in entry.datalines:
  if case == 'ab':
   b = re.findall(r'<lang n="greek">.*?</lang>',line)
  else:
   b = re.findall(r'<lang n="greek"></lang>',line)  
  for x in b:
   a.append(x)
 return a

def make_changes(entries,entriesab):
 changes = []
 for ientry,entry in enumerate(entries):
  entryab = entriesab[ientry]
  greeks = greek_instances(entry,case='csl')
  greeksab = greek_instances(entryab,case='ab')
  if len(greeksab) == 0:
   continue
  if len(greeks) != len(greeksab):
   continue
  if len(greeks) == 1:
   continue  # already handled by make_change_3.py
  #print('chk:',entry.metaline)
  igreek = 0
  text = '\n'.join(entry.datalines)
  parts = re.split('(<lang n="greek"></lang>)',text,flags = re.DOTALL)
  newparts = []
  for part in parts:
   if part == '<lang n="greek"></lang>':
    newpart = greeksab[igreek]
    igreek = igreek + 1
   else:
    newpart = part
   newparts.append(newpart)
  if igreek != len(greeksab):
   print('skipping problem at ',entry.metaline)
   continue
  newtext = ''.join(newparts)
  newlines = newtext.split('\n')
  oldlines = entry.datalines
  assert len(newlines) == len(oldlines)
  for iline,newline in enumerate(newlines):
   oldline = oldlines[iline]
   if oldline == newline:
    continue
   lnum = entry.linenum1 + iline + 1
   line = oldline
   metaline = entry.metaline
   ngreeks = len(greeks)
   change = Change(lnum,line,newline,metaline,ngreeks)
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

 
