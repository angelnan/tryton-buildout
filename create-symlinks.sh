#!/bin/bash

# dst=$1
# src=$2

dst=../trytond/trytond/modules
src=../../../modules

if [[ -z "$dst" || -z "$src" ]]; then
    echo "Use create-symlinks.sh <destination_directory> <source_path>"
    echo 
    echo "directory should point to the addons directory of the server"
    exit 1
fi

# Remove all symlinks in $dst directory. This way we ensure we 
# do not remove modules created there by mistake.

modules=$(find $dst -type l)
if [ "$modules" != "" ]; then
    rm -f $modules
fi

remaining=$(ls $dst | wc -l)
if [ $remaining -gt 1 ]; then
	echo "There are still files in $dst directory after removing all symlinks."
	echo "Please ensure there are no files or directories there."
	echo "Files and directories found:"
	ls $dst
	exit 1
fi

pushd $dst 

echo $(pwd)
# We add sort because we want 'custom-modules' to be processed first. This way it's
# possible to override modules in addons with new modules with the same name.
list=$(find $src -iname "tryton.cfg" | sort | awk '{system("dirname "$dst)}')

echo "list: $list"

for i in $list; do 
    if [ -d "$i" ]; then
        ln -s "$i" "."
    else
        echo "'$i' doesn't exist"
    fi
done

popd
