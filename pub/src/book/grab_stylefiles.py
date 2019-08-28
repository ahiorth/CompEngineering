# Read output from pdflatex/latex, after doconce grab
# doconce grab --from- '\*File List\*' --to- '\*\*\*\*' tmp.txt > tmp.txt
# and find all styles files with full path

dont_copy = []

import sys, commands, os
f = open(sys.argv[1], 'r')
lines = f.readlines()
paths = []
for line in lines:
    words = line.split()
    filename = words[0]
    if filename.endswith('.def') or \
       filename.endswith('.tex') or \
       filename.endswith('.aux') or \
       filename.endswith('.sty') or \
       filename.endswith('.cls') or \
       filename.endswith('.clo') or \
       filename.endswith('.cfg') or \
       filename.endswith('.dfu'):

        if sum(filename.startswith(name) for name in dont_copy) > 0:
            continue
        failure, output = commands.getstatusoutput('kpsewhich %s' % filename)
        if not failure:
            paths.append(output)

# Write copy script
extdoc = []
f = open('tmpcp.sh', 'w')
dest = 'stylefiles'
for path in paths:
    if path.endswith('.aux'):
        # .aux file needed for \externaldocument{}, these often have
        # names /user/.../book.aux so use full path
        local_dir = os.path.join(dest, os.path.dirname(path)[1:])
        extdoc.append((os.path.dirname(path), local_dir))
        if not os.path.isdir(local_dir):
            os.makedirs(local_dir)
        f.write('cp %s %s\n' % (path, local_dir))
    elif path.startswith('./'):
        f.write('cp %s .\n' % path)
    else:
        f.write('cp %s %s\n' % (path, dest))
f.close()
if extdoc:
    # Fix .tex file
    try:
        filename = sys.argv[2]
    except IndexError:
        filename = 'book.tex'
    f = open(filename, 'r')
    text = f.read()
    f.close()
    for dirname, newname in extdoc:
        text = text.replace(dirname, newname)
    f = open(filename, 'w')
    f.write(text)
    f.close()
