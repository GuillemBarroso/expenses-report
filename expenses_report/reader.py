"""Module that reads the user input data."""

import os

import pandas as pd


class Reader:
    """Reader object to get expenses data."""

    def __init__(self, expenses_dir, expenses_file_name):
        """Initialize object."""
        self.expenses_dir = expenses_dir
        self.expenses_file_name = expenses_file_name

    def from_excel(self, categories, columns_to_read):
        """Read data from excel sheet."""
        excel_file = pd.ExcelFile(
            os.path.join(self.expenses_dir, self.expenses_file_name)
        )

        # Create a dictionary of dataframes
        expenses = {}
        for sheet_name in excel_file.sheet_names:
            if sheet_name in categories:
                # Read only the specified columns from the current sheet into a DataFrame
                df = pd.read_excel(
                    excel_file, sheet_name=sheet_name, usecols=columns_to_read
                )

                # Convert "Date" column to datetime format if exists
                if "Date" in df.columns:
                    df["Date"] = pd.to_datetime(df["Date"])

                # Store the DataFrame in the dictionary with the sheet name as key
                expenses[sheet_name] = df

        return expenses
