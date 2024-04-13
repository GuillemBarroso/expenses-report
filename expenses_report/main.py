from expenses_report.calcs import Calcs
from expenses_report.pdf_creator import PDFcreator
from expenses_report.reader import Reader

pdf_dir = "./"
pdf_name = "expenses_test_report.pdf"

# Load data from Excel sheet
expenses_dir = r"data"
expenses_file_name = "expenses.xlsx"
categories = ["Category1", "Category2"]
columns_to_read = ["Date", "Import"]
reader = Reader(expenses_dir, expenses_file_name)
expenses = reader.from_excel(categories, columns_to_read)

# Compute total and monthly aggregates
calcs = Calcs(expenses)
total_aggregate = calcs.total_aggregate()
monthly_aggregate = calcs.monthly_aggregate()

# Create PDF report
pdf_creator = PDFcreator(pdf_dir, pdf_name)
pdf_creator.build_pdf(total_aggregate, monthly_aggregate)
