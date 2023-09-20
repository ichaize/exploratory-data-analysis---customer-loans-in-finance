import pandas as pd
from db_utils import loans_df
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np


loans_df.drop("Unnamed: 0", axis=1, inplace=True)

to_float = ["loan_amount"]
to_cat = ["grade", "home_ownership", "verification_status", "loan_status", "purpose", "term", "employment_length"]
to_bool = ["payment_plan"]
to_int = ["mths_since_last_delinq", "mths_since_last_record", "collections_12_mths_ex_med", "mths_since_last_major_derog"]


col_conversion_dict = {
        "bool": to_bool,
        "cat": to_cat,
        "float": to_float,
        "int": to_int
    }

class DataTransformer:

    def convert_to_bool(self, table, col):
        table[col] = table[col].astype("bool")
        return table
    
    def convert_to_category(self, table, col):
        table[col] = table[col].astype("category")
        return table
    
    def convert_to_float(self, table, col):
        table[col] = table[col].astype("float64")
        return table
    
    def convert_to_int(self, table, col):
        table[col] = table[col].astype("Int64")
        return table
    
    def convert_dtypes(self, table, conversion_dict):
        for col in conversion_dict["bool"]:
            self.convert_to_bool(table, col)
        for col in conversion_dict["cat"]:
            self.convert_to_category(table, col)
        for col in conversion_dict["float"]:
            self.convert_to_float(table, col)
        for col in conversion_dict["int"]:
            self.convert_to_int(table, col)
        return table
    
    def convert_dates(self, date):
        month_nums = {
             "Jan": "01", 
             "Feb": "02",
             "Mar": "03",
             "Apr": "04",
             "May": "05",
             "Jun": "06",
             "Jul": "07",
             "Aug": "08",
             "Sep": "09",
             "Oct": "10",
             "Nov": "11",
             "Dec": "12"
             }
        for month in month_nums:
            if date[0:3] == month:
                date = date[5:] + month_nums[month]
        return date
    
    def clean_dates(self, table):
        no_nulls = table.dropna(subset="last_payment_date")
        no_nulls["last_payment_date"] = no_nulls["last_payment_date"].astype("str")
        no_nulls["last_payment_date"] = no_nulls["last_payment_date"].str.replace("-", "")
        no_nulls["last_payment_date"] = no_nulls["last_payment_date"].apply(lambda x: self.convert_dates(x))
        table.update(no_nulls)
        table["last_payment_date"] = table["last_payment_date"].astype("float64")
        return table     

    def impute_values(self, table, col1, col2):
        '''col1 is the target variable (the one with missing values) 
        and col2 is the independent variable (the one being used as reference)'''
        training_set = table.dropna(subset=col1)
        nulls = table[table[col1].isnull()]
        nulls.reset_index(drop=True, inplace=True)
        X = np.array(training_set[col2]).reshape(-1, 1)
        y = np.array(training_set[col1])
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=1, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        x_null = nulls[col2].values.reshape(-1, 1)
        for row in nulls.index:
            predictor = x_null[row].reshape(-1, 1)
            y_pred = model.predict(predictor)
            print(y_pred)
        # y_null = y_null.reshape(-1, 1)
        # print(y_null.dtype)
        # for row in nulls.index:
        #     y_pred = model.predict(y_null)
        #     print(y_pred)
        # plt.scatter(X_test, y_test, color ='b')
        # plt.plot(X_test, y_pred, color ='k')
        # plt.show()

    def replace_funded_amount_nulls(self, table):
        table["funded_amount"] = table["funded_amount"].fillna(table["loan_amount"])
        return table
    
    def clean_term(self, table):
        table.loc[(table["loan_amount"] > 14855.5) & (table["term"].isnull()), ["term"]] = "60 months"
        table.loc[(table["loan_amount"] <= 14855.5) & (table["term"].isnull()), ["term"]] = "36 months"
        return table
    
    def clean_int_rate(self, table):
        avg_int_rate_by_grade = table.groupby("grade", observed=True)["int_rate"].mean()
        for grade in avg_int_rate_by_grade.index:
            table.loc[(table["grade"] == grade) & (table["int_rate"].isnull()), ["int_rate"]] = avg_int_rate_by_grade[grade]
        return table
    
    def clean_employment_length(self, table):
        table["employment_length"] = pd.Categorical(table["employment_length"], categories=["< 1 year", "1 year", "2 years", "3 years", "4 years", "5 years", "6 years", "7 years", "8 years", "9 years", "10+ years"], ordered=True)
        # table["employment_codes"] = table["employment_length"].cat.codes
        # table["employment_codes"] = table["employment_codes"].astype("int64")
        # employment = table[["employment_length", "employment_codes"]]
        # print(employment.head(30))
        table["employment_length"].fillna("10+ years", inplace=True)
        return table

transformer = DataTransformer()
converted_loans_df = transformer.convert_dtypes(loans_df, col_conversion_dict)
converted_loans_df = transformer.replace_funded_amount_nulls(converted_loans_df)
converted_loans_df = transformer.clean_term(converted_loans_df)
converted_loans_df = transformer.clean_int_rate(converted_loans_df)
converted_loans_df = transformer.clean_employment_length(converted_loans_df)
converted_loans_df = transformer.clean_dates(converted_loans_df)
transformer.impute_values(converted_loans_df, "last_payment_date", "loan_amount")


# def convert_to_bool(self, cols):
#         for col in cols:
#             self.table[col] = self.table[col].astype("bool")
#         return self.table
    
#     def convert_to_category(self, cols):
#         for col in cols:
#             self.table[col] = self.table[col].astype("category")
#         return self.table
    
#     def convert_to_float(self, cols):
#         for col in cols:
#             self.table[col] = self.table[col].astype("float64")
#         return self.table
    
#     def convert_to_int(self, cols):
#         for col in cols:
#             self.table[col] = self.table[col].astype("int64")
#         return self.table

