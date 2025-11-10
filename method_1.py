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
        plt.hist(self.data['Peak'], bins=10, color='skyblue')
        
        #Graph formatting
        plt.ylabel('Frequency')
        plt.xlabel("Peak Player Count")  
        plt.title("Frequency of Player Count")
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Save plot
        out_path = f"{save_dir}/hist.png"
        plt.savefig(out_path)
        plt.close()
        print(f'Histogram saved to {out_path}')

    def plot_line_graph(self, save_dir="Output/plots"):
        os.makedirs(save_dir, exist_ok=True)#create directory if not exists
        plt.figure(figsize=(100,20))
        #Temp Placeholder
        plt.plot(["Oct-2019", "Nov-2019", "Dec-2019", "Jan-2020","Feb-2020","Mar-2020","Apr-2020","May-2020","Jun-2020","Jul-2020","Aug-2020","Sep-2020","Oct-2020","Nov-2020","Dec-2020","Jan-2021","Feb-2021","Mar-2021","Apr-2021","May-2021","Jun-2021","Jul-2021","Aug-2021","Sep-2021","Oct-2021","Nov-2021","Dec-2021","Jan-2022","Feb-2022","Mar-2022","Apr-2022","May-2022","Jun-2022","Jul-2022","Aug-2022","Sep-2022","Oct-2022","Nov-2022","Dec-2022","Jan-2023","Feb-2023","Mar-2023","Apr-2023","May-2023","Jun-2023","Jul-2023","Aug-2023","Sep-2023","Oct-2023","Nov-2023","Dec-2023","Jan-2024","Feb-2024","Mar-2024","Apr-2024","May-2024","Jun-2024","Jul-2024","Aug-2024","Sep-2024","Oct-2024","Nov-2024","Dec-2024","Jan-2025","Feb-2025","Mar-2025","Apr-2025","May-2025","Jun-2025","Jul-2025","Aug-2025","Sep-2025"],self.data["Peak"])
        plt.ylabel("Peak Player Count")
        plt.xlabel("Month-Year")
        plt.title("Peak Player Count per Month")
        out_path = f"{save_dir}/line.png"
        plt.savefig(out_path)
        plt.close()
        print(f'Line Plot saved to {out_path}')

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