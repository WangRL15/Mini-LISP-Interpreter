#!/bin/bash

# check if hidden_test_data exits
if [ ! -d "hidden_test_data" ]; then
  echo "hidden_test_data does not exit！"
  exit 1
fi

# check if interpret.py exits
if [ ! -f "interpret.py" ]; then
  echo "interpret.py does not exit！"
  exit 1
fi

# clear / create hidden_test_data_output.txt
> hidden_test_data_output.txt

# test all file in hidden_test_data 
for file in hidden_test_data/*; do
  if [ -f "$file" ]; then
    echo "Processing test file:: $file"
    echo -e "Test file: $file" >> hidden_test_data_output.txt
    # execute interpret.py and output to hidden_test_data_output.txt
    python3 interpret.py < "$file" >> hidden_test_data_output.txt
    echo -e "\n" >> hidden_test_data_output.txt 
  fi
done

echo "Finish. Result saved to hidden_test_data_output.txt"
