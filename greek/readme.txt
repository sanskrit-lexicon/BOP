Insertion of Greek text into bop.txt

temp_bop_0.txt   latest from csl-orig:
$ cp /c/xampp/htdocs/cologne/csl-orig/v02/bop/bop.txt temp_bop_0.txt

temp_bop_ab_0.txt Andhrabharati's text
downloaded from link
 https://github.com/sanskrit-lexicon/csl-devanagari/issues/40#issuecomment-1115097913
cp ~/Downloads/BOP_main.txt greek/temp_bop_ab_0.txt

==============================================================
8961 matches for "^<L>" in buffer: temp_bop_ab_0.txt
8960 matches for "<L>" in buffer: temp_bop_0.txt
(* 2 8961) 17922

temp_bop_ab_1.txt
python ab_convert_1.py temp_bop_ab_0.txt temp_bop_ab_1.txt
19923 lines read from temp_bop_ab_0.txt
37845 records written to temp_bop_ab_1.txt

 1. unix line endings
 2. tab to \n
 
==============================================================
temp_bop_ab_1_slp1.txt : convert Devanagari to slp1.
cd transcode
python deva.py deva,slp1 ../temp_bop_ab_1.txt ../temp_bop_ab_1_slp1.txt
# check invertibility
python deva.py slp1,deva ../temp_bop_ab_1_slp1.txt temp.txt
diff ../temp_bop_ab_1.txt temp.txt | wc -l

# 4 should be 0   See issue #2
 
==============================================================
python prep1.py temp_bop_0.txt temp_bop_ab_1_slp1.txt temp_prep1.txt
57719 lines read from temp_bop_0.txt
8960 entries found
37845 lines read from temp_bop_ab_1_slp1.txt
8961 entries found

There is one more entry in ab version.
 '3593.1'  This is the cerebral nasal 'Ra' (slp1).
 bop_0 does not count as headword, but bop_ab does count as headword.
 Note that other letters are generally not counted as headwords.
 Solution:  comment out 3593.1

==============================================================
temp_bop_ab_2_slp1.txt  comment out entry 3593.1 (with semicolons)

python prep1.py temp_bop_0.txt temp_bop_ab_2_slp1.txt temp_prep1.txt
57719 lines read from temp_bop_0.txt
8960 entries found
37845 lines read from temp_bop_ab_2_slp1.txt
8960 entries found
in L not in Lab set()
in Lab not in L set()
check_metaline finds 282 differences
  many (all) are differences in 
==============================================================
temp_bop_1.txt pc corrections
  bop_ab changes <pc> in 200+ entries.
  These are typically where a new letter begins in the middle
  of a page.
  e.g. AM  shows as `<pc>027-a` in csl-orig bop, but `<pc>027-1a` in bop_ab.
 python make_change_1.py temp_bop_0.txt temp_bop_ab_2_slp1.txt change_1.txt
 279 changes written to change_1.txt

python updateByLine.py temp_bop_0.txt change_1.txt temp_bop_1.txt
279 transactions

python prep1.py temp_bop_1.txt temp_bop_ab_2_slp1.txt temp_prep1.txt
['k2: o, != o']
['k2: kinnu (kima + nu) != kinnu (kim + nu)']
['k2: viha, != viha']
check_metaline finds 3 differences

change_2.txt  manual (3 corrections to k2)
python updateByLine.py temp_bop_1.txt change_2.txt temp_bop_2.txt
3 change transactions
==============================================================
python prep1.py temp_bop_2.txt temp_bop_ab_2_slp1.txt temp_prep1.txt
741 Greek phrases in ab
278 entries with different number of greek phrases

==============================================================
change_3.txt  Greek phrases
  1 Greek phrase in bop entry and in bopab entry
python make_change_3.py temp_bop_2.txt temp_bop_ab_2_slp1.txt change_3.txt
371 changes written to change_3.txt
python updateByLine.py temp_bop_2.txt change_3.txt temp_bop_3.txt

==============================================================
change_3a.txt  Greek phrases
  Same number of greek changes in entry, but more than 1 greek phrase
python make_change_3a.py temp_bop_3.txt temp_bop_ab_2_slp1.txt change_3a.txt
327 changes written to change_3a.txt

python updateByLine.py temp_bop_3.txt change_3a.txt temp_bop_3a.txt


There is still a lot to do, about half.
876 matches in 670 lines for "<lang n="greek"></lang>" in buffer: temp_bop_3a.txt

==============================================================
131 matches in 94 lines for "<lang n="[^g]" in buffer: temp_bop_ab_2_slp1.txt

bopab: "Russian" -> "russian" to agree with one.dtd
  Arabic -> arabic
Avestan  one.dtd   Avestan font?  (old Persian right-to-left)
Slavonic  Font  (not under jIv not supported in my Emacs font set)
Lettish
L=7191  ?? in Arabic text (hw = vi)

temp_bop_4.txt  cases where non-greek in bopab

python diff_to_changes.py temp_bop_3a.txt temp_bop_4.txt change_4.txt
264 lines changed.
==============================================================
548 matches in 425 lines for ""></lang>" in buffer: temp_bop_4.txt
temp_bop_5.txt

Extract the records of bop_ab where there are 'empty' greek lang tags in bop_5.
To facilitate manual editing of temp_bop_5.txt.

python prep5.py temp_bop_4.txt temp_bop_ab_2_slp1.txt temp_bop_ab_prep5.org
181 entries marked with empty lang tags
Possible errors:
L=732 

These all manually changed in temp_bop_5.txt

==============================================================
python prep6.py temp_bop_5.txt temp_bop_ab_2_slp1.txt temp_prep6.org
check that lang phrases match bop_5 and bop_ab.

temp_bop_6.txt  corrections

temp_bop_ab_3_slp1.txt
"Russian" -> "russian"
"Arabic" -> "arabic"
python prep6.py temp_bop_6.txt temp_bop_ab_3_slp1.txt temp_prep6a.org
0 errors found.  All lang tags agree
==============================================================
temp_bop_7.txt   punctuation changes after </lang>
python make_change_7.py temp_bop_6.txt temp_bop_ab_3_slp1.txt change_7.txt
509 changes
python updateByLine.py temp_bop_6.txt change_7.txt temp_bop_7.txt

==============================================================
temp_bop_8.txt  Punctuation at end of markup
',#}' -> '#},'  and similarly for ';'
',%}' -> '%},'  and similarly for ';'

 
==============================================================
install into csl-orig and check validity
cp temp_bop_8.txt /c/xampp/htdocs/cologne/csl-orig/v02/bop/bop.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh bop  ../../bop
sh xmlchk_xampp.sh bop
  OK as hoped!
==============================================================
Prepare document for proofreading the greek.

This can be applied to different language names
python proof.py greek temp_bop_8.txt proof_greek.txt
==============================================================
trailing punctuation
python punct.py temp_bop_8.txt temp_bop_ab_3_slp1.txt change_9.txt
49 changes written to change_9.txt

python updateByLine.py temp_bop_8.txt change_9.txt temp_bop_9.txt


==============================================================
; change_10: manual one '?' after Greek were missed.
python updateByLine.py temp_bop_9.txt change_10.txt temp_bop_10.txt
1 change
==============================================================
install into csl-orig and check validity
cp temp_bop_10.txt /c/xampp/htdocs/cologne/csl-orig/v02/bop/bop.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh bop  ../../bop
sh xmlchk_xampp.sh bop
 # ok, as required.
 
cd /c/xampp/htdocs/sanskrit-lexicon/bop/greek

==============================================================
