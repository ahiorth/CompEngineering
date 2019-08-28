#!/bin/sh
name=rules
bash -x make.sh
bash -x ../make_html.sh main_$name
bash -x ../make_slides.sh slides_$name
