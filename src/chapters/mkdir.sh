function system {
  "$@"
  if [ $? -ne 0 ]; then
    echo "make.sh: unsuccessful command $@"
    echo "abort!"
    exit 1
  fi
}

if [ $# -eq 0 ]
  then
      echo "No arguments supplied"
      echo "Usage: mkdir.sh <name-of-directory>"
      exit 1
fi

if [ -d "$1" ];
then
    echo "$1 exists, choose a non existing name"
    exit 1
fi
    

name=$1
system cp -r template $name
system cd $name
system mv -f NAME.do.txt $name.do.txt
system mv -f main_NAME.do.txt main_$name.do.txt
system mv -f exercises_NAME.do.txt exercises_$name.do.txt
system doconce replace NAME $name $name.do.txt main_$name.do.txt exercises_$name.do.txt make.sh
system echo "Customize chapter heading, authors, etc. in $name/main_$name.do.txt"
system rm -f *~
system chmod u+rwx make.sh
# Nice to have/indicate
system mkdir fig-$name src-$name
