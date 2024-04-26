#!/bin/bash
# Pack a latex book project for Springer:
# Make subdirectory $author_name with all relevant latex files,
# including all style files.
set -x

author_name=langtangen
# Name of main text file in this directory
name=book
# Name of main tex file for the book as Springer will see
# it in subdir $author_name
book=book

# Put all files in directory $author_name
rm -rf $author_name
mkdir $author_name
cd $author_name
# Copy the single tex file for the entire book
cp ../${name}.tex $book.tex

# Copy all figures to one directory
mkdir figs
for dir in ../fig-*; do  # Assume all figures in ../fig-* directories
  cp $dir/* figs
done
doconce subst '\{fig-.+?/' '{figs/' $book.tex

# Copy ready-made discription of how this directory is organized
cp ../README_Springer_dir.txt 00README.txt

# Copy .bib file and newcommands
cp ../papers.bib .
#doconce replace '{../chapters/papers}' '{papers}' $book.tex
cp ../newcommands_keep.tex .

# Test that the book can be compiled in this subdir
rm -rf tmp.txt
pdflatex book | tee tmp.txt   # output of command in tmp.txt
rm -rf *.dvi *.aux *.out *.log *.loe *.toc *.idx

# Copy the log file from last run in the parent directory
# and analyze potential problems (too long lines, etc.) with the script
# doconce latex_problems
cp ../${name}.log book_last_run.log
doconce latex_problems book_last_run.log > book_last_run.log.summary

# Copy all style files needed for the book to a subdir stylefiles.
# Make use of 1) doconce's output of all needed style files (found
# in tmp.txt from running pdflatex above, but run doonce grab to
# get just the list of files), 2) the script ../grab_stylefiles.py
# to find each style file (the script creates a new script tmpcp.sh
# for copying the style files from their various locations).
doconce grab --from- '\*File List\*' --to- '\*\*\*\*' tmp.txt > tmp2.txt
python ../grab_stylefiles.py tmp2.txt book.tex  # make script tmpcp.sh
if [ ! -d stylefiles ]; then
    mkdir stylefiles
fi
sh ./tmpcp.sh  # copy all style files
rm tmpcp.sh
rm *~ tmp*

# Use most recently compiled PDF in the parent dir as official PDF
cd ..
cp ${name}.pdf $author_name/${name}.pdf

# Make tarfile of the directory tree
tarfile=tutorial.tar.gz
tar czf $tarfile $author_name
#cp ${author_name}/${book}_*.tex $tarfile "~/Dropbox/Springer/Scaling"
exit
