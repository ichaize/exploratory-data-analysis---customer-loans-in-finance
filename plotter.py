import seaborn as sns
import matplotlib.pyplot as plt
# from db_utils import loans_df 
from data_transforms import converted_loans_df
from dataframe_info import skewed_columns


class Plotter:

    def view_histogram(self, table, col):
        sns.displot(data=table, x=col, kde="True")
        plt.show()

    def view_boxplot(self, table, col):
        sns.boxplot(data=table, x=col)
        plt.show()
    
    def view_correlation(self, table, col1, col2):
        sns.pairplot(table[[col1, col2]])
        plt.show()
    
    def facet(self, table, col):
        g = sns.FacetGrid(table)
        g.map(sns.histplot, col)
        plt.show()
    
    def multiple_histograms(self, table):
        for i, col in enumerate(table.columns, 1):
            plt.subplot(3, 9, i)
            sns.histplot(table[col])
        plt.show()

    def scatterplot(self, table, col1, col2):
        sns.scatterplot(data=table, x=col1, y=col2)
        plt.show()

    def scatterplot_of_means(self, table, col1, col2):
        means = table.groupby(col1, observed=True)[col2].mean()
        sns.scatterplot(data=means, x=means.index, y=means)
        plt.show()

    def regplot(self, table, col1, col2):
        means = table.groupby(col1, observed=True)[col2].mean()
        sns.regplot(x=means.index, y=means)
        plt.show()

    def heatmap(self, table):
        table = table.dropna()
        numerical = table.select_dtypes(include=["number"])
        corr = numerical.corr()
        plt.subplots(figsize=(20,15))
        sns.heatmap(corr, annot=True, linewidths=.5)
        plt.show()

loans_plotter = Plotter()
# loans_plotter.view_histogram(converted_loans_df, "employment_length")
# loans_plotter.view_boxplot(converted_loans_df, "funded_amount")
# loans_plotter.view_correlation(converted_loans_df, "last_payment_date", "loan_amount")
# loans_plotter.facet(converted_loans_df, "last_payment_date")
# loans_plotter.regplot(converted_loans_df, "last_payment_date", "issue_date")
# loans_plotter.heatmap(converted_loans_df)
loans_plotter.multiple_histograms(skewed_columns)

    
