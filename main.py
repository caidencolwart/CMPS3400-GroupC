import os
import logging
import numpy as np

#other imports
from Lib.method_1 import DataVisualizer, AdvancedDataVisualizer
from Lib.method_2 import DataAnalyzer
from Lib.config import LOG_DIR

# Ensure we log to a file (LOG_DIR is a directory). Use a concrete logfile path.
LOG_FILE = os.path.join(LOG_DIR, "app.log")

#%% CONFIGURATION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
logging.basicConfig(filename=LOG_FILE,
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
    m2.export_vector(v1, "Output/Peak_Vector.csv")
    m2.export_vector(v2, "Output/Gain_Vector.csv")
    # Example: create an m x n array from two vectors and export it
    try:
      arr = np.vstack((v1, v2)).T
      exported = m2.export_numpy_array(arr, "Peak_Gain_matrix.csv", columns=["Peak", "Gain"])
      print(f"Exported numpy matrix to: {exported}")
    except Exception as e:
      logging.warning(f"Failed to export numpy array demo: {e}")
    
    print("Dot Product of 'Peak' and 'Gain':", m2.dot_product(v1, v2))
    m2.unit_vector(v1)
    m2.unit_vector(v2)
    m2.projection(v1, v2)
    m2.angle_between(v1, v2)
    m2.check_orthogonality(v1, v2)

    month_peak = m2.display_month_peak_info()
    m2.export_dataframe(month_peak, "Output/Month_Peak_Info.csv")
  
    joint_counts = m2.joint_counts('Year', 'Month')
    joint_probs = m2.joint_probabilities('Year', 'Month')
    cond_probs = m2.conditional_probabilities('Year', 'Month')
    m2.export_dataframe(joint_counts, "Output/Joint_Counts_Year_Month.csv")
    m2.export_dataframe(joint_probs, "Output/Joint_Probabilities_Year_Month.csv")
    m2.export_dataframe(cond_probs, "Output/Conditional_Probabilities_Year_Month.csv")
  
    logging.info("Data Analysis Completed.")
  except Exception as e:
    logging.error(f"Error in Data Analysis: {e}")
    print(f"[M2] Error: {e}")
    
  logging.info("===Project Ended===\n")
  print("===Project Ended===\n")  
    
#%% SELF-RUN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
  main()