import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

#--------------Parent Class 1-----------------------------
#store configuration constatnts in dictionary
#use histogram to visualize data
#query data for searching
class DataVisualizer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = pd.read_csv(filepath)
        
        #This strips blank space in column names
        self.data.columns = [col.strip() for col in self.data.columns]
        #This converts the Peak and Gain columns to numeric, removing commas
        for col in ["Peak", "Gain"]:
            self.data[col] = self.data[col].astype(str).str.replace(',', '').astype(float)
        self.data["%Gain"] = self.data["%Gain"].astype(str).str.replace(',', '').astype(float)
        
        self.data["MonthYear"] = self.data['Month'] + '-' + self.data['Year'].astype(str)
        
        #Sorts the years in order to plot correctly
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.data['Month_num'] = self.data["Month"].apply(lambda x: month_order.index(x) + 1)
        self.data.sort_values(["Year", "Month_num"], inplace=True)
        self.data.reset_index(drop=True, inplace=True)

    #Histogram plot     
    def plot_histogram(self, save_dir="Output/plots"):
        os.makedirs(save_dir, exist_ok=True)#create directory if not exists
        
        plt.figure(figsize=(20, 6))
        plt.bar(self.data['MonthYear'], self.data["Peak"], color='skyblue')
        
        #Graph formatting
        plt.xticks(rotation=90)
        plt.ylabel('Peak Player Count')
        plt.xlabel("Month-Year")  
        plt.title("Peak Player Count by Month-Year")
        plt.ylim(0, max(self.data["Peak"]) * 1.1)
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Save plot
        out_path = f"{save_dir}/hist.png"
        plt.savefig(out_path)
        plt.close()
        print(f'Histogram saved to {out_path}')
        
    def query_data(self, column, value):
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' does not exist in the data.")
        return self.data[self.data[column] == value]

#--------------Child Class 1------------------------------
#read data from Input.csv
#visualize the data using violin plot, whisker-plot, and box plot
class AdvancedDataVisualizer(DataVisualizer):
    def __init__(self, filepath, base_visualizer: DataVisualizer = None):
        if base_visualizer:
            self.filepath = base_visualizer.filepath
            self.data = base_visualizer.data
        else:
            super().__init__(filepath)
            
    def plot_distributions(self, save_dir="Output/plots"):
        os.makedirs(save_dir, exist_ok=True)

        # Violin Plot
        years = sorted(self.data['Year'].unique())
        data_per_year = [self.data[self.data['Year'] == year]['Peak'] for year in years]
        plt.figure(figsize=(10,5))
        plt.violinplot(data_per_year)
        plt.xticks(range(1, len(years) + 1), years)
        
        plt.title('Violin Plot of Peak Player Counts by Year')
        plt.xlabel('Year')
        plt.ylabel('Peak Player Count')
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        plt.savefig(f"{save_dir}/violin_plot.png")
        plt.close()
        print(f'Violin plot saved to {save_dir}/violin_plot.png')

        # Scatter Plot
        x = self.data['Year'].values
        y = self.data['Peak'].values
        trendline = np.poly1d(np.polyfit(x, y, deg=1))#linear trendline
        
        plt.figure(figsize=(8,5))
        plt.scatter(x, y, color = 'blue', alpha=0.6)
        plt.plot(x, trendline(x), color='red', linewidth=2, label='Trendline')
        plt.xlabel('Peak Player Count')
        plt.ylabel('Year')
        plt.title('Scatter Plot of Peak Player Counts by Year')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        
        plt.savefig(f"{save_dir}/scatter_plot.png")
        plt.close()
        print(f'Scatter plot saved to {save_dir}/scatter_plot.png')

        # Box Plot
        plt.figure(figsize=(8,5))
        plt.boxplot(self.data["Peak"], vert=False)
        
        plt.title('Box Plot of Peak Player Counts')
        plt.xlabel('Peak Player Count')
        plt.grid(True, axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        plt.savefig(f"{save_dir}/box_plot.png")
        plt.close()
        print(f'Box plot saved to {save_dir}/box_plot.png')
        
    #This method allows querying with multiple conditions, Boolean Indexing    
    def query_advanced(self, condition: dict):
        mask = pd.Series([True] * len(self.data))
        for column, value in condition.items(): 
            if column not in self.data.columns:
                mask &= (self.data[column] == value)
            return self.data[mask]