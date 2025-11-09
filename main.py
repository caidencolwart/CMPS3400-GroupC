from method_1 import DataVisualizer, AdvancedDataVisualizer
import os
import sys

def main():
  csv_path = "Input.csv"
  
  # Instantiate parent and child classes
  parent = DataVisualizer(csv_path)
  child = AdvancedDataVisualizer(csv_path, base_visualizer=parent)
  
  # Generate and save histogram
  parent.plot_histogram()
  
  #advanced visualizations
  child.plot_distributions()
    
if __name__ == "__main__":
    main()