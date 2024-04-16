"""Module containing the entry point of the expenses report package."""

from expenses_report.calcs import Calcs
from expenses_report.pdf_creator import PDFcreator
from expenses_report.reader import Reader
from expenses_report.settings import (
    CATEGORIES,
    COLUMNS_TO_READ,
    EXPENSES_DIR,
    EXPNESES_FILE_NAME,
    PDF_DIR,
    PDF_NAME,
)

# Load data from Excel sheet
reader = Reader(EXPENSES_DIR, EXPNESES_FILE_NAME)
expenses = reader.from_excel(CATEGORIES, COLUMNS_TO_READ)

# Compute total and monthly aggregates
calcs = Calcs(expenses)
total_aggregate = calcs.total_aggregate()
monthly_aggregate = calcs.monthly_aggregate()

# Create PDF report
pdf_creator = PDFcreator(PDF_DIR, PDF_NAME)
pdf_creator.build_pdf(total_aggregate, monthly_aggregate)
