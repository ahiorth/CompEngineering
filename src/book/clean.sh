#!/bin/sh
python -c 'import scripts; scripts.clean()'
rm -rf runestone sphinx-* *.pyc automake*
