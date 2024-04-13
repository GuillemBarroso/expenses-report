import pandas as pd
import os
from fpdf import FPDF
import calendar

# Function to convert month numbers to month names
def convert_month_numbers_to_names(month_number):
    return calendar.month_name[month_number]

# Load data from Excel sheet
user_name = "test_user"
expenses_dir = r'data'
expenses_file_name = 'expenses.xlsx'
excel_file = pd.ExcelFile(os.path.join(expenses_dir, expenses_file_name))

# Read "Date" and "Import" columns of each sheet and create a dictionary of dataframes
expenses = {}
columns_to_read = ["Date", "Import"]
for sheet_name in excel_file.sheet_names:
    if sheet_name != "Summary":
        # Read only the specified columns from the current sheet into a DataFrame
        df = pd.read_excel(excel_file, sheet_name=sheet_name, usecols=columns_to_read)

        # Convert "Date" column to datetime format
        df['Date'] = pd.to_datetime(df['Date'])

        # Store the DataFrame in the dictionary with the sheet name as key
        expenses[sheet_name] = df

# Compute monthly aggregates for each dataframe in "expenses"
monthly_aggregates = {}
for dataframe_name in expenses:
    # Loop over dataframes
    df = expenses[dataframe_name]
    # Group by month and year, and sum the 'Import' values for each group
    monthly_aggregate = df.groupby([df['Date'].dt.year.rename('Year'), df['Date'].dt.month.rename('Month')])['Import'].sum().reset_index()

    # Rename columns for clarity
    monthly_aggregate.columns = ['Year', 'Month', 'Monthly Import']

    # Force column types
    monthly_aggregate['Year'] = monthly_aggregate['Year'].astype(int)
    monthly_aggregate['Month'] = monthly_aggregate['Month'].apply(convert_month_numbers_to_names)
    monthly_aggregate['Monthly Import'] = monthly_aggregate['Monthly Import'].astype(float).round(2)
    # Store dataframe in dictionary
    monthly_aggregates[dataframe_name] = monthly_aggregate

# Compute total expenses
rows = []
for dataframe_name in expenses:
    total = expenses[dataframe_name]["Import"].sum().astype(float).round(2)
    rows.append({"Category": dataframe_name, "Total import": total})

total_aggregates = pd.DataFrame(rows)

def create_table(pdf, df, name):
    pdf.cell(200, 10, txt=f"{name}", ln=True, align="C")
    pdf.ln(5)

    # Calculate table width
    table_width = 40 * len(df.columns)

    # Center-align the table
    x_start = (pdf.w - table_width) / 2

    # Draw table headers
    headers = df.columns
    for header in headers:
        pdf.set_xy(x_start, pdf.get_y())
        pdf.cell(40, 10, txt=str(header), border=1, ln=False, align="C")
        x_start += 40
    pdf.ln()

    # Draw table data
    for _, row in df.iterrows():
        x_start = (pdf.w - table_width) / 2
        for col in row:
            pdf.set_xy(x_start, pdf.get_y())
            pdf.cell(40, 10, txt=str(col), border=1, ln=False, align="C")
            x_start += 40
        pdf.ln()

    pdf.ln(5)  # Add some space between tables

# Function to create PDF
def create_pdf(total_aggregates, monthly_aggregates, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add page with total aggregates
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    create_table(pdf, total_aggregates, "Totals")

    # Add pages with monthly aggregates
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    for expense_type, df in monthly_aggregates.items():
        create_table(pdf, df, expense_type)

    pdf.output(filename)

# Create PDF with tables for each DataFrame in the dictionary
pdf_dir = "./"
pdf_name = f"expenses_{user_name}.pdf"
create_pdf(total_aggregates, monthly_aggregates, os.path.join(pdf_dir, pdf_name))

# Print a message once the PDF file is created
print(f"PDF file '{pdf_name}' has been created.")