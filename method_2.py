import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import permutations, combinations
from autolog import auto_log, log_activity


class DataProcessorBase:

    @auto_log
    def __init__(self, pickle_path="data.pkl", log_filename="output.txt", **kwargs):
        self.__pickle_path = pickle_path
        self.__settings = kwargs

        self.data = self._load_pickle(self.__pickle_path)

        self.export_dir = "Output/"
        self.plot_dir = "Output/plots/"
        os.makedirs(self.export_dir, exist_ok=True)
        os.makedirs(self.plot_dir, exist_ok=True)

        # Output file setup (renamed from log to output)
        self.log_file = os.path.join(self.export_dir, log_filename)
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write("=== Output Log ===\n")

    @auto_log
    def _log(self, text):
        """Append text to output.txt and optionally print to console."""
        with open(self.log_file, "a") as f:
            f.write(text + "\n")
        

    @auto_log
    def _load_pickle(self, path):
        with open(path, "rb") as f:
            return pickle.load(f)

    @auto_log
    def _export_text(self, filename, content):
        path = os.path.join(self.export_dir, filename)
        with open(path, "w") as f:
            f.write(str(content))
        return path


class DataAnalyzer(DataProcessorBase):

    @auto_log
    def __init__(self, pickle_path="data.pkl", *args, **kwargs):
        super().__init__(pickle_path, **kwargs)
        self.__internal_flag = True

    @auto_log
    def _col(self, column):
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found.")
        return self.data[column]

    @auto_log
    def statistics(self, *columns):
        results = {}

        header = "\n" + "="*60 + "\n" + "SUMMARY STATISTICS".center(60) + "\n" + "="*60
        self._log(header)

        for col in columns:
            c = self._col(col)
            stats = {
                "mean": c.mean(),
                "median": c.median(),
                "std": c.std()
            }
            results[col] = stats

            block = (
                f"\nColumn: {col}\n"
                f"{'Mean':<10} | {'Median':<10} | {'Std Dev':<10}\n"
                f"{stats['mean']:<10.2f} | {stats['median']:<10.2f} | {stats['std']:<10.2f}"
            )
            self._log(block)

        self._log("="*60 + "\n")
        return results

    @auto_log
    def joint_counts(self, col1, col2):
        table = pd.crosstab(self._col(col1), self._col(col2))

        header = (
            "\n" + "="*80 + "\n" +
            f"JOINT COUNTS: {col1} x {col2}".center(80) +
            "\n" + "="*80
        )
        self._log(header)
        self._log(table.to_string())
        self._log("="*80 + "\n")

        return table
    
    @auto_log
    def vector(self, column):
        vec = self._col(column).to_numpy()
        self._log(f"\nVector for column '{column}':\n{vec}\n")
        return vec
    
    @auto_log
    def dot_product(self, *vectors):
        result = vectors[0]
        for v in vectors[1:]:
            result = np.dot(result, v)

        self._log(f"\nDot product result:\n{result}\n")
        return result
    
    @auto_log
    def bin_numeric_column(self, column, bins, labels=None):
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in data.")
        numeric_col = self.data[column]
        if labels is None:
            labels = [f"{int(bins[i])}-{int(bins[i+1]-1)}" for i in range(len(bins)-1)]
        return pd.cut(numeric_col, bins=bins, labels=labels, include_lowest=True)

    @auto_log
    def display_month_peak_info(self, peak_column="Peak", month_column="Month", bins=None, r=2):
        if month_column not in self.data.columns or peak_column not in self.data.columns:
            raise ValueError("Specified columns not found in data.")

        if bins is None:
            max_val = self.data[peak_column].max()
            bins = list(range(0, int(max_val + 50000), 50000))

        peak_binned = self.bin_numeric_column(peak_column, bins)
        combined = self.data[[month_column]].copy()
        combined["PeakBin"] = peak_binned

        combined_pairs = combined.apply(lambda row: (row[month_column], row["PeakBin"]), axis=1)
        uniq = combined_pairs.unique()
        perms = list(permutations(uniq, r))
        combs = list(combinations(uniq, r))

        header = (
            "\n" + "=" * 80 + "\n" +
            " MONTH × PEAK BIN REPORT ".center(80) +
            "\n" + "=" * 80
        )
        self._log(header)

        self._log(f" Number of Unique Month-Peak pairs : {len(uniq)}")
        self._log(f" r-value (order)                   : {r}")
        self._log("-" * 80)

        self._log("\nUNIQUE MONTH × PEAK BIN PAIRS:")
        for i, val in enumerate(uniq, start=1):
            self._log(f" {i:>3}. {val}")

        self._log("\nPERMUTATIONS (ordered pairs):")
        self._log(f" Total permutations: {len(perms)}")
        for i, p in enumerate(perms, start=1):
            self._log(f" {i:>3}. {p}")

        self._log("\nCOMBINATIONS (unordered pairs):")
        self._log(f" Total combinations: {len(combs)}")
        for i, c in enumerate(combs, start=1):
            self._log(f" {i:>3}. {c}")

        self._log("=" * 80 + "\n")

        return {
            "unique_pairs": uniq,
            "permutations": perms,
            "combinations": combs,
            "binned_dataframe": combined
        }
