#!/bin/bash

# assuming the code is already set to break_everything mode
yarn run test > fails.out 2>&1
rm fails.out
python get_failing_tests.py 
