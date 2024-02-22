# Export Comments to Excel

This Python script automates the process of exporting comments from various platforms using the ExportComments API and saves them into an Excel file. It handles rate limiting, retries upon failure, and organizes the data by appending it to a specified column in the Excel sheet.

## Features

- Fetch URLs from an Excel file.
- Generate exports for each URL using the ExportComments API.
- Handle API rate limiting with automatic retries.
- Check the status of each export and download the result upon completion.
- Append downloaded data to an Excel file, replacing a specified column with the original URL.

## Requirements

- Python 3.x
- openpyxl
- pandas
- requests
- exportcomments


## Installation

First, ensure you have Python 3 installed on your system. You can then install the required Python packages using pip:

```bash
pip install openpyxl pandas requests exportcomments
```

## Usage

1. **Prepare Your Environment**: Ensure all dependencies listed in the "Requirements" section are installed.
2. **Set Up Your ExportComments API Key**: Make sure the API key is still valid/correct
3. **Prepare the Input Excel File**: The script expects an Excel file named `url_list.xlsx` in the same directory, with URLs to process in the first column.
4. **Run the Script**: Execute the script with Python

5. **Review the Output**: Upon completion, the script saves the results to `final_results.xlsx` in the same directory. Each row's H column will be replaced with the URL from which the comments were exported.

## Handling Errors

The script includes basic error handling for rate limiting and API errors. If an export fails or an unexpected error occurs, the script will print an error message and skip the problematic URL. (There are still possible errors like losing internet that can crash the script.)

## Customization

You can customize the script to change the input and output file names, modify the column to be replaced with the URL, or adjust the handling of API responses based on your needs.

## License

Specify your project's license here, if applicable.