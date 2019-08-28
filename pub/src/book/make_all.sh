# Use a common ../make.sh file or do customized build here.
bash -x clean.sh
bash -x make.sh
bash -x make_html.sh

dest=../../pub
gitrepo=/Users/ah/github/CompEngineering/

rm -rf gitrepo=/Users/ah/github/CompEngineering/pub
cp -rf $dest $gitrepo
