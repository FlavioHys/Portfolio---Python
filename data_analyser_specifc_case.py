import pandas as pd

import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class DataLoader:
    """A class for loading data from a CSV file.
    """
    def __init__(self):
        """Initialize the DataLoader class.
        """
        self.first_df = pd.DataFrame()
        self.second_df = pd.DataFrame() 

    def load_data(self, file_path):
        """Load data from a CSV file.

        Args:
            file_path (str): The file path to the CSV file.

        Returns:
            pd.DataFrame: The loaded data as a pandas DataFrame.
        """
        skip_rows = [i for i in range(0, 6)] + [j for j in range(7, 9)]
        df = pd.read_csv(file_path, skiprows=skip_rows)

        # Selecting specific columns for the two dataframes
        self.first_df =\
            df.loc[:, ['Time', 'Harris Church of England Academy, Rugby']]
        self.second_df =\
            df.loc[:, ['Time.1', 'Cardinal Newman Catholic Secondary School ']]

        return self.first_df, self.second_df


class DataAnalyser:
    """A class for analysing data.

    This class provides methods for formatting data, calculating means,
    and calculating standard deviation of air quality index for two locations.

    Attributes:
        data_loader (DataLoader): The DataLoader class used for loading data.
    """

    def __init__(self, data_loader):
        """Initialize the DataAnalyser class.

        Args:
            data_loader (DataLoader): The DataLoader class.
        """
        self.data_loader = data_loader

    def format_data(self):
        """Format the data by converting the location columns to floats and
        concatenating the 'Date' and 'Time' columns into 'Timestamp'.
        """
        # Convert the CO2 readings columns to floats
        self.data_loader.first_df[
                                'Harris Church of England Academy, Rugby'] = \
                                pd.to_numeric(self.data_loader.first_df[
                                'Harris Church of England Academy, Rugby'],
                                errors='ignore')

        self.data_loader.second_df[
                            'Cardinal Newman Catholic Secondary School '] = \
                                pd.to_numeric(self.data_loader.second_df[
                                'Cardinal Newman Catholic Secondary School '],
                                errors='ignore')

        # Convert 'Time' columns to strings
        self.data_loader.first_df['Time'] \
                                    = self.data_loader.first_df['Time']\
                                        .astype(str)
        self.data_loader.second_df['Time.1'] \
                                    = self.data_loader.second_df['Time.1']\
                                        .astype(str)

        # Set 'Time' columns as the index
        self.data_loader.first_df.set_index('Time', inplace=True)
        self.data_loader.second_df.set_index('Time.1', inplace=True)

    # Mean function
    def calculate_means(self):
        """Calculate the mean air quality index.

        Returns:
            Mean air quality index of two locations.
            >>> hcmean = round(self.data_loader.
                       first_df['Harris Church of England Academy, Rugby']
                       .mean(), 2)
                786.37
            >>> cnmean = round(self.data_loader.
                       second_df['Cardinal Newman Catholic Secondary School ']
                       .mean(), 2)
                1411.98
            >>> hcmean = round(self.data_loader.
                       first_df['Spelling error in the column name ']
                       .mean(), 2)
            An error occurred: cannot access local variable 'hcmean'
            where it is not associated with a value
            >>> cnmean = round(self.data_loader.
                       second_df['Spelling error in the column name ']
                       .mean(), 2)
            An error occurred: cannot access local variable 'cnmean'
            where it is not associated with a value
        """
        try:
            hcmean = round(self.data_loader.
                       first_df['Harris Church of England Academy, Rugby']
                       .mean(), 2)
            cnmean = round(self.data_loader.
                       second_df['Cardinal Newman Catholic Secondary School ']
                       .mean(), 2)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        return hcmean, cnmean

    # Standard deviation function
    def calculate_std(self):
        """Calculate the standard deviation of the air quality index.

        Returns:
            Tuple: Standard deviation of the air quality index
            of two locations.

            >>> hcstd = self.data_loader.first_df[
                    'Harris Church of England Academy, Rugby'].\
                        rolling(window=3, min_periods=3).std().round(2)
            0       NaN
            1       NaN
            2       NaN
            3      0.00
            4      0.00
            5      0.00
            >>> cnstd = self.data_loader.second_df[
                    'Cardinal Newman Catholic Secondary School '].\
                        rolling(window=3, min_periods=3).std().round(2)
             0       NaN
             1       NaN
             2       NaN
             3      0.00
             4      0.00
             5      0.00
            >>> hcstd = self.data_loader.first_df[
                    'Spelling error in the column name '].\
                        rolling(window=3, min_periods=3).std().round(2)
            An error occurred: cannot access local variable 'hcstd'
            where it is not associated with a value
            >>> cnstd = self.data_loader.second_df[
                    'Spelling error in the column name '].\
                        rolling(window=3, min_periods=3).std().round(2)
            An error occurred: cannot access local variable 'cnstd'
            where it is not associated with a value
            >>> hcmax_std = hcstd.max(skipna=True)
            hcmax_std = 64.09
            >>> cnmax_std = cnstd.max(skipna=True)
            cnmax_std = 360.53
            >>> hcmaxwindow = hcstd.idxmax(skipna=True)
            hcmaxwindow = 10:15:25
            >>> cnmaxwindow = cnstd.idxmax(skipna=True)
            cnmaxwindow = 09:31:00
        """
        try:
            hcstd = self.data_loader.first_df[
                    'Harris Church of England Academy, Rugby'].\
                        rolling(window=3, min_periods=3).std().round(2)
            cnstd = self.data_loader.second_df[
                    'Cardinal Newman Catholic Secondary School '].\
                        rolling(window=3, min_periods=3).std().round(2)

            hcmax_std = hcstd.max(skipna=True)
            cnmax_std = cnstd.max(skipna=True)
            hcmaxwindow = hcstd.idxmax(skipna=True)
            cnmaxwindow = cnstd.idxmax(skipna=True)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        return hcmax_std, cnmax_std, hcmaxwindow, cnmaxwindow


class AppGUI(tk.Tk):
    def __init__(self, data_loader):
        super().__init__()
        self.title("Data Analyser")
        self.attributes('-fullscreen', True)

        self.data_loader = data_loader
        self.analyser = DataAnalyser(self.data_loader)
        self.analyser.format_data()

        self.create_widgets()

    def tab_popup(func):
        def wrapper(self, *args, **kwargs):
            tab_name = func.__name__.replace('_', ' ').title()
            messagebox.showinfo("Tab", "Welcome to my Data Analyser")
            return func(self, *args, **kwargs)
        return wrapper

    @tab_popup

    def create_widgets(self):
        # Main window
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        self.attributes('-fullscreen', True)

        # Created notebook
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Created tabs
        mean_tab = ttk.Frame(notebook)
        std_tab = ttk.Frame(notebook)
        plot_tab = ttk.Frame(notebook)

        # Added tabs to the notebook
        notebook.add(mean_tab, text="Mean")
        notebook.add(std_tab, text="Standard Deviation")
        notebook.add(plot_tab, text="Plot")

        # Mean C02 tab
        ttk.Label(mean_tab,
                  text="Mean CO2 Level",
                  wraplength=300,
                  font=("Helvetica", 30, "bold")).pack()

        hcmean, cnmean = self.analyser.calculate_means()
        mean_diff = round(-1*(hcmean - cnmean), 2)

        ttk.Label(mean_tab,
                  text="Harris Church of England Academy, Rugby: " +
                  f"{hcmean}",
                  font=("Helvetica", 14),
                  wraplength=400).pack()
        ttk.Label(mean_tab,
                  text="Cardinal Newman Catholic Secondary School: " +
                  f"{cnmean}",
                  font=("Helvetica", 14),
                  wraplength=400).pack()
        ttk.Label(mean_tab,
                  text="The mean difference for the two locations: " +
                  str(mean_diff),
                  font=("Helvetica", 14),
                  wraplength=400).pack()

        # Standard Deviation tab
        ttk.Label(std_tab,
                  text="Highest standard deviation from a 3-point window",
                  wraplength=1000,
                  font=("Helvetica", 25, "bold")
                  ).pack()

        std_results = self.analyser.calculate_std()

        hcmaxstd, cnmaxstd, hcmaxstd_window, cnmaxstd_window = std_results
        std_frame = ttk.Frame(std_tab)
        std_frame.pack()

        ttk.Label(std_frame,
                  text="Harris Church of England Academy, Rugby: " +
                  f"{hcmaxstd} Highest standard deviation window at: " +
                  f"{hcmaxstd_window}",
                  font=("Helvetica", 14),
                  wraplength=320).pack(side=tk.LEFT)

        ttk.Label(std_frame,
                  text="Cardinal Newman Catholic Secondary School: " +
                  f"{cnmaxstd} Highest stdandard deviation window at: " +
                  f"{cnmaxstd_window}",
                  font=("Helvetica", 14),
                  wraplength=350).pack(side=tk.RIGHT)

        # Data for bell curve
        std_hc = np.linspace(hcmean - 3 * hcmaxstd, hcmean + 3 * hcmaxstd, 100)
        frq_hc = np.exp(-(std_hc - hcmean)**2 /
                      (2 * hcmaxstd**2)) / (np.sqrt(2 * np.pi) * hcmaxstd)

        std_cn = np.linspace(cnmean - 3 * cnmaxstd, cnmean + 3 * cnmaxstd, 100)
        frq_cn = np.exp(-(std_cn - cnmean)**2 /
                      (2 * cnmaxstd**2)) / (np.sqrt(2 * np.pi) * cnmaxstd)

        # Figure and axis for the bell curve
        fig2, stdax = plt.subplots(figsize=(6, 4))
        stdax.plot(std_hc, frq_hc, label=
                   'Harris Church of England Academy, Rugby', color='blue')
        stdax.plot(std_cn, frq_cn, label=
                   'Cardinal Newman Catholic Secondary School', color='orange')
        stdax.set_xlabel('CO2 Level')
        stdax.set_ylabel('Frequency')
        stdax.set_title('Standard Distrbution of CO2 Levels')
        stdax.legend()

        # Embed the Bell Curve figure in the Tkinter window
        canvas2 = FigureCanvasTkAgg(fig2, master=std_tab)
        canvas_widget2 = canvas2.get_tk_widget()
        canvas_widget2.pack(fill=tk.BOTH, expand=True)

        # Line plot tab
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5))

        ax1.plot(self.data_loader.first_df.index,
             self.data_loader.first_df[
                 'Harris Church of England Academy, Rugby'],
             color='blue',
             label='Harris Church of England Academy, Rugby')
        ax1.set_xlabel('Time')
        ax1.set_xticks(ax1.get_xticks()[::60])
        ax1.set_ylabel('CO2 Level')
        ax1.legend()

        ax2.plot(self.data_loader.second_df.index,
                 self.data_loader.second_df[
                     'Cardinal Newman Catholic Secondary School '],
                 color='orange',
                 label='Cardinal Newman Catholic Secondary School')
        ax2.set_xlabel('Time')
        ax2.set_xticks(ax2.get_xticks()[::60])
        ax2.set_ylabel('CO2 Level')
        ax2.legend()

        plt.tight_layout()

        # Embed the Line plot figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_tab)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Configure grid weights for resizing
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Terminate window button
        ttk.Button(main_frame, text="Exit", command=self.destroy).pack(side=tk.BOTTOM)
    


def main():
    """Main function."""
    try:
        file_path = input("Please enter the file path of your data: ")
        data_loader = DataLoader()
        data_loader.first_df, data_loader.second_df \
            = data_loader.load_data(file_path)

        # GUI
        app_gui = AppGUI(data_loader)
        app_gui.mainloop()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
