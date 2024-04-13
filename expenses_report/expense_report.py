import calendar
import os

import pandas as pd

from expenses_report.pdf_creator import PDFcreator


# Function to convert month numbers to month names
def convert_month_numbers_to_names(month_number):
    return calendar.month_name[month_number]


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

# Compute monthly aggregates for each dataframe in "expenses"
monthly_aggregates = {}
for dataframe_name in expenses:
    # Loop over dataframes
    df = expenses[dataframe_name]
    # Group by month and year, and sum the 'Import' values for each group
    monthly_aggregate = (
        df.groupby(
            [df["Date"].dt.year.rename("Year"), df["Date"].dt.month.rename("Month")]
        )["Import"]
        .sum()
        .reset_index()
    )

    # Rename columns for clarity
    monthly_aggregate.columns = ["Year", "Month", "Monthly Import"]

    # Force column types
    monthly_aggregate["Year"] = monthly_aggregate["Year"].astype(int)
    monthly_aggregate["Month"] = monthly_aggregate["Month"].apply(
        convert_month_numbers_to_names
    )
    monthly_aggregate["Monthly Import"] = (
        monthly_aggregate["Monthly Import"].astype(float).round(2)
    )
    # Store dataframe in dictionary
    monthly_aggregates[dataframe_name] = monthly_aggregate

# Compute total expenses
rows = []
for dataframe_name in expenses:
    total = expenses[dataframe_name]["Import"].sum().astype(float).round(2)
    rows.append({"Category": dataframe_name, "Total import": total})

total_aggregates = pd.DataFrame(rows)

pdf_creator = PDFcreator(pdf_dir, pdf_name)
pdf_creator.build_pdf(total_aggregates, monthly_aggregates)