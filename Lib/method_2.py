"""
Data processing and analysis module for handling pickle files and statistical operations.
"""
import os
import pickle
from itertools import combinations, permutations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# %% CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CONFIG = {
    "EXPORT_DIR": "Output/",
    "PLOT_DIR": "Output/plots/"
}

os.makedirs(CONFIG["EXPORT_DIR"], exist_ok=True)
os.makedirs(CONFIG["PLOT_DIR"], exist_ok=True) 


# %% CLASS DEFINITIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ===========================================================
# Parent Class 2
# ===========================================================
class DataProcessorBase:
    """Base class for data processing with pickle file support."""

    def __init__(self, pickle_path="data.pkl", **kwargs):
        """Initialize data processor.
        
        Args:
            pickle_path (str): Path to pickle file containing data.
            **kwargs: Additional settings.
        """
        self.__pickle_path = pickle_path
        self.__settings = kwargs
        self.data = self._load_pickle(self.__pickle_path)

    def _load_pickle(self, path):
        """Load data from a pickle file.
        
        Args:
            path (str): Path to pickle file.
            
        Returns:
            Loaded pickle object.
        """
        with open(path, "rb") as f:
            return pickle.load(f)

    def _export_text(self, filename, content):
        """Export text content to file.
        
        Args:
            filename (str): Output filename.
            content: Content to export.
            
        Returns:
            str: Path to exported file.
        """
        path = os.path.join(CONFIG["EXPORT_DIR"], filename)
        with open(path, "w") as f:
            f.write(str(content))
        print(f"Exported text to {path}")
        return path

    def _save_plot(self, filename):
        """Save current plot to file.
        
        Args:
            filename (str): Output filename.
            
        Returns:
            str: Path to saved plot.
        """
        path = os.path.join(CONFIG["PLOT_DIR"], filename)
        plt.savefig(path)
        plt.close()
        return path


# ===========================================================
# Child Class 2
# ===========================================================
class DataAnalyzer(DataProcessorBase):
    """Analyzer class for statistical operations on data."""

    def __init__(self, pickle_path="data.pkl", *args, **kwargs):
        """Initialize analyzer.
        
        Args:
            pickle_path (str): Path to pickle file.
            *args: Variable arguments.
            **kwargs: Keyword arguments.
        """
        super().__init__(pickle_path, **kwargs)
        self.__internal_flag = True

    def _col(self, column):
        """Safely retrieve a column from data.
        
        Args:
            column (str): Column name.
            
        Returns:
            pd.Series: Column data.
            
        Raises:
            ValueError: If column not found.
        """
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found.")
        return self.data[column]

    def statistics(self, *columns):
        """Calculate summary statistics for given columns.
        
        Args:
            *columns: Column names to analyze.
            
        Returns:
            dict: Statistics for each column.
        """
        results = {}
        for col in columns:
            c = self._col(col)
            results[col] = {
                "mean": c.mean(),
                "median": c.median(),
                "std": c.std()
            }

        print("\n" + "=" * 60)
        print("SUMMARY STATISTICS".center(60))
        print("=" * 60)
        for col, stats in results.items():
            print(f"\nColumn: {col}")
            print(f"{'Mean':<10} | {'Median':<10} | {'Std Dev':<10}")
            print(f"{stats['mean']:<10.2f} | {stats['median']:<10.2f} | {stats['std']:<10.2f}")
        print("=" * 60 + "\n")
        return results

    def joint_counts(self, col1, col2):
        """Create cross-tabulation of two columns.
        
        Args:
            col1 (str): First column name.
            col2 (str): Second column name.
            
        Returns:
            pd.DataFrame: Cross-tabulation table.
        """
        table = pd.crosstab(self._col(col1), self._col(col2))
        print("\n" + "=" * 80)
        print(f"JOINT COUNTS: {col1} x {col2}".center(80))
        print("=" * 80)
        print(table.to_string())
        print("=" * 80 + "\n")
        return table

    def vector(self, column):
        """Convert column to numpy vector.
        
        Args:
            column (str): Column name.
            
        Returns:
            np.ndarray: Column as vector.
        """
        vec = self._col(column).to_numpy()
        print(f"\nVector for column '{column}':\n{vec}\n")
        return vec

    def dot_product(self, *vectors):
        """Compute dot product of vectors.
        
        Args:
            *vectors: Vectors to multiply.
            
        Returns:
            Result of dot product.
        """
        result = vectors[0]
        for v in vectors[1:]:
            result = np.dot(result, v)
        print(f"\nDot product result:\n{result}\n")
        return result

    def bin_numeric_column(self, column, bins, labels=None):
        """Bin a numeric column into discrete categories.
        
        Args:
            column (str): Column name to bin.
            bins: Bin edges.
            labels (list, optional): Custom labels for bins.
            
        Returns:
            pd.Series: Binned data.
        """
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in data.")
        
        numeric_col = self.data[column]
        if labels is None:
            labels = [
                f"{int(bins[i])}-{int(bins[i+1]-1)}"
                for i in range(len(bins) - 1)
            ]
        return pd.cut(numeric_col, bins=bins, labels=labels, include_lowest=True)

    def display_month_peak_info(self, peak_column="Peak", month_column="Month",
                                 bins=None, r=2):
        """Display month-peak relationships with permutations and combinations.
        
        Args:
            peak_column (str): Peak data column name.
            month_column (str): Month data column name.
            bins (list, optional): Custom bins for peak data.
            r (int): Order for permutations/combinations.
            
        Returns:
            dict: Report containing unique pairs, permutations, combinations, binned data.
        """
        if (month_column not in self.data.columns or
                peak_column not in self.data.columns):
            raise ValueError("Specified columns not found in data.")

        if bins is None:
            max_val = self.data[peak_column].max()
            bins = list(range(0, int(max_val + 50000), 50000))

        peak_binned = self.bin_numeric_column(peak_column, bins)
        combined = self.data[[month_column]].copy()
        combined["PeakBin"] = peak_binned
        combined_pairs = combined.apply(
            lambda row: (row[month_column], row["PeakBin"]), axis=1
        )
        uniq = combined_pairs.unique()
        perms = list(permutations(uniq, r))
        combs = list(combinations(uniq, r))

        print("\n" + "=" * 80)
        print(" MONTH × PEAK BIN REPORT".center(80))
        print("=" * 80)
        print(f" Number of Unique Month-Peak pairs : {len(uniq)}")
        print(f" r-value (order) : {r}")
        print("-" * 80)
        print("\nUNIQUE MONTH × PEAK BIN PAIRS:")
        for i, val in enumerate(uniq, start=1):
            print(f" {i:>3}. {val}")

        print("\nPERMUTATIONS (ordered pairs):")
        print(f" Total permutations: {len(perms)}")
        for i, p in enumerate(perms, start=1):
            print(f" {i:>3}. {p}")

        print("\nCOMBINATIONS (unordered pairs):")
        print(f" Total combinations: {len(combs)}")
        for i, c in enumerate(combs, start=1):
            print(f" {i:>3}. {c}")
        print("=" * 80 + "\n")

        return {
            "unique_pairs": uniq,
            "permutations": perms,
            "combinations": combs,
            "binned_dataframe": combined
        }


# %% FUNCTION DEFINITIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    """Main execution function."""
    pass


# %% SELF-RUN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print("Executing method_2 as main program.")
    main()