# coding=utf-8
"""Carry changes from BOP_main-L2.txt file to bop.txt
    Author - Dr. Dhaval Patel
    email - drdhaval2785@gmail.com
    date - 16 January 2024
    Usage - python3 carry_change_from_single_line_to_printed_line.py basefile correctedfile outputfile
    e.g. - python3 carry_change_from_single_line_to_printed_line.py bop.txt BOP_main-L2.txt bop1.txt
"""
import sys
import os
import re
from indic_transliteration import sanscript


if __name__ == "__main__":
	basefile = sys.argv[1]
	correctedfile = sys.argv[2]
	outputfile = sys.argv[3]
	bsin = open(basefile, 'r')
	cin = open(correctedfile, 'r')
	tempout = open('bop_temp.txt', 'w')
	fout = open(outputfile, 'w')
	dt = ''
	for lin in bsin:
		if lin.startswith('<L>'):
			dt = lin.rstrip() + '\t'
			print(lin)
		elif lin.startswith('<LEND>'):
			dt += '\t' + lin.rstrip() + '\n'
			dt = re.sub('[ ]+', ' ', dt)
			dt = dt.replace(' \t', '\t')
			dt = dt.replace('- ', '-')
			tempout.write(dt + '\n')
		elif lin.rstrip() != '':
			dt += lin.rstrip() + ' '

