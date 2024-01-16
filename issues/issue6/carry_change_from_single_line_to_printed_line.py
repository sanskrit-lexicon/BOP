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


def prepare_temp():
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
			#print(lin)
		elif lin.startswith('<LEND>'):
			dt = dt.rstrip()
			dt += '\t' + lin
			dt = re.sub('[ ]+', ' ', dt)
			dt = dt.replace(' \t', '\t')
			dt = dt.replace('-\n', '')
			dt = dt.replace('\n', ' ')
			dt = re.sub('[ ]+', ' ', dt)
			#dt = re.sub('([0-9])[ ]*[.][ ]*([0-9])', '\g<1>.\g<2>', dt)
			dt = dt.replace('-#} {#', '')
			dt = dt.replace('#}\n{#', ' ')
			dt = re.sub('([a-zA-Z])[\-]([a-zA-Z])', '\g<1>\g<2>', dt)
			#dt = dt.replace('<div', '\n<div')
			#dt = re.sub('<F>', '\n<F>', dt)
			#dt = re.sub('[ ]*infr[.]', 'infr.', dt)
			dt = dt.rstrip()
			tempout.write(dt + '\n')
		elif lin.rstrip() != '':
			dt += lin


def prep_AB():
	filein = 'BOP_main-L2.txt'
	fileout = 'bop_L2_temp.txt'
	fin = open(filein, 'r')
	fout = open(fileout, 'w')
	data = fin.read()
	data = data.replace('\r\n', '\n')
	data = re.sub('\n([^\n])', ' \g<1>', data)
	data = data.replace(' <L>', '<L>')
	fout.write(data)
	fin.close()
	fout.close()


def inline_diff(a, b):
    import difflib
    matcher = difflib.SequenceMatcher(None, a, b)
    def process_tag(tag, i1, i2, j1, j2):
        if tag == 'replace':
            return (matcher.a[i1-5:i2+5], matcher.b[j1-5:j2+5])
        if tag == 'delete':
            return (matcher.a[i1-5:i1] + matcher.a[i1:i2] + matcher.a[i2:i2+5], matcher.a[i1-5:i1] + matcher.a[i2:i2+5])
        if tag == 'equal':
            return ''
        if tag == 'insert':
            return (matcher.a[i1-5:i1] + matcher.a[i1:i2] + matcher.a[i2:i2+5], matcher.a[i1-5:i1] + matcher.a[i1:i2] + matcher.b[j1:j2] + matcher.a[i2:i2+5])
        assert False, "Unknown tag %r"%tag
    result = []
    for t in matcher.get_opcodes():
        result.append(process_tag(*t))
    result = [x for x in result if x != '']
    return result


def prep_replacements(base, AB):
	fin1 = open(base, 'r')
	fin2 = open(AB, 'r')
	dict1 = {}
	dict2 = {}
	for lin1 in fin1:
		[meta1, text1, lend1] = lin1.split('\t')
		#print(meta1)
		x1 = re.search('<L>(.*)?<pc>', meta1)
		lnum1 = x1.group(1)
		dict1[lnum1] = text1
	for lin2 in fin2:
		[meta2, text2, lend2] = lin2.split('\t')
		x2 = re.search('<L>(.*)?<pc>', meta2)
		lnum2 = x2.group(1)
		dict2[lnum2] = text2
	rep_dict = {}
	for x in dict1:
		a = dict1[x]
		b = dict2[x]
		#print(x)
		y = inline_diff(a, b)
		#print(y)
		#print()
		if len(y) > 0:
			rep_dict[x] = y
	return rep_dict


def apply_rep_to_bop(bop, newbop, rep_dict):
	fin = open(bop, 'r')
	fout = open(newbop, 'w')
	lnum = '1'
	blob = ''
	for lin in fin:
		p = re.search('<L>(.*)?<pc>', lin)
		q = re.search('<LEND>', lin)
		if p:
			blob = lin
			lnum = p.group(1)
			q = False
		if not q:
			blob += lin
		if q:
			blob += lin
			if lnum in rep_dict:
				for (a, b) in rep_dict[lnum]:
					if a in blob:
						blob.replace(a, b)
						print(lnum, 'REPLACE', a, b)
					else:
						print(lnum, 'MANUAL', a, b)
			fout.write(blob)


if __name__ == "__main__":
	prepare_temp()
	prep_AB()
	rep_dict = prep_replacements('bop_temp.txt', 'bop_L2_temp.txt')
	#print(rep_dict)
	apply_rep_to_bop('bop.txt', 'bop1.txt', rep_dict)

	# bop_temp.txt
	a = '<L>4249<pc>176-b<k1>द्यु<k2>द्यु	{#द्यु#}¦ 2. {%P.%} {#द्यौमि#} ({#अभिगमने#} {%K.%} {#अभिसर्पणे#} {%V.%}) aggredi. BHATT. 6.18.: {#सिंहो मृगन् द्युवन्#} (cf. {#द्रु#}, unde {#द्यु#} ortum esse videtur mutatâ semivocali {#र्#} in {#य्#}; v. gr. comp. §. 20.). --{#द्यु#} splendere {%in dial. Vêd. ortum est%} e {#दिव्#} {%mutato%} {#व्#} in {#उ#}.	<LEND>'
	# BOP_main-L2.txt
	b = '<L>4249<pc>176-b<k1>द्यु<k2>द्यु	{#द्यु#}¦ 2. {%P.%} {#द्यौमि#} ({#अभिगमने#} {%K.%} {#अभिसर्पणे#} {%V.%}) aggredi. BHATT. 6.18.: {#सिंहो   मृगन् द्युवन्#} (cf. {#द्रु#}, unde {#द्यु#} ortum esse videtur mutatâ semivocali {#र्#} in {#य्#}; v. gr. comp. §. 20.). — {#द्यु#} splendere {%in dial. Vêd. ortum est%} e {#दिव्#} {%mutato%} {#व्#} in {#उ#}.	<LEND>'
	#print(inline_diff(a, b))
