@Echo off
REM for compiling doconce files
SET "name=book"
echo %name%
SET "outa=%name%%extn%"
SET "outb=%name%_simple%extn%"
SET "CHAPTER=chapter"
SET "BOOK=book"
SET "APPENDIX=appendix"

SET "opt=CHAPTER=%CHAPTER% BOOK=%BOOK% APPENDIX=%APPENDIX%"
SET "opt=%opt% --exercise_numbering=chapter"
echo %opt%
REM --- begin simple pdflatex ----
doconce format pdflatex %name%  --device=paper --exercise_numbering=chapter   --latex_style=Springer_T4 --latex_title_layout=titlepage --latex_list_of_exercises=loe --latex_admon=graybox2 --latex_table_format=left --latex_admon_title_no_period --latex_no_program_footnotelink "--latex_code_style=default:lst[style=blue1]@pypro:lst[style=blue1bar]@dat:lst[style=gray]@sys:vrb[frame=lines,label=\\fbox{{\tiny Terminal}},framesep=2.5mm,framerule=0.7pt]" "--latex_admon_color=warning:darkgreen!40!white;notice:darkgray!20!white;summary:tucorange!20!white;question:red!50!white;block:darkgreen!40!white"


REM # Auto edits
doconce replace "{rgb}{0.87843, 0.95686, 1.0}" "{rgb}{0.988235,0.964706,0.862745}" %name%.tex
doconce replace "{rgb}{0.7,     0.95686, 1}" "{rgb}{0.988235,0.964706,0.862745}" %name%.tex
if %errorlevel%==1 goto :eof
REM doconce replace 'linecolor=black,' 'linecolor=darkblue,' %name%.tex
REM doconce subst 'frametitlebackgroundcolor=.*?,' 'frametitlebackgroundcolor=blue!5,' %name%.tex
REM helps position the figures

rm -rf %name%.aux %name%.ind %name%.idx %name%.bbl %name%.toc %name%.loe

pdflatex %name%
if %errorlevel%==1 goto :eof
bibtex %name%
makeindex $name
pdflatex %name%
makeindex $name
pdflatex %name%
pdflatex %name%
REM mv %outa% %outb%
cp %name%.pdf ../../pub/
rm -rf %name%.aux %name%.ind %name%.idx %name%.bbl %name%.toc %name%.loe %name%.log %name%.tex.old %name%.tex.old~~

