import os
import subprocess

# Create a "reports" folder if it doesn't exist
os.makedirs("reports", exist_ok=True)

# Find all test files in the "tests" folder
test_files = sorted([f for f in os.listdir("tests") if f.startswith("test_") and f.endswith(".py")])

# Loop through each test file and run pytest with customized options
for test_file in test_files:
    # Extract the test file name without extension
    test_name = os.path.splitext(test_file)[0]

    # Set log and test data filenames based on the test file name
    log_filename = f"logs/{test_name}_log.log"
    test_data_filename = f"test_data/{test_name}_data.json"

    # Set the HTML report filename
    html_report_filename = f"reports/{test_name}_report.html"

    subprocess.run([
        "pytest",
        f"tests/{test_file}",
        "--log-file", log_filename,
        "--test-data-file", test_data_filename,
        "--html", html_report_filename
    ])

