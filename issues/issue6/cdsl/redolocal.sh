version=$1
cp temp_bop_${version}.txt /c/xampp/htdocs/cologne/csl-orig/v02/bop/bop.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
home="/c/xampp/htdocs/sanskrit-lexicon/bop/issues/issue6/cdsl"
# sh generate_dict.sh bop  ../../bop
appdir=${home}/apps/${version}
sh generate_dict.sh bop  $appdir
#sh xmlchk_xampp.sh
validate="/c/xampp/htdocs/cologne/xmlvalidate.py"
python3 $validate $appdir/pywork/bop.xml $appdir/pywork/bop.dtd
cd /c/xampp/htdocs/cologne/csl-orig/v02/bop/
git restore bop.txt
cd ${home}


