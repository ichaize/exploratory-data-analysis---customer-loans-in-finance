from data_transforms import converted_loans_df
# from db_utils import original_loans_df
import pandas as pd
import numpy as np
from scipy import stats

loans_df = converted_loans_df

class DataFrameInfo:

    def check_dtypes(self, table):
        print(table.dtypes)

    def get_df_stats(self, table):
        numeric_cols = table.select_dtypes(include=["int64", "float64"])
        categorical_cols = table.select_dtypes(include=["category", "object"])
        for col in numeric_cols:
            print(f"The number of unique values in {col} is {table[col].unique().size}")
            print(f"The mean of {col} is {table[col].describe().iloc[1]}")
            print(f"The median of {col} is {table[col].describe().iloc[5]}")
            print(f"The standard deviation of {col} is {table[col].describe().iloc[2]}")
        for col in categorical_cols:
            print(f"The number of unique values in {col} is {table[col].describe().iloc[1]}")
            print(f"The most frequent value in {col} is {table[col].describe().iloc[2]}")

    def get_col_stats(self, table, col):
        numeric_cols = table.select_dtypes(include=["int64", "float64"])
        if col in numeric_cols:
            print(f"The number of unique values in {col} is {table[col].unique().size}")
            print(f"The mean of {col} is {table[col].describe().iloc[1]}")
            print(f"The median of {col} is {table[col].describe().iloc[5]}")
            print(f"The standard deviation of {col} is {table[col].describe().iloc[2]}")
        else:
            print(f"The number of unique values in {col} is {table[col].describe().iloc[1]}")
            print(f"The most frequent value in {col} is {table[col].describe().iloc[2]}")
    
    def get_shape(self, table):
        print(table.shape)

    def count_nulls(self, table):
        for col in table.columns:
            num_nulls = table[col].isna().sum()
            percent_nulls = 100 * num_nulls / (len(table.index))
            if percent_nulls == 0:
                print(f"There are no nulls in {col}")
            else:
                print(f"There are {num_nulls} null values in {col}")
                print(f"The percentage of null values in {col} is {percent_nulls}")
    
    def unique_values(self, table, col):
        print(table[col].unique())

    def get_categories(self, table, col):
        print(table[col].cat.categories)

    

            

    


info_getter = DataFrameInfo()
# info_getter.check_dtypes(loans_df)
# info_getter.get_df_stats(loans_df)
# info_getter.get_shape(loans_df)
# info_getter.count_nulls(loans_df)
# info_getter.get_col_stats(loans_df, "last_payment_date")
# info_getter.unique_values(loans_df, "last_payment_date")
# info_getter.pearson_series_correlation(loans_df, "last_payment_date", "loan_amount")
# info_getter.get_categories(loans_df, "employment_length")
# info_getter.pearson_df_correlation(loans_df)
# info_getter.test_missing_at_random(loans_df, "last_payment_date", "loan_amount")




    # def anova(self, table, cat_col, num_col):
    #     table.dropna(subset=[cat_col, num_col], inplace=True)
    #     category_group_list=table.groupby(cat_col, observed=True)[num_col].apply(list)
    #     anova_result = stats.f_oneway(*category_group_list)
    #     print(anova_result)
    #     if anova_result[1] > 0.05:
    #         print(f"There is no correlation between {cat_col} and {num_col}")
    #     else: 
    #         print(f"There is correlation between {cat_col} and {num_col}: the p-value is {anova_result[1]}")

    # def pearson_series_correlation(self, table, col1, col2):
    #     print(table[col1].corr(table[col2]))

    # def pearson_df_correlation(self, table):
    #     table = table.astype("category")
    #     print(table.corr())
        # numeric_cols = table.select_dtypes(include=["int64", "float64"])
        # for col in table.columns:
        #     print(table[col].corr(table[col1]))

   

    # def test_missing_at_random(self, table, col1, col2):
    #     nulls = table[table[col1].isnull()]
    #     non_nulls = table[~table[col1].isnull()]
    #     print(nulls[col2].mean())
    #     print(non_nulls[col2].mean())
    #     t_test_result = ttest_ind(nulls[col2], non_nulls[col2], nan_policy="omit")
    #     if t_test_result[1] < 0.05:
    #         print(f"The p-value is {t_test_result[1]}: the missing data is unlikely to be missing at random")
    #     else: 
    #         print(f"The p-value is {t_test_result[1]}: the missing data is probably missing at random")