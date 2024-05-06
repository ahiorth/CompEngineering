# How to compile the chapters 
```
Terminal>cd CompEngineering/src/chapters/lin
Terminal>./make.sh
```
NB: If you do not have `ispell` installed do
```
Terminal>cd CompEngineering/src/chapters/lin
Terminal>./make.sh nospell
```

Basically the make script in the `lin` folder calls the `make.sh`, `make_html.sh`, and `clean.sh` files in the `chapter` folder.  
# How to compile the book
To compile the book, a few more steps are needed. In the `book` folder, we need to make shortcuts or soft links to all the chapter directories. This is done by running a python script - from the terminal in the `book` folder do:
```
Terminal>python -c "import scripts as s; s.make_links()"
```
If all links where made succesful do
```
Terminal>./make.sh
Terminal>./make_html.sh
```

