import glob, sys, os, shutil, logging

sphinx_rootdir = 'sphinx-uio'
if not os.path.isdir(sphinx_rootdir):
    print( """*** error: %(sphinx_rootdir)s does not exist. This means unsuccessful
    doconce sphinx_dir command. Try to upgrade to latest DocOnce version.
    (The script tmp_sphinx_gen.sh runs sphinx-quickstart - it may have failed.)
""" % vars())
    
