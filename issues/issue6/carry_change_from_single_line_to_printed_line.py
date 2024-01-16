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
			print(lin)
		elif lin.startswith('<LEND>'):
			dt += '\t' + lin.rstrip() + '\n'
			dt = re.sub('[ ]+', ' ', dt)
			dt = dt.replace(' \t', '\t')
			dt = dt.replace('- ', '-')
			dt = re.sub('([0-9])[ ]*[.][ ]*([0-9])', '\g<1>.\g<2>', dt)
			dt = dt.replace('-#} {#', '')
			dt = re.sub('([a-zA-Z])[\-]([a-zA-Z])', '\g<1>\g<2>', dt)
			tempout.write(dt + '\n')
		elif lin.rstrip() != '':
			dt += lin.rstrip() + ' '




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


if __name__ == "__main__":
	#prepare_temp()

	# bop_temp.txt
	a = '<L>4249<pc>176-b<k1>द्यु<k2>द्यु	{#द्यु#}¦ 2. {%P.%} {#द्यौमि#} ({#अभिगमने#} {%K.%} {#अभिसर्पणे#} {%V.%}) aggredi. BHATT. 6.18.: {#सिंहो मृगन् द्युवन्#} (cf. {#द्रु#}, unde {#द्यु#} ortum esse videtur mutatâ semivocali {#र्#} in {#य्#}; v. gr. comp. §. 20.). --{#द्यु#} splendere {%in dial. Vêd. ortum est%} e {#दिव्#} {%mutato%} {#व्#} in {#उ#}.	<LEND>'
	# BOP_main-L2.txt
	b = '<L>4249<pc>176-b<k1>द्यु<k2>द्यु	{#द्यु#}¦ 2. {%P.%} {#द्यौमि#} ({#अभिगमने#} {%K.%} {#अभिसर्पणे#} {%V.%}) aggredi. BHATT. 6.18.: {#सिंहो   मृगन् द्युवन्#} (cf. {#द्रु#}, unde {#द्यु#} ortum esse videtur mutatâ semivocali {#र्#} in {#य्#}; v. gr. comp. §. 20.). — {#द्यु#} splendere {%in dial. Vêd. ortum est%} e {#दिव्#} {%mutato%} {#व्#} in {#उ#}.	<LEND>'
	print(inline_diff(a, b))
