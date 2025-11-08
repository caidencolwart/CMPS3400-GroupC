import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv as csv

class plot():
    print("hi")



class distributions(plot):
   def violin_plot():
        df = pd.read_csv('Input.csv')
        fig, axes = plt.subplots()
        axes.violinplot(dataset=[
            df[df.Year == 2019]["Peak"].values,
            df[df.Year == 2020]["Peak"].values,
            df[df.Year == 2021]["Peak"].values,
            df[df.Year == 2022]["Peak"].values,
            df[df.Year == 2023]["Peak"].values,
            df[df.Year == 2024]["Peak"].values,
            df[df.Year == 2025]["Peak"].values
        ])
        axes.set_title("Peak Playerbase")
        axes.yaxis.grid(True)
        axes.set_xlabel("Year")
        axes.set_ylabel("Peak Player Count")
        axes.set_xticks([1, 2, 3, 4, 5, 6, 7])
        axes.set_xticklabels(['2019', '2020', '2021', '2022', '2023', '2024', '2025'])
        plt.show() 