#!/bin/bash

# Create a "reports" folder if it doesn't exist
mkdir -p reports

# Find all test files in the "tests" folder
test_files=$(find tests -name "test_*.py" | sort)

# Loop through each test file and run pytest with customized options
for test_file in $test_files; do
    # Extract the test file name without extension
    test_name=$(basename "$test_file" .py)

    # Set log and test data filenames based on the test file name
    log_filename="${test_name}_log.log"
    test_data_filename="${test_name}_data.json"

    # Set the HTML report filename
    html_report_filename="reports/${test_name}_report.html"

    # Run pytest with the specified options (including HTML report)
    pytest "$test_file" \
        --log-filename="$log_filename" \
        --test-data-filename="$test_data_filename" \
        --html="$html_report_filename"
done