"""Module containing the calculations included in the report."""

import calendar

import pandas as pd


class Calcs:
    """Calculations object."""

    def __init__(self, expenses):
        """Initialize object."""
        self._expenses = expenses

    @staticmethod
    def _convert_month_numbers_to_names(month_number):
        """Convert months from integer ID to string name; 1 -> January."""
        return calendar.month_name[month_number]

    def monthly_aggregate(self):
        """Compute monthly aggregates for each dataframe in 'expenses'."""
        monthly_aggregates = {}
        for dataframe_name in self._expenses:
            # Loop over dataframes
            df = self._expenses[dataframe_name]
            # Group by month and year, and sum the 'Import' values for each group
            monthly_aggregate = (
                df.groupby(
                    [
                        df["Date"].dt.year.rename("Year"),
                        df["Date"].dt.month.rename("Month"),
                    ]
                )["Import"]
                .sum()
                .reset_index()
            )

            # Rename columns for clarity
            monthly_aggregate.columns = ["Year", "Month", "Monthly Import"]

            # Force column types
            monthly_aggregate["Year"] = monthly_aggregate["Year"].astype(int)
            monthly_aggregate["Month"] = monthly_aggregate["Month"].apply(
                self._convert_month_numbers_to_names
            )
            monthly_aggregate["Monthly Import"] = (
                monthly_aggregate["Monthly Import"].astype(float).round(2)
            )
            # Store dataframe in dictionary
            monthly_aggregates[dataframe_name] = monthly_aggregate

        return monthly_aggregates

    def total_aggregate(self):
        """Compute total aggregate per category in 'expenses' dataframe."""
        rows = []
        for dataframe_name in self._expenses:
            total = (
                self._expenses[dataframe_name]["Import"].sum().astype(float).round(2)
            )
            rows.append({"Category": dataframe_name, "Total import": total})

        return pd.DataFrame(rows)
