#!/bin/bash

# if the output files already exist, move them to avoid accidentally appending the new 
# data and therefore polluting it
if test -f "$3"; then
	mv $3 `echo $3"_old"`
fi
if test -f "$4"; then
	mv $4 `echo $4"_old"`
fi

warmups=0
if (( "$#" > 4 )); then
	warmups=$5
fi

for (( x=0; x<$warmups; x++ )); do
	echo "Warmup run: "$x" of "$warmups
	# run some tests into the void 
	npm run test -- --o
done

for x in $(eval echo {1..$1}); do
	echo "Running test suite: " $x
	npm run test $(cat $2) >> $3 
	python process_junit_xml_out.py $4
	echo "Done running test suite, cleaning up now..."
	rm -rf /tmp/*
done
