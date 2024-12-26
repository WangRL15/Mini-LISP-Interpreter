#!/bin/bash

# check if public_test_data exits
if [ ! -d "public_test_data" ]; then
  echo "public_test_data does not exit！"
  exit 1
fi

# check if interpret.py exits
if [ ! -f "interpret.py" ]; then
  echo "interpret.py does not exit！"
  exit 1
fi

# clear / create public_test_data_output.txt
> public_test_data_output.txt

# test all file in public_test_data 
for file in public_test_data/*; do
  if [ -f "$file" ]; then
    echo "Processing test file:: $file"
    echo -e "Test file:: $file" >> public_test_data_output.txt 
    # execute interpret.py and output to public_test_data_output.txt
    python3 interpret.py < "$file" >> public_test_data_output.txt
    echo -e "\n" >> public_test_data_output.txt 
  fi
done

echo "Finish. Result saved to public_test_data_output.txt"
