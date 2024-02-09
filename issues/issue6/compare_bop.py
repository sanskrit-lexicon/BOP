# coding=utf-8
"""Compare csl-orig/v02/bop/bop.txt to BOP_main-L2.txt
    Author - Dr. Dhaval Patel
    email - drdhaval2785@gmail.com
    date - 09 February 2024
    Usage - python3 compare_bop.py basefile correctedfile outputfile
    e.g. - python3 compare_bop.py bop.txt BOP_main-L2.txt bop1.txt
"""
import sys
import os
import re
from indic_transliteration import sanscript



def prepare_bop_oneline(bop, bop1):
	fin = open(bop, 'r')
	fout = open(bop1, 'w')
	data = ''
	for lin in fin:
		lin = lin.rstrip()
		if lin.startswith('<L>'):
			data += lin + '\t'
		elif lin.startswith('<LEND>'):
			data += lin + '\n'
		else:
			data += lin + '🞄'
	fout.write(data)
	fin.close()
	fout.close()
	
	fin1 = open(bop1, 'r')
	data1 = fin1.read()
	fin1.close()
	fout1 = open(bop1, 'w')
	data1 = data1.replace('🞄<LEND>', '\t<LEND>')
	data1 = data1.replace('🞄<L>', '<L>')
	data1 = data1.replace('-🞄', '')
	data1 = data1.replace('🞄', ' 🞄')
	fout1.write(data1)
	fout1.close()


if __name__ == "__main__":
	bop = 'bop.txt'
	bop1 = 'bop1.txt'
	prepare_bop_oneline(bop, bop1)

	
	
