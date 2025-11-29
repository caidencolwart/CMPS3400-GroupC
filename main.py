from method_1 import DataVisualizer, AdvancedDataVisualizer
from method_2 import placeholderName, dataCalculations
import os
import sys

def main():
  csv_path = "Input.csv"
  __pklpath = "data.pkl"
  # Instantiate parent and child classes
  #parent = DataVisualizer(csv_path)
  #child = AdvancedDataVisualizer(csv_path, base_visualizer=parent)
  
  # Generate and save histogram
  #parent.plot_histogram()
  #parent.plot_line_graph()
  
  #advanced visualizations
  #child.plot_distributions()

  #method 2 methods lol
  placeholderName(csv_path)
  dataCalculations(__pklpath)
  dataCalculations.calcProbabilities()

    
if __name__ == "__main__":
    main()