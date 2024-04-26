@Echo off
REM for compiling doconce files
SET "name=%1"
SET "extn=main_"
echo %name%
SET "outa=%extn%%name%"
SET "outb=%name%_simple%extn%"

echo %outa%

REM --- begin simple pdflatex ----
REM doconce format pdflatex %name% --latex_code_style=vrb --latex_title_layout=std --tables2csv  
REM doconce format pdflatex %name% $opt --device=screen --latex_admon_color=1,1,1 --latex_admon=mdfbox $args --latex_list_of_exercises=toc --latex_table_format=left "--latex_code_style=default:lst[style=blue1]@pypro:lst[style=blue1bar]@dat:lst[style=gray]@sys:vrb[frame=lines,label=\\fbox{{\tiny Terminal}},framesep=2.5mm,framerule=0.7pt]"
doconce format pdflatex %name% $opt --device=screen --latex_admon=graybox2 $args --latex_list_of_exercises=toc --latex_table_format=left --latex_admon=graybox2 --latex_table_format=left --latex_admon_title_no_period --latex_no_program_footnotelink "--latex_code_style=default:lst[style=blue1]@pypro:lst[style=blue1bar]@dat:lst[style=gray]@sys:vrb[frame=lines,label=\\fbox{{\tiny Terminal}},framesep=2.5mm,framerule=0.7pt]" "--latex_admon_color=warning:darkgreen!40!white;notice:darkgray!20!white;summary:tucorange!20!white;question:red!50!white;block:darkgreen!40!white"
if %errorlevel%==1 goto :eof
REM # Auto edits
doconce replace "{rgb}{0.87843, 0.95686, 1.0}" "{rgb}{0.988235,0.964706,0.862745}" %name%.tex
doconce replace "{rgb}{0.7,     0.95686, 1}" "{rgb}{0.988235,0.964706,0.862745}" %name%.tex
if %errorlevel%==1 goto :eof
REM doconce replace 'linecolor=black,' 'linecolor=darkblue,' %outa%.tex
REM doconce subst 'frametitlebackgroundcolor=.*?,' 'frametitlebackgroundcolor=blue!5,' %outa%.tex
REM helps position the figures

rm -f *.aux
pdflatex %name%
if %errorlevel%==1 goto :eof
bibtex %name%
pdflatex %name%
REM cp %name%.pdf ../../../pub/chapters/%name%/pdf/



REM --- jupyter notebook ---
REM doconce format ipynb %name%
REM mv %name%.ipynb ipynb*.tar.gz ../../../pub/chapters/%name%/notebook/
REM --- end jupyter notebook ---
cp *.do.txt ../BACKUP/
rm -rf *.idx *.bbl *.aux *.log *.out tmp* *.dlog
