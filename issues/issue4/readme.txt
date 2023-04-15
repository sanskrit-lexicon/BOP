work on issue4 for BOP dictionary.  
objective: Proofread Greek text.

# *************************************************************************
# startup instructions (for Anna)
# *************************************************************************
# 1. local copy of BOP repository
# If necessary, make a 'sanskrit-lexicon' directory (such as in ~/Documents/)
# mkdir ~/Documents/sanskrit-lexicon
cd ~/Documents/sanskrit-lexicon
# clone the BOP directory from Github.
git clone https://github.com/sanskrit-lexicon/BOP.git
# this will create 'BOP' folder: ~/Documents/sanskrit-lexicon/BOP
---------
# 2. sync local copy of csl-orig repository
cd ~/Documents/cologne/csl-orig
git pull
--------
# 3. temp_bop_0.txt
cd ~/Documents/sanskrit-lexicon/bop/issues/issue4
cp ~/Documents/cologne/csl-orig/v02/BOP/bop.txt temp_bop_0.txt
# 4. temp_bop_1.txt
# make a second copy in issue4
cp temp_bop_0.txt temp_bop_1.txt

# *************************************************************** **********
# Make corrections to temp_bop_1.txt
# *************************************************************************
This is the main task.
edit temp_bop_1.txt.
Greek text is identified by '<lang n="greek">X</lang>'.
There are 1499  instances in 1197 lines of temp_bop_1.txt.

For each such instance:
 a. compare temp_bop_1.txt to the scanned image of Bopp dictionary.
 b. If necessary, make change to temp_bop_1.txt
    NOTE: Do not introduce new (extra) lines in temp_bop_1.txt,
          as this will cause problems in next step

# *************************************************************************
# make change_1.txt
# *************************************************************************
# The program diff_to_changes_dict.py compares each line of
# temp_bop_0.txt to the corresponding line of temp_bop_1.txt.
# If these lines are different (i.e., a change was made in temp_bop_1.txt),
# then the program writes a change transaction.
python diff_to_changes_dict.py temp_bop_0.txt temp_bop_1.txt change_1.txt

Notes:
1. You can remake change_1.txt at any time.
1a. diff_to_changes_dict.py assumes temp_bop_0.txt and temp_bop_1.txt
   have the same number of lines. That's why the 'no extra lines'
   comment above is important.
2. You can push this BOP repository at any time
3. Jim will use his own copy of temp_bop_0.txt and your pushed
   change_1.txt to recreate his copy of your temp_bop_1.txt.
   [See *install instructions* below for details.
4. The BOP/.gitignore file has 'temp*' line, which means
   git will not track files whose names start with 'temp'.
   Thus Anna's local temp_bop_1.txt is not directly available to Jim.
   But Jim can recreate a copy of Anna's temp_bop_1.txt from change_1.txt.


# *************************************************************************
# Installation (Jim)
# *************************************************************************
# Jim makes a local copy temp_bop_0.txt just as Anna did.
# Use updateByLine.py program to create temp_bop_1.txt
python updateByLine.py temp_bop_0.txt change_1.txt temp_bop_1.txt
15 change transactions from change_1.txt  02-22-2023

# install into csl-orig
# a. copy to csl-orig
cp temp_bop_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/bop/bop.txt

# b. Recreate local displays
cd /c/xampp/htdocs/cologne/csl-pywork/v02
grep 'bop ' redo_xampp_all.sh
sh generate_dict.sh bop  ../../bop

# c. check xml validity of bop.xml
sh xmlchk_xampp.sh bop
# ok.  [If there are errors, they must be corrected]

## d. update csl-orig
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .  # v02/bop/bop.txt
git commit -m "bop. Misc Greek corrections.
 Ref: https://github.com/sanskrit-lexicon/BOP/issues/4"
git push
----------------------------------------------------
update at Cologne
cd ... csl-orig
git pull
cd ../csl-pywork/v02
grep 'bop ' redo_cologne_all.sh
sh generate_dict.sh bop  ../../BOPScan/2020/
cd /c/xampp/htdocs/sanskrit-lexicon/BOP/bopissues/issue4
----------------------------------------------------
# *************************************************************************
# Progress
# *************************************************************************
Anna has provided change_1.txt and change_2.txt.
Apply these to by local temp_bop_0.txt

python updateByLine.py temp_bop_0.txt change_1.txt temp_bop_1.txt
55 change transactions from change_1.txt

python updateByLine.py temp_bop_1.txt change_2.txt temp_bop_2.txt
5 change transactions from change_2.txt

# copy to csl-orig, and remake local version
cp temp_bop_2.txt /c/xampp/htdocs/cologne/csl-orig/v02/bop/bop.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh bop  ../../bop

sh xmlchk_xampp.sh bop
python3 ../../xmlvalidate.py ../../bop/pywork/bop.xml ../../bop/pywork/bop.dtd
ok

# looks ok.
# push csl-orig to Github
cd /c/xampp/htdocs/cologne/csl-orig/
git add v02/bop/bop.txt
git commit -m "BOP Greek proofreading.
> Ref: https://github.com/sanskrit-lexicon/BOP/issues/4"

git push

# install at cologne
----------------------
# update this repository
cd /c/xampp/htdocs/sanskrit-lexicon/BOP/issues/issue4
_____________________________________________________________
THE END.
