"""Module containing the settings of the expenses report.

The user can modify them as required to adapt to its particular case.

"""

# --------------------------------------------
# Parameters related to the expenses XLSX file
# --------------------------------------------
# Directory of the expenses XLSX
EXPENSES_DIR = r"data"
# Expenses XLSX name
EXPNESES_FILE_NAME = "expenses.xlsx"
# Name of the expenses categories
# This should exactly match to the names of the XLSX sheets
CATEGORIES = ["Category1", "Category2"]
# Name of the XLSX columns to read at each sheet
COLUMNS_TO_READ = ["Date", "Import"]

# ------------------------------------------
# Parameters related to the output PDF report
# ------------------------------------------
# Directory of the output PDF report
PDF_DIR = "./"
# Name of the PDF report
PDF_NAME = "expenses_test_report.pdf"
