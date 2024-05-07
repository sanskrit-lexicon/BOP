#-*- coding:utf-8 -*-
"""bop_transcode.py
 04-29-2024
"""
from __future__ import print_function
import sys, re,codecs
import transcoder
transcoder.transcoder_set_dir('transcoder')

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def write_lines(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for line in lines:
   f.write(line+'\n')  
 print(len(lines),"written to",fileout)

def convert(line,tranin,tranout):
 # convert text  in '<s>X</s>'
 tagname = 's'
 def f(m):
  x = m.group(1)
  y = transcode(x,tranin,tranout)
  return '{#%s#}' % y

 regex = '{#(.*?)#}'
 lineout = re.sub(regex,f,line)
 return lineout

def transcode(x,tranin,tranout):
 y = transcoder.transcoder_processString(x,tranin,tranout)
 return y

def convert_metaline(line,tranin,tranout):
 # '<k1>X<k2>Y'
 m = re.search('<k1>([^<]+)<k2>([^<]+)',line)
 x = m.group(0)  # entire match
 k1 = m.group(1)
 k2 = m.group(2)
 #k1a =transcoder.transcoder_processString(k1,tranin,tranout)
 #k2a =transcoder.transcoder_processString(k2,tranin,tranout)
 k1a = transcode(k1,tranin,tranout)
 k2a = transcode(k2,tranin,tranout)
 y = '<k1>%s<k2>%s' %(k1a,k2a)
 lineout = line.replace(x,y)
 return lineout

def convert_lines(lines,tranin,tranout):
 newlines = []
 for iline,line in enumerate(lines):
  if line.startswith('<L>'):
   newline = convert_metaline(line,tranin,tranout)
  else:
   newline = convert(line,tranin,tranout)
  newlines.append(newline)
 return newlines

if __name__=="__main__":
 #test()
 #test1()
 tranin = sys.argv[1]
 tranout = sys.argv[2]
 filein = sys.argv[3] #  xxx.txt (path to digitization of xxx
 fileout = sys.argv[4] # 
 lines = read_lines(filein)
 newlines = convert_lines(lines,tranin,tranout)
 write_lines(fileout,newlines)
