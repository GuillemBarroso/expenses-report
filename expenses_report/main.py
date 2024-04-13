import os

import pandas as pd

from expenses_report.calcs import Calcs
from expenses_report.pdf_creator import PDFcreator

pdf_dir = "./"
pdf_name = "expenses_test_report.pdf"

# Load data from Excel sheet
user_name = "test_user"
expenses_dir = r"data"
expenses_file_name = "expenses.xlsx"
excel_file = pd.ExcelFile(os.path.join(expenses_dir, expenses_file_name))

# Read "Date" and "Import" columns of each sheet and create a dictionary of dataframes
expenses = {}
columns_to_read = ["Date", "Import"]
for sheet_name in excel_file.sheet_names:
    if sheet_name != "Summary":
        # Read only the specified columns from the current sheet into a DataFrame
        df = pd.read_excel(excel_file, sheet_name=sheet_name, usecols=columns_to_read)

        # Convert "Date" column to datetime format
        df["Date"] = pd.to_datetime(df["Date"])

        # Store the DataFrame in the dictionary with the sheet name as key
        expenses[sheet_name] = df

# Compute total and monthly aggregates
calcs = Calcs(expenses)
total_aggregate = calcs.total_aggregate()
monthly_aggregate = calcs.monthly_aggregate()

# Create PDF report
pdf_creator = PDFcreator(pdf_dir, pdf_name)
pdf_creator.build_pdf(total_aggregate, monthly_aggregate)
