from method_1 import DataVisualizer, AdvancedDataVisualizer
from method_2 import DataProcessorBase, DataAnalyzer
import os
import sys

def main():
  csv_path = "Input.csv"
  # Instantiate parent and child classes
  parent = DataVisualizer(csv_path)
  child = AdvancedDataVisualizer(csv_path, base_visualizer=parent)
  
  # Generate and save histogram
  parent.plot_histogram()
  parent.plot_line_graph()
  
  #advanced visualizations
  child.plot_distributions()

  #method 2 methods lol
  an = DataAnalyzer("data.pkl")

  print(an.statistics("Peak", "Gain"))

  v1 = an.vector("Peak")
  v2 = an.vector("Gain")
  print(an.dot_product(v1, v2))
  an.display_month_peak_info()
    
if __name__ == "__main__":
    main()