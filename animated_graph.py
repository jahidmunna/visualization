import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class AnimatedHorizontalBarChart:

    def __init__(self, data_file):
        # Load data
        self.df = pd.read_csv(data_file)
        self.df = self.df.rename(columns={'Country Name': 'Country'})

        # Define colors
        self.colors = plt.colormaps['tab20'].colors
        # Fixed colors for countries
        self.df['colors'] = self.colors[:len(self.df['Country'])]

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

    def sort_df(self, year):
        return self.df[['Country', year, 'colors']].sort_values(by=[year])

    def animate(self, year):
        sorted_df = self.sort_df(year)
        self.ax.clear()
        bars = self.ax.barh(
            sorted_df['Country'],
            sorted_df[year] / 1e9,
            color=sorted_df['colors']
        )
        self.ax.set_xlabel(
            'GDP (in billions)',
            fontsize=14
        )
        self.ax.set_ylabel(
            'Country',
            fontsize=14
        )
        self.ax.set_title(
            f'GDP Per Year (Year: {year})',
            fontsize=18,
            fontweight='bold'
        )

        # Set y-axis tick labels to show full country names
        self.ax.set_yticks(range(len(sorted_df)))
        self.ax.set_yticklabels(sorted_df['Country'], fontsize=10)

        # Add value labels to the right of each bar
        for i, bar in enumerate(bars):
            value = sorted_df[year].iloc[i] / 1e9  # Divide by 1 billion
            # Add "$B" suffix
            self.ax.text(bar.get_width(), i,
                         f'{value:.2f} $B', va='center', fontsize=10)

    def animate_chart(self, save=False):
        # Animate only based on year. Coutry and color columns are used for all. So ignore in the loop below
        animation = FuncAnimation(
            self.fig, self.animate, frames=self.df.columns[1:-1].values, interval=500)

        if save:
            animation.save('chart.gif', writer='imagemagick')
        else:
            plt.show()


if __name__ == '__main__':
    # Create an instance of the chart and animate it
    chart = AnimatedHorizontalBarChart('gdp_sample.csv')
    chart.animate_chart(save=False)
