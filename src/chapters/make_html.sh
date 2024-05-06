#!/bin/bash -x
# Compile a chapter as a stand-alone HTML document.
# See make.sh for variables.
#
# Run from subdirectory as
#
# bash -x ../make_html.sh main_chaptername --encoding=utf-8
set -x

mainname=$1
shift
args="$@"

CHAPTER=document
BOOK=document
APPENDIX=document

# mainname: main_chaptername
# nickname: chaptername
nickname=`echo $mainname | sed 's/main_//g'`

function system {
  "$@"
  if [ $? -ne 0 ]; then
    echo "make.sh: unsuccessful command $@"
    echo "abort!"
    exit 1
  fi
}

rm -fr tmp_*

# Spell checking: done in make.sh

preprocess -DFORMAT=html ../newcommands.p.tex > newcommands_keep.tex

opt="CHAPTER=$CHAPTER BOOK=$BOOK APPENDIX=$APPENDIX"

#style=solarized3
#html=${nickname}-solarized
#system doconce format html $mainname $opt --html_style=$style --html_output=$html $args
#system doconce split_html $html.html --nav_button=text

#style=bootstrap_bluegray
#html=${nickname}-bootstrap
#system doconce format html $mainname $opt --html_style=$style --html_output=$html $args
#system doconce split_html $html.html --nav_button=text

style=bootswatch_readable
html=${nickname}-readable
system doconce format html $mainname $opt --html_style=$style --html_output=$html --html_code_style=inherit $args
system doconce replace 'width=400' 'width=800' $html.html

system doconce split_html $html.html --nav_button=text

# Sphinx themes
#themes="basicstrap bloodish pyramid read_the_docs scipy_lectures uio"
#theme="pyramid"
#theme="uio"

#system doconce format sphinx ${mainname} $opt --sphinx_keep_splits $args
#system doconce split_rst ${mainname}
#system doconce sphinx_dir theme=$theme dirname=sphinx-${theme} ${mainname}
# Change logo?
#doconce replace _static/uio_logo.png https://raw.githubusercontent.com/CINPLA/logo/master/brain/cinpla_uio_logo.png sphinx-${theme}/_themes/uio/layout.html
#doconce replace _static/uio_logo.png https://raw.githubusercontent.com/CINPLA/logo/master/brain/cinpla_logo_transparent.png sphinx-${theme}/_themes/uio/layout.html

#system python automake_sphinx.py

# Publish
dest=/some/repo/some/where
dest=../../../chapters
if [ ! -d $dest ]; then
exit 0  # drop publishig
fi
dest=$dest/$nickname
if [ ! -d $dest ]; then
  mkdir $dest
  mkdir $dest/pdf
  mkdir $dest/html
fi
cp -r ${nickname}-*.html ._${nickname}-*.html $dest/html

#rm -rf $dest/html/sphinx
#cp -r sphinx-${theme}/_build/html $dest/html/sphinx

# index.html for this chapter
#cp ../index_html_files.do.txt index.do.txt
#system doconce format html index --html_style=bootstrap_FlatUI CHAPTER="${nickname}" --html_bootstrap_navbar=off #--html_links_in_new_window
#cp index.html $dest/html/
#rm -f index.*

# We need fig, mov in html publishing dir
rsync="rsync -rtDvz -u -e ssh -b --delete --force "
dirs="fig-$nickname mov-$nickname"
for dir in $dirs; do
  if [ -d $dir ]; then
    $rsync $dir $dest/html
  fi
done

#cd $dest
#git add html
