#!/bin/bash

# dst=$1
# src=$2

dst=../userdoc
src=../modules


if [[ -z "$dst" || -z "$src" ]]; then
	echo "Use create-symlinks.sh <destination_directory> <source_path>"
	echo
	echo "directory should point to the addons directory of the server"
	exit 1
fi

if [ -d "$dst" ]; then
    pushd $dst
    srclog=$(cd $src 2>&1)
    if [ -n "$srclog" ]; then
        echo "the '$src' as destination directory must exist."
        echo
        echo " Err: '$srclog'"
        echo
        exit 1
    fi
    popd
else
	echo "the '$dst' as destination directory must exist."
	echo
	exit 1
fi

# Remove all symlinks in $dst directory. This way we ensure we 
# do not remove modules created there by mistake.

modules=$(find $dst -type l)

if [ "$modules" != "" ]; then
    echo "REMOVING symlinks $modules"
	rm $modules
fi

#remaining=$(ls $dst | wc -l)
#if [ $remaining != '0' ]; then
#	echo "There are still files in $dst directory after removing all symlinks."
#	echo "Please ensure there are no files or directories there."
#	echo "Files and directories found:"
#	ls $dst
#	exit 1
#fi

pushd $dst 

# We exclude paths with hidden directories
list=$(find $src -type d -iname "doc" | grep -v "/\.")

for i in $list; do
    if ! test -f "$i/../tryton.cfg"; then
        continue
    fi
    f=$(find $i -iname "*.rst")
    if [ -n "$f" ]; then
        if [ -d "$i" ]; then
            module=$(basename `dirname $i`)
            echo "create symlink of $i in $module"
            ln -s "$i" "$module"
        else
            echo "'$i' doesn't exist"
        fi
    else
        echo "NOT ADDING $i"
    fi
done

echo "create symlink for the master_root file"
ln -s $src/trytond-doc/trytond_doc/doc/index.rst index.rst

popd
