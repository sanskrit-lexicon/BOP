# 04-29-2024

This directory in local installation:
cd /c/xampp/htdocs/sanskrit-lexicon/bop/issues/issue6/cdsl

python bop_transcode.py deva slp1 ../bop.txt bop_slp1.txt
# check invertibility
python bop_transcode.py slp1 deva bop_slp1.txt temp_bop_slp1_deva.txt
diff ../bop.txt temp_bop_slp1_deva.txt | wc -l
# 0 As expected.
rm temp_bop_slp1_deva.txt  # no further use

------------------------------------------
temp_bop_0.txt  cdsl-orig version as of 04-29-2024
  commit 4fde1c49c7329b28400878876b50ae2a03902cd3
cd /c/xampp/htdocs/cologne/csl-orig
git show 4fde1c49:v02/bop/bop.txt > /c/xampp/htdocs/sanskrit-lexicon/bop/issues/issue6/cdsl/temp_bop_0.txt

57719 temp_bop_0.txt
------------------------------------------
../bop_L2_temp.txt  has each entry on one line, 3 'fields' tab-separated
and 
To convert this to 'standard' 3-line cdsl form

python cdsl_AB.py AB,CDSL ../BOP_main-L2.txt BOP_main-L2_cdsl.txt
19922 read from ../BOP_main-L2.txt
37844 written to BOP_main-L2_cdsl.txt

python cdsl_AB.py CDSL,AB  BOP_main-L2_cdsl.txt  BOP_main-L2_cdsl_AB.txt
17921 written to BOP_main-L2_cdsl_AB.txt
37844 read from BOP_main-L2_cdsl.txt
19922 written to BOP_main-L2_cdsl_AB.txt


diff -w ../BOP_main-L2.txt BOP_main-L2_cdsl_AB.txt | wc -l
# 0
Note: '-w' flag used because there are some windows line-endings in
    ../BOP_main-L2.txt

rm BOP_main-L2_cdsl_AB.txt  # no need for this

-------------------------------------------------
BOP_main-L2_cdsl.txt has devanagari. Convert to slp1
python bop_transcode.py deva slp1 BOP_main-L2_cdsl.txt temp_bop_1_ab.txt
37844 written to temp_bop_1_ab.txt

# invertibility check

python bop_transcode.py slp1 deva temp_bop_1_ab.txt temp.txt
diff BOP_main-L2_cdsl.txt temp.txt | wc -l
0 # as expected.
rm temp.txt
-------------------------------------------------
manually get the 'main' section of temp_bop_0.txt
cp temp_bop_0.txt temp_bop_0a.txt
edit temp_bop_0a.txt
Remove lines (a) before first <L> and (b) after last <LEND>
 wc -l temp_bop_?.txt
  57719 temp_bop_0.txt
  57226 temp_bop_0a.txt  # removed about 500 lines
------------------------------------------------------------
temp_bop_0a.txt and temp_bop_1_ab.txt are now comparable.
Begin to analyze differences
------------------------------------------------------------
Compare metalines
grep -E '^<L>' temp_bop_0a.txt > temp_metalines.txt
grep -E '^<L>' temp_bop_1_ab.txt > temp_metalines_ab.txt

AB has 1 additional headword:
3594a3595
> <L>3593.1<pc>146-2a<k1>R<k2>R
This is AB's entry 
<L>3593.1<pc>146-2a<k1>R<k2>R
{#Ra#}¦ {%De radicibus, quae apud grammaticos a linguali nasali%} {#R#} {%incipiunt v. gr.%} 109.
<LEND>

cdsl has <P>{%De radicibus, quae apud grammaticos a linguali nasali%} {#R#} {%incipiunt v. gr.%} 109.

Manually adjust  temp_bop_1.txt to agree with AB 3593.1

Now, temp_bop_1.txt and temp_bop_1_ab.txt have identical meta-lines sequences.
--------------------------------------------------------------------
sh redolocal.sh X
 uses temp_bop_X.txt to generate apps/X
 display url:
 http://localhost/sanskrit-lexicon/BOP/issues/issue6/cdsl/apps/X/web/
 
--------------------------------------------------------------------

sh redolocal.sh 1_ab
  This gives an error.

cp temp_bop_1_ab.txt  temp_bop_1a_ab.txt
edit temp_bop_1a_ab.txt

With that one change:
sh redolocal.sh 1a_ab
 gives no errors

Note: The 'apps' directory is not tracked by git,
 due to .gitignore file within this cdsl directory.
--------------------------------------------------------
NOTE on GREP: grep -R --include=*.py 'import diff'
in /c/xampp/htdocs/sanskrit-lexicon/pwk/pwkissues

issue102/step2/alldiff.py: import difflib

--------------------------------------------------------
cd cmp
python alldiff.py ../temp_bop_1.txt ../temp_bop_1a_ab.txt temp_alldiff.txt

8961 entries found
37844 lines read from ../temp_bop_1a_ab.txt
8961 entries found
2541 entries the same
6420 entries differ

--------------------------------------------------------------------
many of the diffs are due to an extra space in cdsl.
Example: (AB) Br. 1.16.  (CDSL) Br. 1. 16.

python cmp_auth.py 1 ../abbrevs/bopauth.txt ../temp_bop_1.txt ../temp_bop_1a_ab.txt temp_cmp_auth_1.txt
Search for ' NA ' in temp_cmp_auth_1.txt
These are cases where AB has 'upcased' an auth abbrev.
36 found.

cp ../temp_bop_1.txt ../temp_bop_1a.txt
and make manual changes to temp_bop_1a.

<L>3157<pc>123-a<k1>  GAT. 1. -> GHAT. 1.  print change
<L>3575<pc>145-1b<k1>wOk BHAT. -> BHATT.  print change
<L>5310<pc>224-b<k1>pota  75. 4. -> HIT. 75. 4. print change
<L>4352<pc>180-b<k1>DA BHAT. 5.32. -> BHATT. 5.32.  print change
<L>6348<pc>271-a<k1>mfdu AGHR. -> RAGH. print change

# rerun, using temp_bop_1a.txt
python cmp_auth.py 1 ../abbrevs/bopauth.txt ../temp_bop_1a.txt ../temp_bop_1a_ab.txt temp_cmp_auth_1_a.txt
8 items with NA (LS ABBREV misalign)

more changes to temp_bop_1a.txt

# rerun, using revised temp_bop_1a.txt
python cmp_auth.py 1 ../abbrevs/bopauth.txt ../temp_bop_1a.txt ../temp_bop_1a_ab.txt temp_cmp_auth_1_b.txt
Now there are no 'NA' -- So the two files agree with the sequence of auths.

-----------------------------------------------------
# make new version temp_bop_1b.txt

X. 1. 23. -> X. 1.23.  for author-abbreviations X
python cmp_auth.py 2 ../abbrevs/bopauth.txt ../temp_bop_1a.txt ../temp_bop_1a_ab.txt ../temp_bop_1b.txt

cd ../  #cdsl
python diff_to_changes_dict.py temp_bop_1a.txt temp_bop_1b.txt change_bop_1a_1b.txt
5308 changes written to change_bop_1a_1b.txt

# for information,
python cmp_auth.py 1 ../abbrevs/bopauth.txt ../temp_bop_1b.txt ../temp_bop_1a_ab.txt temp_cmp_auth_1_b2.txt
34 lines read from ../abbrevs/bopauth.txt
34 auth abbreviations from file ../abbrevs/bopauth.txt
57230 lines read from ../temp_bop_1b.txt
37844 lines read from ../temp_bop_1a_ab.txt
18368 groups 8961 entries
17921 groups 8961 entries
7874 entries the same
1087 entries differ
6259 written to temp_cmp_auth_1_b2.txt

-----------------------------------------------------
new version temp_bop_1c.txt

auths diffs over line break
Example:
OLD:
{#aMSa#}¦ {%m.%} (r. {#aMS#} s. {#a#}) 1) pars, portio. 2) humerus. SAK.
22. 6. infr. (cf. germ. vet. {%ahsala%}, lat. {%axilla%}, v. sq,
NEW:
{#aMSa#}¦ {%m.%} (r. {#aMS#} s. {#a#}) 1) pars, portio. 2) humerus. SAK. 22. 6.
infr. (cf. germ. vet. {%ahsala%}, lat. {%axilla%}, v. sq,

python cmp_auth.py 3 ../abbrevs/bopauth.txt ../temp_bop_1b.txt ../temp_bop_1a_ab.txt ../temp_bop_1c.txt
7874 entries the same
1087 entries differ
1076 entries changed
57230 written to ../temp_bop_1c.txt

cd ../
python diff_to_changes_dict.py temp_bop_1b.txt temp_bop_1c.txt change_bop_1b_1c.txt
5705 changes written to change_bop_1b_1c.txt

----------------------------------------------------
# new version temp_bop_1d.txt


-----------------------------------------------------
next version temp_bop_1d.txt
cd ../
cp temp_bop_1c.txt temp_bop_1d.txt

ITERATE:
python cmp_auth.py 1 ../abbrevs/bopauth.txt ../temp_bop_1d.txt ../temp_bop_1a_ab.txt temp_cmp_auth_1_d2.txt

manual edit temp_bop_1d.txt (in light of temp_cmp_auth_1_c2.txt)
UNTIL 0  entries differ
-----------------

python diff_to_changes_dict.py temp_bop_1c.txt temp_bop_1d.txt change_bop_1c_1d.txt
519 changes written to change_bop_1c_1d.txt
-----------------------------------------------------
create temp_bop_1e.txt
auth = 'R. Schl.'
 Typical 'R. Schl. Z.2.3.'  where 'Z' is
   cdsl often has 'R.Schl. I. 2. 3.'  OR 'R.Schl. I. 2.3.'
 A few:  'R. Schl. 23.10'.
   cdsl often has 'R. Schl. 23. 10'

Similar:
 PAN. R.N.N.  R = uppercase [IV]+
 RAM. ed. Ser.
 RAM. Schl. R. N. N.
 RAM.
 GITA-GOV. N. N.
 Pott. N. N. 
 Graff N. N.
 
# python cmp_auth.py 3 ../abbrevs/bopauth.txt ../temp_bop_1d.txt ../temp_bop_1a_ab.txt ../temp_bop_1d.txt

cp temp_bop_1d.txt temp_bot_1e.txt

ITERATE:
python cmp_auth.py 4 ../abbrevs/bopauth.txt ../temp_bop_1e.txt ../temp_bop_1a_ab.txt temp_cmp_auth_1_e2.txt

manual edit temp_bop_1e.txt (in light of temp_cmp_auth_1_e2.txt)
UNTIL 0  entries differ

Emacs regex replacements:
R\. Schl\. \([0-9IV]+\)\. ?\([0-9]+\)\. ?\([0-9]+\)\. → R. Schl. \1.\2.\3.
replaced 581 occurrences

---------------
# rerun alldiff.py with version 1e
python alldiff.py ../temp_bop_1e.txt ../temp_bop_1a_ab.txt temp_alldiff_1e.txt

17921 groups 8961 entries
4988 entries the same
3973 entries differ  
3973 written to temp_alldiff_1e.txt
(compare to 6420 entries differ with temp_bop_1.txt)

-------------------
python diff_to_changes_dict.py temp_bop_1d.txt temp_bop_1e.txt change_bop_1d_1e.txt
1427 changes written to change_bop_1d_1e.txt
--------------------------------------------------------
Now, work on hyphens at end of lines
--------------------------------------------------------
2908 matches for "-$" in buffer: temp_bop_1e.txt
2144 matches for "-#}$" in buffer: temp_bop_1e.txt
431 matches for "-%}$" in buffer: temp_bop_1e.txt
--------------------------------------------------------
temp_bop_2a.txt
2908 matches for "-$" in buffer: temp_bop_1e.txt
# construct temp_bop_2a.txt
# lines ending in '-'
python hyphen_merge.py 1 ../temp_bop_1e.txt ../temp_bop_2a.txt

57230 lines read from ../temp_bop_1e.txt
18368 groups 8961 entries
8961 entries
1975 entries changed
57230 written to ../temp_bop_2a.txt

# construct change file
python diff_to_changes_dict.py temp_bop_1e.txt temp_bop_2a.txt change_bop_1e_2a.txt
5550 changes written to change_bop_1e_2a.txt

# rerun alldiff.py with version 2a
python alldiff.py ../temp_bop_2a.txt ../temp_bop_1a_ab.txt temp_alldiff_2a.txt

18368 groups 8961 entries
17921 groups 8961 entries
5995 entries the same
2966 entries differ
2966 written to temp_alldiff_2a.txt

So this reduced the differing entries by 1000!

--------------------------------------------------------
temp_bop_2b.txt
2144 matches for "-#}$" in buffer: temp_bop_1e.txt
# construct temp_bop_2a.txt
# lines ending in '-#}'
python hyphen_merge.py 2 ../temp_bop_2a.txt ../temp_bop_2b.txt

57230 lines read from ../temp_bop_2a.txt
18368 groups 8961 entries
8961 entries
696 entries changed
57230 written to ../temp_bop_2b.txt

# construct change file
python diff_to_changes_dict.py temp_bop_2a.txt temp_bop_2b.txt change_bop_2a_2b.txt
3970 changes written to change_bop_2a_2b.txt

# rerun alldiff.py with version 2b
python alldiff.py ../temp_bop_2b.txt ../temp_bop_1a_ab.txt temp_alldiff_2b.txt

18368 groups 8961 entries
17921 groups 8961 entries
6103 entries the same
2858 entries differ
2858 written to temp_alldiff_2b.txt

So this reduced the differing entries by only 100+

--------------------------------------------------------
temp_bop_2c.txt
431 matches for "-%}$" in buffer: temp_bop_1e.txt

# construct temp_bop_2c.txt
# lines ending in '-#}'
python hyphen_merge.py 3 ../temp_bop_2b.txt ../temp_bop_2c.txt

57230 lines read from ../temp_bop_2b.txt
18368 groups 8961 entries
8961 entries
347 entries changed
57230 written to ../temp_bop_2c.txt

# construct change file
python diff_to_changes_dict.py temp_bop_2b.txt temp_bop_2c.txt change_bop_2b_2c.txt
831 changes written to change_bop_2b_2c.txt

# rerun alldiff.py with version 2c
python alldiff.py ../temp_bop_2c.txt ../temp_bop_1a_ab.txt temp_alldiff_2c.txt
18368 groups 8961 entries
17921 groups 8961 entries
6174 entries the same
2787 entries differ
2787 written to temp_alldiff_2c.txt

So this reduced the differing entries by only 70+

--------------------------------------------------------
temp_bop_3a.txt
cp ../temp_bop_2c.txt ../temp_bop_3a.txt

miscellaneous edits to ../temp_bop_3a.txt,
  guided by cases in temp_alldiff_2x.txt

---
'. infr.' -> '.infr.'  What is the abbreviation here? AB: 'infr.' = infra
'.\ninfr. ' -> '.infr.\n'
'.\ninfr.' -> '.infr.\n'


cp alldiff.py alldiff1.py
There are now empty lines in entries. Alter alldiff1.py accordingly
python alldiff1.py ../temp_bop_3a.txt ../temp_bop_1a_ab.txt temp_alldiff1_3a.txt
2706 written to temp_alldiff_3a.txt
2224 written to temp_alldiff1_3a.txt

 So that solves almost 500 of the alleged differences

-------------------------------------
795 matches in 787 lines for "--" in buffer: temp_bop_3a.txt
878 matches in 628 lines for "—" in buffer: temp_bop_1a_ab.txt

temp_bop_1a_ab.txt has no '--'.

Manually change '--' to '—' in temp_bop_3a.txt
python alldiff1.py ../temp_bop_3a.txt ../temp_bop_1a_ab.txt temp_alldiff1_3a.txt
2179 written to temp_alldiff1_3a.txt

--------------------
639 matches in 609 lines for "{%V\.%}" in buffer: temp_bop_1a_ab.txt
563 matches in 555 lines for "{%V\.%}" in buffer: temp_bop_3a.txt
111 matches in 109 lines for "{%v\.%}" in buffer: temp_bop_1a_ab.txt
192 matches for "{%v\.%}" in buffer: temp_bop_3a.txt

699 matches for " 0$" in buffer: temp_alldiff1_3a.txt
These are cases where the number of characters in entries is the same for 3a and 1a_ab.

python cmp_misc.py 1 ../temp_bop_3a.txt ../temp_bop_1a_ab.txt ../temp_bop_3b.txt

117 entries changed
57230 written to ../temp_bop_3b.txt

python diff_to_changes_dict.py temp_bop_3a.txt temp_bop_3b.txt change_bop_3a_3b.txt
117 changes written to change_bop_3a_3b.txt

python alldiff1.py ../temp_bop_3b.txt ../temp_bop_1a_ab.txt temp_alldiff1_3b.txt
2060 written to temp_alldiff1_3b.txt


--------------------------------------------------------
cp ../temp_bop_3b.txt ../temp_bop_3c.txt
Manual editing of temp_bop_3c.txt, in several steps

------------------------
Compare italic sequences
python cmp_misc.py 2 ../temp_bop_3c.txt ../temp_bop_1a_ab.txt temp_cmp_misc_3b_2.txt
1440 entries differ
12106 written to temp_cmp_misc_3b_2.txt

{%a.%} -> {%a%}.  (13)
{%b.%} -> {%b%}.  (16)
{%afz → {%aʃz
%}LB{% -> LB
{%« -> «{% 62
»%} -> %}» 29
python cmp_misc.p y 2 ../temp_bop_3c.txt ../temp_bop_1a_ab.txt temp_cmp_misc_3b_2.txt
%}». -> ».%} 44
:%} -> %}: 86
'{%f. id.%}' -> '{%f.%} {%id.%}'  20
'%},LB%{' -> ',LB'  105
'. id.%}' -> '.%} {%id.%}'  ~90
'. i. q.%}' ->  '.%} {%i. q.%}'  100+
etc. etc.

Eventually, temp_cmp_misc_3b_2.txt is empty.
Thus, ../temp_bop_3c.txt and ../temp_bop_1a_ab.txt agree
in the {%X%} markup.
Of course, there will still be differences.

generate the changes from 3b to 3c
cd ../
python diff_to_changes_dict.py temp_bop_3b.txt temp_bop_3c.txt change_bop_3b_3c.txt
2565 changes written to change_bop_3b_3c.txt

--------------------------------------------------------
## examine {#X#} sequences
cp ../temp_bop_3c.txt ../temp_bop_3d.txt
python cmp_misc.py 3 ../temp_bop_3d.txt ../temp_bop_1a_ab.txt temp_cmp_misc_3d.txt
620 entries differ
14429 written to temp_cmp_misc_3d.txt

Do the iteration thing, by editing the two files
  ../temp_bop_3d.txt and ../temp_bop_1a_ab.txt  
until devanagari instances are the same.

First change is to merge devanagari on consecutive lines

#}LB{# -> LB  1463 occurrences

$ python cmp_misc.py 3 ../temp_bop_3d.txt ../temp_bop_1a_ab.txt temp_cmp_misc_3d.txt
335 entries differ

#},LB{# -> ,LB  122
$ python cmp_misc.py 3 ../temp_bop_3d.txt ../temp_bop_1a_ab.txt temp_cmp_misc_3d.txt
232 entries differ

Question: double-avagraha
<L>965<pc>032-a<k1>AmBasa
example: {#sarvam AmBasam evA ''sIt KaYca dyOSca#}
_\({#[^#]*\)" -> \1''  114 changes


python cmp_misc.py 3 ../temp_bop_3d.txt ../temp_bop_1a_ab.txt temp_cmp_misc_3d.txt
182 entries differ

.{# -> . {#  185 instances
'{# — ' -> ' — {#'  117 instances

python cmp_misc.py 3 ../temp_bop_3d.txt ../temp_bop_1a_ab.txt temp_cmp_misc_3d.txt
114 entries differ

° degree -> ॰ Deva-abbrev   41
° (U+00B0) is the Degree Symbol
॰ is known as the Devanagari Abbreviation Sign

python cmp_misc.py 3 ../temp_bop_3d.txt ../temp_bop_1a_ab.txt temp_cmp_misc_3d.txt
0 entries differ

So now ../temp_bop_3d.txt and ../temp_bop_1a_ab.txt  agree in {#X#}

generate the changes from 3c to 3d
cd ../
python diff_to_changes_dict.py temp_bop_3c.txt temp_bop_3d.txt change_bop_3c_3d.txt
3292 changes written to change_bop_3c_3d.txt

--------------------------------------------------------
## examine <lang.*?</lang> sequences
cp ../temp_bop_3d.txt ../temp_bop_3e.txt
python cmp_misc.py 4 ../temp_bop_3e.txt ../temp_bop_1a_ab.txt temp_cmp_misc_3e.txt
91 entries differ

now edit 3e and 1a_ab to resolve differences in lang-tags

---
<lang n="russian"> -> <lang n="Russian"> 24
  Note: Formerly one.dtd (in csl-pywork) require "russian" (lower case)
  However, now one.dtd does not check the value of the n-attribute of lang tag
  So we can use whatever.
  Probably later we will change '<lang n="Russian">X</lang>' to '<rus>X</rus>' (per one.dtd)
  And we will apply lang tag to refer to the language name e.g. <lang>russ.</lang> <rus>X</rus>
---
Similar comment re "arabic" and "Arabic" . cdsl changed to Arabic.
---
Question: re Slavonic:
1. What is the modern equivalent?  There is no 'slav...' in Google Translate
2. Why did AB seem to 'lower-case' the entries?
   Because of limited font support for some upper-case?
AB: it could mostly be Bulgarian (which is from Old Church Slavonic). 
--------------------------------------------------------
python cmp_misc.py 4  ../temp_bop_1_ab.txt ../temp_bop_1a_ab.txt temp_lang_ab_1_1a.txt

Current versions of 3e and 1a_ab now agree w.r.t. lang tag.

generate the changes from 3d to 3e
cd ../
python diff_to_changes_dict.py temp_bop_3d.txt temp_bop_3e.txt change_bop_3d_3e.txt
78 changes written to change_bop_3d_3e.txt

python alldiff1.py ../temp_bop_3e.txt ../temp_bop_1a_ab.txt temp_alldiff1_3e_1a_ab.txt
889 entries differ

How to get at those 889 diffs?
--------------------------------------------------------
cp ../temp_bop_3e.txt ../temp_bop_4a.txt

# cp cmp_misc.py cmp_misc1.py and adjust as needed
python cmp_misc1.py 1  ../temp_bop_4a.txt ../temp_bop_1a_ab.txt temp_cmp_misc_4a_1.txt
882 entries differ  (why not 889?)

'-{' -> '— {' 69
'; \([0-9][0-9]\)\. \([0-9][0-9]\)\.'  ->  '; \1.\2.' 120
'^\([0-9][0-9]\)\. \([0-9][0-9]\)\.'  ->  '\1.\2.' 45
'\.LB: '  -> '.:LB'  480
'; \([0-9]+\.\) \([0-9]+\.\):'  ->  '; \1\2:' 230

9 matches for "\.»" in buffer: temp_bop_1a_ab.txt
377 matches in 359 lines for "»\." in buffer
etc. etc.

Continue until the two files agree in words.
... many hours pass ...
Now 0 entries differ !

# generate change file 3e to 4a
python diff_to_changes_dict.py temp_bop_3e.txt temp_bop_4a.txt change_bop_3e_4a.txt
2856 changes written to change_bop_3e_4a.txt

--------------------------------------------------------
sh redolocal.sh 4a
gives errors.
Reason: the xml uses <div n="lb">
make_xml.py in csl-pywork was adjusted to use "<br/>".
Now displays break on lines (still) but, with the revisions to bop.txt,
the lines are often different.

--------------------------------------------------------
temp_bop_4b.txt  Remove blank lines within entries.
cd ../
cp /c/xampp/htdocs/sanskrit-lexicon/PWK/pwkissues/issue106/pw_7_work/remove_lines.py .
python remove_lines.py temp_bop_4a.txt temp_bop_4b.txt
57230 from temp_bop_4a.txt
remove_extra_in: 948 lines dropped
remove_extra_in: 56282 lines returned
56282 lines written to temp_bop_4b.txt

# double check that 4b still agrees with 1a_ab at word-level
python cmp_misc1.py 1  ../temp_bop_4b.txt ../temp_bop_1a_ab.txt temp_cmp_misc_4b_1.txt
# 0 entries differ  as expected.
--------------------------------------------------------
I think this may be the place to stop now and discuss with Andhrabharati.

--------------------------------------------------------
Install temp_bop_4b.txt to github and cologne.
Also, install revised make_xml.py in csl-pywork

cd ../
cp temp_bop_4b.txt /c/xampp/htdocs/cologne/csl-orig/v02/bop/bop.txt

# remake local displays
cd /c/xampp/htdocs/cologne/csl-pywork/v02/
sh generate_dict.sh bop  ../../bop
sh xmlchk_xampp.sh bop
# ok  as expected

# sync csl-orig to github
cd /c/xampp/htdocs/cologne/csl-orig/
git add .
git commit -m "BOP: https://github.com/sanskrit-lexicon/BOP/issues/6"
git push

# sync csl-pywork to github
cd /c/xampp/htdocs/cologne/csl-pywork
git pull
# make_xml.py
git add .
git commit -m "BOP: https://github.com/sanskrit-lexicon/BOP/issues/6"
git push

---------------
install changes to cologne server
login to cologne ssh
cd to csl-orig
git pull
cd to csl-pywork
git pull

------------------------------------------
push this repo to github


__________________________________________________________
NOTE: changes to temp_bop_1a_ab.txt
---
<L>4352<pc>180-b<k1>DA<k2>DA
old: 'R. Schl. [Page181-a+ 37] I.11.1.:'
new: 'R. Schl. I.11.1.: [Page181-a+ 37] '
---
<L>4352<pc>180-b<k1>DA<k2>DA
old: R. Schl.  I.11.1.
new: R. Schl. I.11.1.
---
<L>6820<pc>298-a<k1>laB<k2>laB
old: R. Schl. I.10.: 10.:
new: R. Schl. I.10.10.:
---
<L>1096<pc>036-1a<k1>i
old: 'RAM. ed. Ser. [Page037-a+ 37] I.10.19.: '
new: 'RAM. ed. Ser. I.10.19.: [Page037-a+ 37] '
---
<L>8718<pc>391-a<k1>sPuw
old: 'RAM. ed. Ser. [Page391-b+ 35] II.74.61.: '
new: 'RAM. ed. Ser. II.74.61.: [Page391-b+ 35] '
---
<L>1062<pc>035-b<k1>As
old: RAM. I.29.21. ed. Ser.
new: RAM. ed. Ser. I.29.21. 
---
<L>2395<pc>083-a<k1>kF
old: GIT.-GOV. 4.14.
new: GITA-GOV. 4.14.  (print chg.) GITA-GOV. usual in BOP
---
<L>1869<pc>065-b<k1>kapi
old: Graff I.59.
new: Graff I.159.
---
<L>2938<pc>110-a<k1>gras
old: 'N. 11.2. 23.'
new: 'N. 11.22. 23.'
---
<L>6264<pc>266-a<k1>muc 
old: MAH. 1.095.
new: MAH. 1.4095.
---
<L>7693<pc>340-1b<k1>SaMs
old: MAN. 2.85.
new: MAN. 2.185.
---
<L>8666<pc>387-a<k1>sTA
old: HIT. 54.7.
new: HIT. 54.17.
---
<L>888<pc>029-a<k1>Atman<k2>Atman
old: Th. {#ahman#} spiritus.
new: Th. {%ahman%} spiritus.
---
<L>1739<pc>062-a<k1>kak<k2>kak
old: {%to be proud.%}
new: {%to be proud%}.
old: {%to be unsteady.%}
new: {%to be unsteady%}.
---
<L>2282<pc>077-b<k1>kuruvaka
old: {%A purple species of barleria.%}
new: {%A purple species of barleria%}.
---
<L>2891<pc>107-b<k1>gF
old: '{%goi-%} [Page108-a+ 37] {%rim%} '
new: '{%goirim%} [Page108-a+ 37] '
---
ć (preformed) vs. ć (combining)  Both forms exist in BOP
  SHOULD they all of 1 form (Jim prefers pre-formed)
---
<L>3615<pc>147-a<k1>tat
old: slav. <lang n="greek">ΤΟ, ΤᾹ</lang>
new:  ? why greek text after slav.?
---
<L>4024<pc>165-a<k1>das
old: {%praet. mltf.%}
new: {%praet. mtf.%}
---
<L>5018<pc>213-a<k1>parvan  Question
old: 10th of each half month.%}
new: 10th of each half month%}.
And there are some other examples. What is AB's rule ?
---
<L>5775<pc>242-b<k1>BaYj
old: {%praet. mltf.%}
new: {%praet. mtf.%}
---
<L>5805<pc>244-a<k1>Bavat
old: {%reverentiae causâ ponitur pro pronom.%}
new: {%reverentiae causâ ponitur pro pronom%}.
---
<L>6327<pc>269-b<k1>mfga
old: {%A deer, an antelope.%}
new: {%A deer, an antelope%}.
---
<L>6327<pc>269-b<k1>mfga
old: {%A deer, an antelope.%}
new: {%A deer, an antelope%},
---
<L>6732<pc>293-a<k1>ruh
old: {%in aliquo loco.%}
new: {%in aliquo loco%}.
---
<L>7138<pc>315-b<k1>vAtApi
old: {%Asuri.%}
new: {%Asuri%}.
---
<L>7770<pc>345-b<k1>SaraBa
old: the snowy mountains.%}
new: the snowy mountains%}.

old: {%A young elephant.%}
new: {%A young elephant%}.

old: {%A monkey in Rama's army.%}
new: {%A monkey in Rama's army%}.

old: {%A camel.%}
new: {%A camel%}.

old: {%A grasshopper.%}
new: {%A grasshopper%}.

old: {%A locust.%}
new: {%A locust%}.
---
<L>7839<pc>347-a<k1>SAlva
old: division of India.%}
new: division of India%}.
---
<L>7950<pc>352-b<k1>SUr
old: {%v.%}
new: {%V.%}
---
<L>8226<pc>366-a<k1>sad
old: śasseoir
new: s'asseoir   (French, 2 instances)
---
<L>2249<pc>076-b<k1>kup
old: {# kupita#}
new: {#kupita#}
---
<L>2344<pc>079-a<k1>kf
old: '{# - upakfta#}'
new: '— {#upakfta#}'
---
<L>1192<pc>043-a<k1>Irkzy
old: {# Irz#}
new: {#Irz#}
---
<L>2756<pc>100-b<k1>gam
old: tejॐSasamBavam   How did this not get transcoded? Only instance in bop
new: tejoMSasamBavam
---
<L>3287<pc>130-a<k1>Cad
old: {#CadayAmi (Urjane#} <sup>(*)</sup>)
new: {#CadayAmi#} ({#Urjane#} <sup>(*)</sup>)
---
<L>8902<pc>402-a<k1>hf
old: raSmiBiH (saMhftya = saMhftyA ''tmAnam#} i. e. vim tuam comprehendendo, colligendo)
new: raSmiBiH#} ({#saMhftya = saMhftyA ''tmAnam#} i. e. vim tuam comprehendendo, colligendo)
**************************
BEGIN changes to greek text in AB version.
35 entries with changes Why so many?
**************************
---
<L>925<pc>030-b<k1>Ap
old: <lang n="greek">πϱυμνός, πϱυνός</lang>
new: <lang n="greek">πϱυμνός, πϱέμνον</lang>
---
<L>3843<pc>157-b<k1>tF
old: <lang n="greek">τέϱ-μα, τέϱ-ϑϱον, τεϱέω, τέϱ-ε-ϱον, τοϱεύω, τιτϱάω, τιτϱαίνω, τιτϱώσϰω; τέϱασ</lang>
new: <lang n="greek">τέϱ-μα, τέϱ-ϑϱον, τεϱέω, τέϱ-ε-τϱον, τοϱεύω, τιτϱάω, τιτϱαίνω, τιτϱώσϰω; τέϱασ</lang>
---
<L>3886<pc>160-a<k1>tri
old: <lang n="greek">τϱῖες</lang>
new: <lang n="greek">τϱεῖς</lang>
---
<L>4121<pc>171-b<k1>du
old: <lang n="greek">ύω, δονέω</lang>
new: <lang n="greek">δύω, δονέω</lang>
---
<L>4523<pc>192-a<k1>naS
old: <lang n="greek">νέϰύς, νεϰϱός</lang>
new: <lang n="greek">νέϰυς, νεϰϱός</lang>
---
<L>4542<pc>193-b<k1>nABi
old: <lang n="greek">ὄνυξ, ὀϕϱς, ὀδούς, ὄνομα</lang>
new: <lang n="greek">ὄνυξ, ὀϕϱύς, ὀδούς, ὄνομα</lang>
---
<L>4874<pc>208-b<k1>pad
old: <lang n="greek">πούς</lang>
new: <lang n="greek">ΠΟΔ, πούς</lang>
---
<L>4898<pc>209-a<k1>para
old: <lang n="greek">τοῦ</lang>
new: <lang n="greek">τόν</lang>
---
<L>5042<pc>214-a<k1>pA
old: <lang n="greek">ΡΩ, πέπωϰα, πῶϑι, ἐπόϑην</lang>
new: <lang n="greek">ΠΩ, πέπωϰα, πῶϑι, ἐπόϑην</lang>
---
<L>5582<pc>233-a<k1>prI
old: <lang n="greek">ΦΙΑ</lang>
new: <lang n="greek">ΦΙΛ</lang>
AND
old: <lang n="greek">ΦΛΑ</lang>
new: <lang n="greek">ΦΛΙ</lang>
---
<L>5643<pc>236-1a<k1>baMh
old: <lang n="greek">βαϑίς</lang>
new: <lang n="greek">βαϑύς</lang>
---
<L>5756<pc>241-a<k1>brU
old: <lang n="greek">ΡΈΩ, ϱ̔ῆμα, ϱ̔ήτωέ</lang>
new: <lang n="greek">ΡΈΩ, ϱ̔ῆμα, ϱ̔ήτωϱ</lang>
---
<L>5762<pc>241-1a<k1>Bakz
old: <lang n="greek">ϕαγον; ϕάσηλος</lang> et <lang n="greek">ΦΑΓ, ἔϕαϰός</lang>
new: <lang n="greek">ΦΑΓ, ἔϕαγον; ϕάσηλος</lang> et <lang n="greek">ϕαϰός</lang>
---
<L>5873<pc>247-a<k1>Buj
old: <lang n="greek">ΦΥΤ, ϕεύγω</lang>
new: <lang n="greek">ΦΥΓ, ϕεύγω</lang>
---
<L>6045<pc>256-b<k1>man
old: <lang n="greek">μῆνος</lang>
new: <lang n="greek">μένος</lang>
---
<L>6322<pc>269-a<k1>mUza
old: <lang n="greek">μῶς, μυ-ός</lang>
new: <lang n="greek">μῦς, μυ-ός</lang>
---
<L>6382<pc>272-b<k1>meha
old: <lang n="greek">οιχός</lang>
new: <lang n="greek">μοιχός</lang>
---
<L>6400<pc>273-a<k1>mnA
old: <lang n="greek">βΕβλη-ϰα</lang>
new: <lang n="greek">βέβλη-ϰα</lang>

old: <lang n="greek">ΒΑΛ, πέπτώ-ϰα</lang>
new: <lang n="greek">ΒΑΛ, πέπτω-ϰα</lang>
---
<L>6480<pc>277-b<k1>yA
old: <lang n="greek">ἵστνμι</lang>
new: <lang n="greek">ἵστημι</lang>
---
<L>6707<pc>290-b<k1>ruc
old: <lang n="greek">λευ-ϰος, λύχ-νος</lang>
new: <lang n="greek">λευ-ϰός, λύχ-νος</lang>
---
<L>6711<pc>291-a<k1>ruj
old: <lang n="greek">λυγϱός, ο-ΡΥΤ, ὀ-ϱύσσω, ὄϱυγμα, ὀ-ϱυϰτή, ὀϱυχή</lang>
new: <lang n="greek">λυγϱός, ο-ΡΥΓ, ὀ-ϱύσσω, ὄ-ϱυγμα, ὀ-ϱυϰτή, ὀϱυχή</lang>
---
<L>6839<pc>299-b<k1>laz
old: <lang n="greek">λῶ, λῆμα, λωΐων, λωΐτεϱος, λώΐστος, λιλαίομαι</lang>
new: <lang n="greek">λῶ, λῆμα, λωΐων, λωΐτεϱος, λώϊστος, λιλαίομαι</lang>
---
<L>7027<pc>310-a<k1>varizWa
old: <lang n="greek">ἄϱισος</lang>
new: <lang n="greek">ἄϱιστος</lang>
---
<L>7081<pc>311-b<k1>vas
old: <lang n="greek">ἄσ-τν, Ϝάσ-τν, ἑσ-τία, Ἑστία</lang>
new: <lang n="greek">ἄσ-τυ, Ϝάσ-τυ, ἑσ-τία, Ἑστία</lang>
---
<L>7191<pc>317-b<k1>vi
old: <lang n="Arabic">???ك</lang>
new: <lang n="Arabic">بيباك</lang>
---
<L>7411<pc>324-b<k1>viS
old: <lang n="greek">ἵϰω/lang>
new: lang n="greek">ἵϰω</lang>   simple typo missing <
---
<L>7256<pc>319-b<k1>vid
old: <lang n="greek">ἸΔ, εἶδον, εἶδομαι; οἶδα</lang>
new: <lang n="greek">ἸΔ, εἶδον, εἴδομαι; οἶδα</lang>
---
<L>7534<pc>333-b<k1>vfD
old: <lang n="greek">βλασ-τός, βλάσ-τημ βλασ-τάνω</lang>
new: <lang n="greek">βλασ-τός, βλάσ-τη, βλασ-τάνω</lang
---
<L>8029<pc>355-b<k1>SrA
old: <lang n="greek">ϰάϱχϱς</lang>
new: <lang n="greek">ϰάϱχϱυς</lang>

old: <lang n="greek">πεϱϰάζξ</lang>
new: <lang n="greek">πεϱϰάζω</lang>
---
<L>8041<pc>357-a<k1>Sru
old: <lang n="greek">ϰλύω; ϰλ-τός</lang>
new: <lang n="greek">ϰλύω; ϰλυ-τός</lang>
---
<L>8089<pc>360-a<k1>Svi
old: <lang n="greek">ϰύω, ϰύημα, ϰῦμα, ϰυΐτϰω, ϰύτος</lang>
new: <lang n="greek">ϰύω, ϰύημα, ϰῦμα, ϰυΐσϰω, ϰύτος</lang>
---
<L>8377<pc>371-b<k1>salila
old: <lang n="greek">ἅλς</lang>
new: <lang n="greek">σάλος, ἅλς</lang>
---
<L>8574<pc>382-a<k1>sev
old: <lang n="greek">σίβομαι</lang>
new: <lang n="greek">σέβομαι</lang>
---
<L>8752<pc>393-b<k1>sru
old: <lang n="greek">σϱέϜω, ϱ̔εύ-σις, ϱ̔εῦ-μα</lang>
new: <lang n="greek">σϱέϜω, ϱ̔εύ-σω, ϱ̔εῦ-σις, ϱ̔εῦ-μα</lang>
---
<L>8856<pc>400-a<k1>hA
old: <lang n="greek">ϰιχάνε (ϰίχημι)</lang>
new: <lang n="greek">ϰιχάνω (ϰίχημι)</lang>
*******************************************
END changes to greek text in AB version.
*******************************************
---
old: .»  occurs 9 times (9 changes)
new: ».  occurs 350 times
---
<L>334<pc>011-b<k1>antar
old: {%vn-ûtrj%}<sup>(*)</sup>
new: {%vn-ûtrj%} <sup>(*)</sup>  (this is the norm in AB)
---
<L>375<pc>013-a<k1>apa
old: <lang n="greek">ἀπό</lang> lat.
new: <lang n="greek">ἀπό</lang>, lat.
---
<L>2152<pc>074-a<k1>kilviza
old: BH. 3.13. 6.45. {%b%}
new: BH. 3.13. 6.45.{%b%}
---
<pc>056-a<k1>fkza
old: <lang n="greek">ἄρϰτος</lang> hib.
new: <lang n="greek">ἄρϰτος</lang>, hib.
---
— <div
old: SA. 4.10. —
new: SA. 4.10.

old: RAM. III.79.20. —
new: RAM. III.79.20.
---
<L>3528<pc>143-b<k1>jyAyas
old: BH. 3.1. 8.3)
new: BH. 3.1. 8. 3)
---
<L>3656<pc>149-a<k1>tap
old: {#tApayan…raSmivAn iva tajasA; -tApta#} pro {#tApita#}
new: {#tApayan…raSmivAn iva tajasA#}; - {#tApta#} pro {#tApita#}
---
<L>2756<pc>100-b<k1>gam
old: gr. comp.) [Page101-a+ 37] 109^{%a%}),1. Huc
new: gr. comp. 109^{%a%}),1. [Page101-a+ 37] Huc

old: v. gr. comp. 9oc2. et abjecto
new: v. gr. comp. 92. et abjecto
---
<L>4008<pc>164-a<k1>darSana
old: R. [Page164-b+ 37] Schl. I.58.18. —
new: R. Schl. I.58.18. [Page164-b+ 37] —
---
12 instances:
old: Ǵ   
new: J
---
25 instances:
old: ǵ
new: j
---
<L>4352<pc>180-b<k1>DA
old: [Page181-a+ 37]{#rAjA 
new: [Page181-a+ 37] {#rAjA 
---
<L>4368<pc>183-a<k1>DAv
old: 16.49.; 19.0.
new: 16.49.; 19.10.
---
<L>5196<pc>219-b<k1>punar
old: DR. [Page220-a+ 37] 6.16. 3)
new: DR. 6.16. [Page220-a+ 37] 3)
---
<L>6036<pc>256-b<k1>maDu
old: <lang n="greek">λ</lang> lat. {%mel, mellis%}
new: <lang n="greek">λ</lang>; lat. {%mel, mellis%}
---
<L>6359<pc>271-b<k1>me
old: gr.<lang n="greek">ἀ-μείβω</lang>.)
new: gr. <lang n="greek">ἀ-μείβω</lang>.)
---
<L>6460<pc>276-a<k1>yam
old: 3765.3791. 5181.
new: 3765. 3791. 5181.
---
<L>6480<pc>277-b<k1>yA
old: lith {%jóju%}
new: lith. {%jóju%}
---
<L>6506<pc>279-a<k1>yAvat
old: 43.2. 5) quum,
new: 43.12. 5) quum,
---
<L>6773<pc>295-b<k1>rohiRI
old: {%in, mythologia%}
new: {%in mythologia%}
---
<L>7697<pc>341-b<k1>Sak
old: (Grimm. II.12. [Page342-a+ 37] n. 96.); gr.
new: (Grimm. II.12. n. 96.); [Page342-a+ 37] gr.
---
<L>7983<pc>353-b<k1>So
old: [Page354-a+ 36]{%hvetan%}
new: [Page354-a+ 36] {%hvetan%}
---
<L>7983<pc>353-b<k1>So
old: foruna, [Page357-a+ 37] tfelicitas.
new: fortuna, [Page357-a+ 37] felicitas.
---
<L>8451<pc>375-a<k1>sAraTi
old: curru est-e {#sa#}
new: curru est - e {#sa#}
---
<L>8632<pc>385-a<k1>stiG
old: {%stiζa%}semita,
new: {%stiζa%} semita,
---
<L>7510<pc>329-b<k1>vfka
old: <lang n="greek">υ</lang> lat. {%lupus%}
new: <lang n="greek">υ</lang>, lat. {%lupus%}
---
<L>7522<pc>330-b<k1>vft
old: (v. 3. {#vft#}). R. Schl. I.5.4
new: (v. 2. {#vft#}). R. Schl. I.5.4

___________________________________________________
-----------------------------------------------------
NOTES: ../temp_bop_1a_ab.txt
4369<L>1532<pc>053-a<k1>uSIra SAK. 43.8.  print change from 'SAK. 43..'
AB: not a print change, just a typo correction
----------------------------------------------------
05-09-2024  Actions based on AB review.
cp temp_bop_4b.txt temp_bop_4c.txt
manual edits of temp_bop_4c.txt and temp_bop_1a_ab.txt (AB version)
---
Re slavonic/russian, see AB comment at
  https://github.com/sanskrit-lexicon/BOP/issues/5#issuecomment-1517967036
---
ć (preformed) vs. ć (combining)
AB: Yes, we can go with the pre-formed letter.
47 matches in 43 lines for "ć" in buffer: temp_bop_4c.txt preformed
10 matches in 9 lines for "ć" in buffer: temp_bop_4c.txt combining
Same for AB version
Action change the combining to preformed in both files
"ć" -> "ć"   10
---
'pronom.' is an abbreviation
'pronom%}.' -> 'pronom.%}'

1 match for "pronom\.%}" in buffer: temp_bop_1.txt
0 matches for "pronom%}\." in buffer: temp_bop_4c.txt
Nothing to change,  as AB noted.
---
\.»  0 times
»\.  386 times
AM». -> AM.»  L=904
lat». -> AM.» L=1171
--------------------

Now for checking and installing ...
python cmp_misc1.py 1  ../temp_bop_4c.txt ../temp_bop_1a_ab.txt temp_cmp_misc_4c_1.txt
# 0 entries differ, as expected
---
# generate change file 4b to 4c
python diff_to_changes_dict.py temp_bop_4b.txt temp_bop_4c.txt change_bop_4b_4c.txt
11 lines changed
---

--------------------------------------------------------
Install temp_bop_4c.txt to github and cologne.
cd ../
cp temp_bop_4c.txt /c/xampp/htdocs/cologne/csl-orig/v02/bop/bop.txt

# remake local displays
cd /c/xampp/htdocs/cologne/csl-pywork/v02/
sh generate_dict.sh bop  ../../bop
sh xmlchk_xampp.sh bop
# ok  as expected

----
# sync csl-orig to github
cd /c/xampp/htdocs/cologne/csl-orig/
git add .
git commit -m "BOP: final adjustments https://github.com/sanskrit-lexicon/BOP/issues/6"
git push

---------------
install changes to cologne server
login to cologne ssh
cd to csl-orig
git pull
cd to csl-pywork/v02
sh generate_dict.sh bop  ../../BOPScan/2020/
---------------
Regenerate AB version

# 1. deva form
python bop_transcode.py slp1 deva temp_bop_1a_ab.txt temp_bop_1a_ab_deva.txt 
37844 written to temp_bop_1a_ab_deva.txt

check invertibility

python bop_transcode.py deva slp1 temp_bop_1a_ab_deva.txt temp.txt 
37844 written to temp.txt
diff temp_bop_1a_ab.txt temp.txt | wc -l
# 0 as expected
rm temp.txt

# 2. 
python cdsl_AB.py CDSL,AB temp_bop_1a_ab_deva.txt BOP_main_L2_rev.txt

diff -w ../BOP_main-L2.txt BOP_main_L2_rev.txt | wc -l
# 476  (/ 476 4) = 119 lines different (approximate)
-----

Another view of the diff
python cmp_misc1.py 1 ../temp_bop_1_ab.txt ../temp_bop_1a_ab.txt ../cmp_bop_1_ab_1a_ab.txt

37844 lines read from ../temp_bop_1_ab.txt
37844 lines read from ../temp_bop_1a_ab.txt
17921 groups 8961 entries
17921 groups 8961 entries
8838 entries the same
123 entries differ
369 written to cmp_bop_1_ab_1a_ab.txt

Note: change 'CD:' refers to temp_bop_1_ab.txt
and 'AB:' referse to temp_bop_1a_ab.txt

