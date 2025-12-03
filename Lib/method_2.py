"""
Data processing and analysis module for handling pickle files and statistical operations.
"""
import os
import pickle
from itertools import combinations, permutations
from .config import OUTPUT_DIR, PLOT_DIR

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast
import operator as _operator


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
        # Ensure we don't accidentally create nested Output/Output when
        # callers pass filenames that already include the Output directory.
        if os.path.isabs(filename):
            path = filename
        else:
            path = os.path.join(OUTPUT_DIR, os.path.basename(filename))
        with open(path, "w") as f:
            f.write(str(content))
        print(f"Exported text to {path}")
        return path

    def _save_plot(self, filename):
        path = os.path.join(PLOT_DIR, filename)
        plt.savefig(path)
        plt.close()
        return path
    
    def export_dataframe(self, df: pd.DataFrame, filename: str) -> str:
        """Export DataFrame to CSV file.
        
        Args:
            df (pd.DataFrame): DataFrame to export.
            filename (str): Output filename.
            
        Returns:
            str: Path to exported CSV file.
        """
        # Allow callers to pass a dict (e.g., the report returned by
        # `display_month_peak_info`) — prefer `binned_dataframe` when present.
        if isinstance(df, dict):
            if "binned_dataframe" in df and isinstance(df["binned_dataframe"], pd.DataFrame):
                df_to_save = df["binned_dataframe"]
            else:
                df_to_save = pd.DataFrame.from_dict(df)
        else:
            df_to_save = df

        if os.path.isabs(filename):
            path = filename
        else:
            path = os.path.join(OUTPUT_DIR, os.path.basename(filename))

        df_to_save.to_csv(path, index=False)
        print(f"Exported DataFrame to {path}")
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
    
    def export_statistics(self, stats: dict, filename: str) -> str:
        """Export statistics dictionary to CSV file.
        
        Args:
            stats (dict): Statistics data.
            filename (str): Output filename.
            
        Returns:
            str: Path to exported CSV file.
        """
        df = pd.DataFrame.from_dict(stats, orient='index')
        return self.export_dataframe(df, filename)

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
    
    def joint_probabilities(self, col1, col2):
        counts = self.joint_counts(col1, col2)
        total = counts.values.sum()
        joint_probs = counts / total
        print("\n=== JOINT PROBABILITIES ===", joint_probs)
        return joint_probs
    
    def conditional_probabilities(self, col1, col2):
        joint_probs = self.joint_probabilities(col1, col2)
        cond_probs = joint_probs.div(joint_probs.sum(axis=1), axis=0)
        print("\n=== CONDITIONAL PROBABILITIES ===", cond_probs)
        return cond_probs

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
    
    def export_vector(self, vector: np.ndarray, filename: str) -> str:
        df = pd.DataFrame(vector, columns=["Value"])
        return self.export_dataframe(df, filename)

    def export_numpy_array(self, array, filename: str, columns: list = None) -> str:
        """Convert a 1-D or 2-D numpy array to a DataFrame and export it.

        Args:
            array: Array-like object (1-D or 2-D) to convert.
            filename (str): Output filename (basename or path).
            columns (list, optional): Column names for DataFrame. If provided,
                its length must match the number of columns in the array.

        Returns:
            str: Path to exported CSV file.
        """
        arr = np.asarray(array)

        if arr.ndim == 1:
            # treat as single column
            if columns is not None and len(columns) != 1:
                raise ValueError("When exporting a 1-D array, 'columns' must have length 1 if provided.")
            df = pd.DataFrame(arr, columns=columns if columns is not None else ["Value"])

        elif arr.ndim == 2:
            ncols = arr.shape[1]
            if columns is not None:
                if len(columns) != ncols:
                    raise ValueError("Length of 'columns' must match number of columns in the array.")
                df = pd.DataFrame(arr, columns=columns)
            else:
                df = pd.DataFrame(arr)

        else:
            raise ValueError("Array must be 1-D or 2-D")

        return self.export_dataframe(df, filename)

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
    
    def unit_vector(self, vector: np.ndarray) -> np.ndarray:
        u_vec = vector / np.linalg.norm(vector)
        print(f"\nUnit vector:\n{u_vec}\n")
        return u_vec
    
    def projection(self, a: np.ndarray, b: np.ndarray) -> float:
        proj = (np.dot(a, b) / np.dot(b, b)) * b
        print(f"\nProjection of vector a onto b:\n{proj}\n")
        return proj
    
    def angle_between(self, a: np.ndarray, b: np.ndarray) -> float:
        cos_theta = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        angle = np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))
        print(f"\nAngle between vectors a and b: {angle} degrees\n")
        return angle
    
    def check_orthogonality(self, a: np.ndarray, b: np.ndarray) -> bool:
        ortho = np.isclose(np.dot(a, b), 0)
        print(f"\nVectors a and b are orthogonal: {ortho}\n")
        return ortho
        

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
        
    def plot_binned_column(self, column: str, bins: list):
        binned = self.bin_numeric_column(column, bins)
        counts = binned.value_counts().sort_index()
        counts.plot(kind='bar', title=f"Binned Distribution of {column}")
        return self._save_plot(f"binned_{column}.png")


# %% FUNCTION DEFINITIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    """Main execution function."""
    pass


# %% SELF-RUN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print("Executing method_2 as main program.")
    main()


# ===========================================================
# Safe expression evaluator
# ===========================================================
class Eval:
    """A very small safe evaluator for arithmetic expressions.

    Supports literals, arithmetic operators and parentheses. It uses Python's
    AST to parse expressions and only allows a restricted set of nodes.
    """

    # supported operators mapping
    _ops = {
        ast.Add: _operator.add,
        ast.Sub: _operator.sub,
        ast.Mult: _operator.mul,
        ast.Div: _operator.truediv,
        ast.FloorDiv: _operator.floordiv,
        ast.Mod: _operator.mod,
        ast.Pow: _operator.pow,
        ast.USub: _operator.neg,
        ast.UAdd: _operator.pos,
    }

    def eval(self, expression: str):
        """Evaluate a simple arithmetic expression safely.

        Args:
            expression (str): The expression to evaluate.

        Returns:
            The numeric result of the expression.
        """
        node = ast.parse(expression, mode='eval')
        return self._eval_node(node.body)

    def _eval_node(self, node):
        # Numbers
        if isinstance(node, ast.Num):
            return node.n
        # Constant for Python 3.8+
        if hasattr(ast, 'Constant') and isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant: {node.value}")

        # Binary operations
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type in self._ops:
                return self._ops[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type}")

        # Unary operations
        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in self._ops:
                return self._ops[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type}")

        # Parenthesis and grouping handled by AST structure naturally
        raise ValueError(f"Unsupported expression node: {type(node)}")


# single shared evaluator instance for module users
evaluator = Eval()


if __name__ == "__main__":
    # Run the evaluator example after the instance is created
    try:
        print("\nEval example: evaluator.eval('2 + 3 * (4 - 1)') =>", evaluator.eval('2 + 3 * (4 - 1)'))
    except Exception as e:
        print("Eval example failed:", e)


# ===========================================================
# Example closure using `nonlocal`
# ===========================================================
def make_nonlocal_counter(start: int = 0, step: int = 1):
    count = start

    def _inc():
        nonlocal count
        count += step
        return count

    # attach a small helper to read current value without incrementing
    def _get():
        return count

    _inc.get = _get
    return _inc

# module-level instance demonstrating nonlocal state
nonlocal_counter = make_nonlocal_counter(0, 1)