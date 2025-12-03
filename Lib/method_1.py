#Version: v1.0
#Date Last Updated: 02-12-2025
#%% MODULE BEGINS
module_name_gl = 'method_1'
'''
Version: v1.0
Description: 
-Method_1 parent class, reads CSV files and creates basic plots
-AdvancedDataVisualizer child class, extends parent with advanced plots and queries
Authors: Caiden Colwart & Ethan Cochran
Date Created : 
Date Last Updated: 03-12-2025
Doc:
-all reqs have been met
Notes:
-all plots export to Output/plots
-reads from Input/data.csv 
'''
#%% IMPORTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates



#%% CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CONFIG = {
    "PLOT_DIR": "Output/plots/",
    "HIST_BINS": 10,
    "LINE_FIGSIZE": (20,10),
    "VIOLIN_FIGSIZE": (10,5),
    "SCATTER_FIGSIZE": (8, 5),
}
#%% CONFIGURATION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
os.makedirs(CONFIG["PLOT_DIR"], exist_ok=True)

#%% DECLERATIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Class defs start here
#===========================================================
# Parent Class 1
#===========================================================
class DataVisualizer:
    def __init__(self, csv_path,):
        self.filepath = csv_path
        self.data = pd.read_csv(csv_path)  
        
        #clean column names      
        self.data.columns = [col.strip() for col in self.data.columns]
        
        #clean data
        numeric_targets = ["Peak", "Gain", "%Gain"]
        for col in numeric_targets:
            if col in self.data.columns:
                self.data[col] = (
                    self.data[col]
                    .astype(str)
                    .str.replace(",", "", regex=False)
                    .str.replace("%", "", regex=False)
                )
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
        
        #Fix Date column
        if "Month" in self.data.columns and "Year" in self.data.columns:

            # Convert Month (Jan, Feb, ...) → number (1-12)
            self.data["Month_num"] = pd.to_datetime(
                self.data["Month"], format="%b", errors="coerce"
            ).dt.month

            # Build proper datetime
            self.data["Date"] = pd.to_datetime(
                {
                    "year": self.data["Year"].astype(int),
                    "month": self.data["Month_num"].astype(int),
                    "day": 1,
                },
                errors="coerce"
            )

            # Sort chronologically
            self.data.sort_values("Date", inplace=True)
            self.data.reset_index(drop=True, inplace=True)

            
        for col in ["Peak", "Gain", "%Gain"]:
            if col not in self.data.columns:
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
        
    #-----------Simple Query Method-------------------------    
    def query_simple(self, column, value):
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' does not exist in the data.")
        return self.data[self.data[column] == value]


    #-----------Histogram-------------------------       
    def plot_histogram(self, column = "Peak"):  
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' does not exist in the data.")
        
        clean = pd.to_numeric(self.data[column], errors='coerce').dropna()
              
        plt.figure(figsize=(12,5))
        plt.hist(clean, edgecolor='skyblue', bins=CONFIG["HIST_BINS"])
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.grid(True, axis='y', alpha=0.75)
        
        out = os.path.join(CONFIG["PLOT_DIR"], f"histogram_{column}.png")
        plt.savefig(out)
        plt.close()
        print(f"Histogram saved to {out}")
            
    #-----------Line Plot-------------------------                 
    def plot_line_graph(self, y_column = "Peak"):
        if "Date" not in self.data.columns:
            raise ValueError("does not exist in the data.")
        
        clean = self.data[["Date", y_column]].dropna()
        
        clean["Month-year"] = clean["Date"].dt.strftime("%b-%Y")
        
        clean = clean.sort_values("Date")
                        
        plt.figure(figsize=CONFIG["LINE_FIGSIZE"])
        plt.plot(clean["Month-year"], clean[y_column], marker='o', linestyle='-')
        
        plt.title(f"{y_column} over Time")
        plt.xlabel("Date (Month-year)")
        plt.ylabel(y_column)
        plt.xticks(rotation=90, fontsize=6)
        plt.tight_layout()
        
        out = os.path.join(CONFIG["PLOT_DIR"], f"line_{y_column}.png")
        plt.savefig(out) 
        plt.close()
        print(f"Line graph saved to {out}")
#===========================================================
# Child Class 1
#===========================================================
class AdvancedDataVisualizer(DataVisualizer):
    def __init__(self, csv_path, base_visualizer=None):
        if base_visualizer:
            self.filepath = base_visualizer.filepath
            self.data = base_visualizer.data
        else:
            super().__init__(csv_path)        
            
    #-----------Violin Plot-------------------------
    def plot_violin(self, column="Peak"):
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' does not exist in the data.")
        
        clean = self.data[["Year", column]].dropna()
        clean[column] = pd.to_numeric(clean[column], errors='coerce')
        clean = clean.dropna()  
        
        years = sorted(clean['Year'].unique())
        grouped = [clean[clean['Year'] == y][column].dropna() for y in years]
        
        plt.figure(figsize=CONFIG["VIOLIN_FIGSIZE"])
        plt.violinplot(grouped)
        plt.xticks(range(1, len(years) + 1), years)
        plt.title(f"Violin Plot of {column} by Year")
        plt.grid(True, linestyle="--", alpha=0.7)

        out = os.path.join(CONFIG["PLOT_DIR"], f"violin_{column}.png")
        plt.savefig(out)
        plt.close()
        print(f"Violin plot saved to {out}")
            
    #-----------Box Plot-------------------------    
    def plot_box(self, column="Peak"):   
        clean = pd.to_numeric(self.data[column], errors='coerce').dropna()
        
        plt.figure(figsize=(8, 4))
        plt.boxplot(clean, vert=False)
        plt.title(f"Box Plot of {column}")
        plt.grid(True, axis="x", linestyle="--", alpha=0.7)

        out = os.path.join(CONFIG["PLOT_DIR"], f"box_{column}.png")
        plt.savefig(out)
        plt.close()
        print(f"Box plot saved to {out}")     
        
            
    #-----------Scatter Plot-------------------------   
    def plot_scatter(self, y = "Peak"):
        if "Date" not in self.data.columns:
            raise ValueError("Date column does not exist in the data.")
        
        clean = self.data[["Date", y]].dropna()
        clean[y] = pd.to_numeric(clean[y], errors='coerce')
        clean = clean.dropna()
        
        plt.figure(figsize= CONFIG["SCATTER_FIGSIZE"])
        plt.scatter(clean["Date"], clean[y], alpha=0.7)
        
        x = clean["Date"].map(lambda d: d.toordinal())
        y_values = clean[y].values
        coef = np.polyfit(x, y_values, 1)
        poly = np.poly1d(coef)
        
        plt.plot(clean["Date"], poly(x), color='red', linestyle='--', label='Trend Line')
        
        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        plt.xticks(rotation=45)
        
        plt.title(f"Scatter Plot of {y} vs Date with Trend Line")
        plt.xlabel("Year")
        plt.ylabel(y)
        plt.legend()
        
        out = os.path.join(CONFIG["PLOT_DIR"], f"scatter_{y}_vs_Date.png")
        plt.savefig(out)
        plt.close()
        print(f"Scatter plot saved to {out}")
     
    #-----------Boolean Indexinv Query-------------------------     
    def query_boolean(self, conditions: dict): 
        mask = pd.Series([True] * len(self.data))
        for col, val in conditions.items():
            if col not in self.data.columns:
                raise ValueError(f"Column '{col}' does not exist in the data.")
            mask &= (self.data[col] == val)
        return self.data[mask]
    
#%% MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    pass

#%% SELF-RUN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print(f"Executing {module_name_gl} as main program.")
    main()