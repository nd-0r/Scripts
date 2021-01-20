#!/bin/bash
read -p "Enter working directory: " workDir
echo "moving to $workDir"
cd "$workDir"
read -p "Should all files in working directory be split to mono: Y or N" response
if [ "$response" == "Y" ]; then
	echo "Converting"
	GLOBIGNORE=".:.."
	# shopt -s dotglob 
	for i in *; do
		chans=$(soxi -c "$i")
		while [ $chans -ge 1 ]; do
			currentChan=$(printf %02i $chans)
			out=`echo "$i"|sed "s/\(.*\)\.\(.*\)/\1-$currentChan.\2/"`
			sox -S "$i" "$out" remix $chans
			chans=$(expr $chans - 1)
		done
	done
else
	exit 0
fi 
exit 0
