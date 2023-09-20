import seaborn as sns
import matplotlib.pyplot as plt
from db_utils import loans_df 
from data_transforms import converted_loans_df

class Plotter:

    def __init__(self, table):
        self.table = table
    
    def view_histogram(self, col):
        sns.displot(data=self.table, x=col, kde="True")
        plt.show()

    def view_boxplot(self, col):
        sns.boxplot(data=self.table, x=col)
        plt.show()
    
    def view_correlation(self, col1, col2):
        sns.pairplot(self.table[[col1, col2]])
        plt.show()
    
    def facet(self, col):
        g = sns.FacetGrid(self.table)
        g.map(sns.histplot, col)
        plt.show()

    def scatterplot(self, col1, col2):
        sns.scatterplot(data=self.table, x=col1, y=col2)
        plt.show()

    def scatterplot_of_means(self, col1, col2):
        means = self.table.groupby(col1, observed=True)[col2].mean()
        sns.scatterplot(data=means, x=means.index, y=means)
        plt.show()

    def regplot(self, col1, col2):
        means = self.table.groupby(col1, observed=True)[col2].mean()
        sns.regplot(x=means.index, y=means)
        plt.show()

loans_plotter = Plotter(converted_loans_df)
# loans_plotter.view_histogram("employment_length")
# loans_plotter.view_boxplot("funded_amount")
# loans_plotter.view_correlation("last_payment_date", "loan_amount")
# loans_plotter.facet("last_payment_date")
# original_loans_plotter = Plotter(loans_df)
loans_plotter.regplot("last_payment_date", "loan_amount")

    
