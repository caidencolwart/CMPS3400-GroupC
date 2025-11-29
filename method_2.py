import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import permutations, combinations

class DataProcessorBase:

    def __init__(self, pickle_path="data.pkl", **kwargs):
        self.__pickle_path = pickle_path
        self.__settings = kwargs

        self.data = self._load_pickle(self.__pickle_path)

        self.export_dir = "Output/"
        self.plot_dir = "Output/plots/"
        os.makedirs(self.export_dir, exist_ok=True)
        os.makedirs(self.plot_dir, exist_ok=True)

    def _load_pickle(self, path):
        with open(path, "rb") as f:
            return pickle.load(f)

    def _export_text(self, filename, content):
        path = os.path.join(self.export_dir, filename)
        with open(path, "w") as f:
            f.write(str(content))
        return path

    def _save_plot(self, filename):
        path = os.path.join(self.plot_dir, filename)
        plt.savefig(path)
        plt.close()
        return path

class DataAnalyzer(DataProcessorBase):

    def __init__(self, pickle_path="data.pkl", *args, **kwargs):
        super().__init__(pickle_path, **kwargs)
        self.__internal_flag = True

    def _col(self, column):
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found.")
        return self.data[column]

    def statistics(self, *columns):
        results = {}
        for col in columns:
            c = self._col(col)
            results[col] = {
                "mean": c.mean(),
                "median": c.median(),
                "std": c.std()
            }

        print("\n" + "="*60)
        print("SUMMARY STATISTICS".center(60))
        print("="*60)
        for col, stats in results.items():
            print(f"\nColumn: {col}")
            print(f"{'Mean':<10} | {'Median':<10} | {'Std Dev':<10}")
            print(f"{stats['mean']:<10.2f} | {stats['median']:<10.2f} | {stats['std']:<10.2f}")
        print("="*60 + "\n")
        return results

    def joint_counts(self, col1, col2):
        table = pd.crosstab(self._col(col1), self._col(col2))
        print("\n" + "="*80)
        print(f"JOINT COUNTS: {col1} x {col2}".center(80))
        print("="*80)
        print(table.to_string())
        print("="*80 + "\n")
        return table

    def vector(self, column):
        vec = self._col(column).to_numpy()
        print(f"\nVector for column '{column}':\n{vec}\n")
        return vec

    def dot_product(self, *vectors):
        result = vectors[0]
        for v in vectors[1:]:
            result = np.dot(result, v)
        print(f"\nDot product result:\n{result}\n")
        return result

    def bin_numeric_column(self, column, bins, labels=None):
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in data.")
        numeric_col = self.data[column]
        if labels is None:
            labels = [f"{int(bins[i])}-{int(bins[i+1]-1)}" for i in range(len(bins)-1)]
        return pd.cut(numeric_col, bins=bins, labels=labels, include_lowest=True)

    def display_month_peak_info(self, peak_column="Peak", month_column="Month", bins=None, r=2):
        if month_column not in self.data.columns or peak_column not in self.data.columns:
            raise ValueError("Specified columns not found in data.")

        # Default bins: 0, 50k, 100k, ... up to max(Peak)
        if bins is None:
            max_val = self.data[peak_column].max()
            bins = list(range(0, int(max_val + 50000), 50000))

        peak_binned = self.bin_numeric_column(peak_column, bins)
        combined = self.data[[month_column]].copy()
        combined["PeakBin"] = peak_binned

        # Create Month × PeakBin pairs
        combined_pairs = combined.apply(lambda row: (row[month_column], row["PeakBin"]), axis=1)
        uniq = combined_pairs.unique()
        perms = list(permutations(uniq, r))
        combs = list(combinations(uniq, r))

        print("\n" + "=" * 80)
        print(f" MONTH × PEAK BIN REPORT".center(80))
        print("=" * 80)
        print(f" Number of Unique Month-Peak pairs : {len(uniq)}")
        print(f" r-value (order)                   : {r}")
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