-----------------------------------------------------------------------
This directory contains the files for making a PDF from latex source
-----------------------------------------------------------------------

The LaTeX code is automatically generated from another source, and all
LaTeX code for the book appears in a single file

   book.tex

Figures are in subdirectory figs.

References are in BibTeX format in papers.bib.

To compile the book, run

  pdflatex book
  bibtex book
  makeindex book
  pdflatex book
  pdflatex book

All the needed LaTeX style files are in the subdirectory stylefiles.

book_last_run.log contains the LaTeX log output from the last
run of pdflatex book.tex for examination of errors.

book_last_run.log.summary provides a summary of the log file for
quick reading of key problems. Only lines longer than 30pt are
reported in the summary (meaning that shorter lines, still leading
to an overfull hbox, are accepted - this is in accordance with
previous editions of the book).

newcommands_keep.tex: newcommands, included in book.tex
book.pdf: compiled book.tex

stylefiles: directory with all the stylefiles used in book.tex
(note that svmono.cls is modified to svmonodo.cls).
