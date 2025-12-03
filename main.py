import os
import logging

#other imports
from Lib.method_1 import DataVisualizer, AdvancedDataVisualizer
from Lib.method_2 import DataAnalyzer

#%% CONFIGURATION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
os.makedirs("Output/logs", exist_ok=True)
logging.basicConfig(filename="Output/logs/main.log",
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
CSV_PATH = "Input/Input.csv"
PICKLE_PATH = "Input/data.pkl"

#Class definitions Start Here
#Function definitions Start Here
def main():
  logging.info("====Project Started====")
  print("===Project Starting===\n")
  
  #----------------Method_1----------------
  try:
    logging.info("Starting Data Visualization...")
    m1_parent = DataVisualizer(CSV_PATH)
    m1_parent.plot_histogram()
    m1_parent.plot_line_graph()
  
    m1_child = AdvancedDataVisualizer(CSV_PATH, base_visualizer=m1_parent)
    m1_child.plot_violin(column="Peak")
    m1_child.plot_box(column="Peak")
    m1_child.plot_scatter(y="Peak")
  
    query_boolean = m1_child.query_boolean({'Year': 2024, 'Month': "jan"})
    print("Query Result for Year 2024, Month Jan:\n", query_boolean)
    
    logging.info("Data Visualization Completed.")
  except Exception as e:
    logging.error(f"Error in Data Visualization: {e}")
    print(f"[M1] Error: {e}")
  
  #----------------Method_2----------------
  try:
    logging.info("Starting Data Analysis...")
    m2 = DataAnalyzer(PICKLE_PATH)

    stats = m2.statistics('Peak', 'Gain')
    print("\n[M2] Statistics")
    for col, s in stats.items():
      print(f"{col}: Mean{s['mean']}, Median: {s['median']}, Std: {s['std']}")
  
    v1 = m2.vector('Peak')
    v2 = m2.vector('Gain')
    print("Dot Product of 'Peak' and 'Gain':", m2.dot_product(v1, v2))

    month_peak = m2.display_month_peak_info()
    print("\n[M2] Month Peak Info:\n", month_peak)
  
    joint = m2.joint_counts('Year', 'Month')
    print("\n[M2] Joint Counts:\n", joint)
  
    logging.info("Data Analysis Completed.")
  except Exception as e:
    logging.error(f"Error in Data Visualization: {e}")
    print(f"[M1] Error: {e}")
    
logging.info("===Project Ended===\n")
print("===Project Ended===\n")  
    
#%% SELF-RUN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
  main()