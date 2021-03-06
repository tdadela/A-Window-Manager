#!/bin/bash

arg='.'
if [[ $# -eq 1 ]]; then
	arg=$@
fi

echo Repositiory: $(basename `git rev-parse --show-toplevel`)
echo
git diff | cat
echo
git status
echo
autopep8 -i *.py awm/*.py
pepdiff=$(autopep8 -daa *.py awm/*.py)

if [ -n "$pepdiff" ]; then
	echo $pepdiff
	read -p 'Accept above pep8 changes? ' -n 1 -r
	echo
	if [[ ! $REPLY =~ ^[Nn]$ ]]; then
		autopep8 -iaa *.py awm/*
		echo Applied
	fi
fi
echo git add $arg
git add $arg
git status
echo Enter commit name.
read -p 'Please, use conventional commits: '
git commit -m "$REPLY"
git push
