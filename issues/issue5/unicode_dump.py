# coding=utf-8
""" 
unicode_dump.py 
"""
from __future__ import print_function
import sys, re,codecs
import unicodedata

def select(entries):
 nfound = 0
 text = 'slav.'
 for entry in entries:
  grlines = []
  for line in entry.datalines:
   if text in line:
    grlines.append(line)
  # add attribute to the entry
  entry.grlines = grlines
  if grlines != []:
   nfound = nfound + 1
   # assert len(grlines) == 1
 print('select %s entries matching "%s"' %(nfound,text))

def unicode_dump(line):
 outarr = []
 outarr.append(line)
 if line.startswith(';'):
  return outarr
 if line.strip() == '':
  return outarr
 words = re.split('[\t ]',line)
 for word in words:
  outarr.append('%s :' % word)
  for c in word:
   ic = ord(c)
   name = unicodedata.name(c)
   out = '   %s %04x %s' %(c,ic,name)
   outarr.append(out)
  outarr.append('')
 return outarr

def write(fileout,outrecs):
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
if __name__=="__main__":
 filein = sys.argv[1] # any text file
 fileout = sys.argv[2] # text output
 # read all the entries of the dictionary.
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 outrecs = [unicode_dump(line) for line in lines]
 
 write(fileout,outrecs)
