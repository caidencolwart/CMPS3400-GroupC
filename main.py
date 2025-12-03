from method_1 import DataVisualizer, AdvancedDataVisualizer
from method_2 import DataProcessorBase, DataAnalyzer
from ui import load_ui_settings
import os
import sys

def main():
    # Load UI input file
    ui = load_ui_settings("ui.txt")

    # Read UI parameters
    csv_path = ui.get("CSV_PATH", "Input.csv")
    pkl_path = ui.get("PKL_PATH", "data.pkl")

    # Instantiate parent and child classes
    parent = DataVisualizer(csv_path)
    child = AdvancedDataVisualizer(csv_path, base_visualizer=parent)

    # Execute based on user settings
    if ui.get("PLOT_HISTOGRAM", "no").lower() == "yes":
        parent.plot_histogram()

    if ui.get("PLOT_LINE_GRAPH", "no").lower() == "yes":
        parent.plot_line_graph()

    if ui.get("PLOT_DISTRIBUTIONS", "no").lower() == "yes":
        child.plot_distributions()

    # Method 2 analysis
    an = DataAnalyzer(pkl_path)

    if ui.get("SHOW_STATS", "no").lower() == "yes":
        an.statistics("Peak", "Gain")

    if ui.get("VECTOR_COL1") and ui.get("VECTOR_COL2"):
        v1 = an.vector(ui["VECTOR_COL1"])
        v2 = an.vector(ui["VECTOR_COL2"])
        an.dot_product(v1, v2)

    if ui.get("SHOW_MONTH_PEAK", "no").lower() == "yes":
        an.display_month_peak_info()


if __name__ == "__main__":
    main()
