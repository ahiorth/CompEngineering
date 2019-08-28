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

REM --- HTML ----
REM Compile HTML Bootstrap book
doconce format html %name%  --html_style=bootswatch_journal --html_code_style=inherit --html_output=%name%.html
doconce split_html %name%.html