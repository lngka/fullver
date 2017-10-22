#!/bin/bash

# TEST="4.20OKOKOKOKOK"
# if [[ `echo $TEST | grep "OKOKOKOKOK"` != "" ]]; then
#     echo "Found OKOKOKOKOK"
#     echo "TEST is $TEST"
# else
#     echo "NOT FOUND OKOKOKOKOK"
#     echo "TEST is $TEST"
# fi

TEST=$( cat 1.txt )

for item in $TEST; do
    echo $item
done
