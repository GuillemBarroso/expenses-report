"""Module containing the creation of the report in pdf format."""

import os

from fpdf import FPDF


class PDFcreator:
    """PDF creator class."""

    def __init__(self, pdf_dir, pdf_name):
        """Initialize object."""
        self.pdf_dir = pdf_dir
        self.pdf_name = pdf_name

        self._pdf = FPDF()
        self._pdf.set_auto_page_break(auto=True, margin=15)

    def _create_table(self, df, table_name):
        """Create table from a dataframe under a certain table_name."""
        self._pdf.cell(200, 10, txt=f"{table_name}", ln=True, align="C")
        self._pdf.ln(5)

        # Calculate table width
        table_width = 40 * len(df.columns)

        # Center-align the table
        x_start = (self._pdf.w - table_width) / 2

        # Draw table headers
        headers = df.columns
        for header in headers:
            self._pdf.set_xy(x_start, self._pdf.get_y())
            self._pdf.cell(40, 10, txt=str(header), border=1, ln=False, align="C")
            x_start += 40
        self._pdf.ln()

        # Draw table data
        for _, row in df.iterrows():
            x_start = (self._pdf.w - table_width) / 2
            for col in row:
                self._pdf.set_xy(x_start, self._pdf.get_y())
                self._pdf.cell(40, 10, txt=str(col), border=1, ln=False, align="C")
                x_start += 40
            self._pdf.ln()

        self._pdf.ln(5)  # Add some space between tables

    def _save_pdf(self):
        """Write pdf file under specified directory and name."""
        self._pdf.output(os.path.join(self.pdf_dir, self.pdf_name))
        print(f"PDF file '{self.pdf_name}' has been created.")

    def build_pdf(self, total_aggregates, monthly_aggregates):
        """Build pdf structure."""
        # Add page with total aggregates
        self._pdf.add_page()
        self._pdf.set_font("Arial", size=10)
        self._create_table(total_aggregates, "Totals")

        # Add pages with monthly aggregates
        self._pdf.add_page()
        self._pdf.set_font("Arial", size=10)
        for expense_type, df in monthly_aggregates.items():
            self._create_table(df, expense_type)

        # Write file
        self._save_pdf()
