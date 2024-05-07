#-*- coding:utf-8 -*-
"""bop_transcode.py
 04-29-2024
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def write_lines(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for line in lines:
   f.write(line+'\n')  
 print(len(lines),"written to",fileout)

def version1_convert_lines_AB_CDSL(lines):
 newlines = []
 for iline,line in enumerate(lines):
  if not line.startswith('<L>'):
   newlines.append(line)
  else:  
   parts = line.split('\t')
   """
   if len(parts) != 3:
    print(len(parts),'unexpected number of parts at line',iline+1)
    #print(line)
    newlines.append(line)
    continue
   """
   for part in parts:
    newlines.append(part)
   # one additional empty line
   newlines.append('')
 return newlines

def convert_lines_AB_CDSL(lines):
 newlines = []
 for iline,line in enumerate(lines):
  parts = line.split('\t')
  for part in parts:
   newlines.append(part)
 return newlines

def convert_lines_CDSL_AB(lines):
 #print('enter convert_lines_CDSL_AB',len(lines))
 newlines = []
 inentry = False
 for iline,line in enumerate(lines):
  dbg = False
  if dbg:print(iline+1,line[:40])
  if line.startswith('<L>'):
   inentry = True
   if dbg: print('case 0')
  if not inentry:
   newlines.append(line)
   if dbg: print('case 1')
   continue
  # in an entry
  if line.startswith('<L>'):
   # metaline
   group = [line]
   if dbg: print('case 2')
  elif line.startswith('<LEND>'):
   if dbg: print('case 4')
   prev = group.pop()  # remove previous
   new = '%s\t%s' % (prev,line)
   group.append(new)
   # output group
   for x in group:
    newlines.append(x)
   inentry = False
  elif lines[iline - 1].startswith('<L>'):
   # line after metaline
   group = ['%s\t%s' % (group[0],line)]
   if dbg: print('case 3')
  else:
   # a line in entry, except for metaline and <LEND>
   group.append(line)
   if dbg: print('case 5')
 return newlines

if __name__=="__main__":
 codein,codeout = sys.argv[1].split(',')
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx
 fileout = sys.argv[3] # 
 lines = read_lines(filein)
 print(len(lines),"read from",filein)
 if (codein,codeout) == ('AB','CDSL') :
  newlines = convert_lines_AB_CDSL(lines)
 elif (codein,codeout) == ('CDSL','AB') :
  newlines = convert_lines_CDSL_AB(lines)
 else:
  print('unknown options:%s' % sys.argv[1])
  exit(1)
 write_lines(fileout,newlines)
