import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import FixedLocator


class AnimatedHorizontalBarChart:
    
    def __init__(self, data_file):
        # Load data
        self.df = pd.read_csv(data_file)
        self.df = self.df.rename(columns={'Country Name': 'Country'})
        
        # Create figure and axis
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.set_xlabel('GDP (in billions)', fontsize=14)
        self.ax.set_ylabel('Country', fontsize=14)
        self.ax.set_title('GDP Per Year', fontsize=18, fontweight='bold')
        
        # Set x-axis tick labels to show full values
        self.ax.xaxis.set_major_formatter('{:.1f}'.format)
        
        # Add a small border to the chart
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['left'].set_linewidth(0.5)
        self.ax.spines['bottom'].set_linewidth(0.5)
        
        # Define colors
        self.colors = plt.cm.get_cmap('tab20').colors
        
    def sort_df(self, year):
        return self.df[['Country', year]].sort_values(year)
    
    def animate(self, year):
        sorted_df = self.sort_df(year)
        self.ax.clear()
        bars = self.ax.barh(sorted_df['Country'], sorted_df[year] / 1e9, color=self.colors)
        self.ax.set_xlabel('GDP (in billions)', fontsize=14)
        self.ax.set_ylabel('Country', fontsize=14)
        self.ax.set_title('GDP Per Year (Year: {})'.format(year), fontsize=18, fontweight='bold')
        
        # Set y-axis tick labels to show full country names
        self.ax.set_yticks(range(len(sorted_df)))
        self.ax.set_yticklabels(sorted_df['Country'], fontsize=10)
        
        # Add value labels to the right of each bar
        for i, bar in enumerate(bars):
            value = sorted_df[year].iloc[i] / 1e9  # Divide by 1 billion
            self.ax.text(bar.get_width(), i, f'{value:.2f}$B', va='center', fontsize=10)  # Add "$B" suffix
    
    def animate_chart(self, save=False):
        animation = FuncAnimation(self.fig, self.animate, frames=self.df.columns[1:].values, interval=1000)
        
        if save:
            animation.save('chart.gif', writer='imagemagick')
        else:
            plt.show()

if __name__ == '__main__':
    # Create an instance of the chart and animate it
    chart = AnimatedHorizontalBarChart('gdf_sample.csv')
    chart.animate_chart(save=True)
