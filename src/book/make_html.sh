#!/bin/bash -x
# Compile the book to LaTeX/PDF.
#
# Usage: make.sh [nospell]
#
# With nospell, spellchecking is skipped.
set -x

name=book
CHAPTER=chapter
BOOK=book
APPENDIX=appendix

function system {
  "$@"
  if [ $? -ne 0 ]; then
    echo "make.sh: unsuccessful command $@"
    echo "abort!"
    exit 1
  fi
}

preprocess -DFORMAT=html ../chapters/newcommands.p.tex > newcommands_keep.tex

opt="CHAPTER=$CHAPTER BOOK=$BOOK APPENDIX=$APPENDIX"
opt="$opt --exercise_numbering=chapter"

# Compile HTML Bootstrap book
html_style=bootswatch_journal
#html_style=bootswatch_readable
system doconce format html $name $opt --html_style=$html_style  --html_code_style=inherit --html_output=$name
#system doconce format html $name $opt --html_style=solarized_dark --html_code_style=inherit --html_output=$name
#system doconce replace '\\\]' '\\]' $name.html
system doconce replace 'width="400"' 'width="800"' $name.html
#system doconce split_html $name.html


# Publish
dest=../../html
if [ ! -d $dest ]; then
    #exit 0  # drop publishing
  mkdir $dest
fi

cp -v $name.html ._${name}*.html $dest
figdirs="fig-* mov-*"
for figdir in $figdirs; do
    if [ ! -d $dest ]; then
	#exit 0  # drop publishing
	mkdir $dest
    fi
    # slash important for copying files in links to dirs
    if [ -d $figdir/ ]; then
        cp -r $figdir/ $dest/$figdir/
    fi
done

system ./clean.sh
