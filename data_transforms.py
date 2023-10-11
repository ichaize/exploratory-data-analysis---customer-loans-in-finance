import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from scipy import stats

to_cat = ["grade", "home_ownership", "verification_status", "loan_status", "purpose", "sub_grade"]
cat_cols = ["grade_cats", "home_ownership_cats", "verification_status_cats", "loan_status_cats", "purpose_cats", "sub_grade_cats"]

class DataTransformer:
    
    def prepare_data(self, table, conversion_dict, cols_to_drop, nulls_to_drop, dates_to_clean):
        self.convert_dtypes(table, conversion_dict)
        self.drop_columns(table, cols_to_drop)
        self.drop_nulls(table, nulls_to_drop)
        self.clean_dates(table, dates_to_clean)
        self.clean_funded_amount(table)
        self.clean_term(table)
        self.clean_int_rate(table)
        self.clean_employment_length(table)
        self.prep_for_corr(table)
        return table

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
    
    def drop_columns(self, table, cols_to_drop):
        table.drop(labels=cols_to_drop, axis=1, inplace=True)
        return table
    
    def drop_nulls(self, table, cols_to_drop):
        for col in cols_to_drop:
            table.dropna(subset=[col], inplace=True)
        return table
    
    def convert_dates_to_epoch(self, date):
        month_nums = {
             "Jan": "1", 
             "Feb": "2",
             "Mar": "3",
             "Apr": "4",
             "May": "5",
             "Jun": "6",
             "Jul": "7",
             "Aug": "8",
             "Sep": "9",
             "Oct": "10",
             "Nov": "11",
             "Dec": "12"
             }
        for month in month_nums:
            if date[0:3] == month:
                ts = pd.Timestamp(year=int(date[4:]), month=int(month_nums[month]), day=1)
                epoch_time = ts.timestamp()
        return epoch_time
    
    def clean_dates(self, table, cols):
        for col in cols:
            no_nulls = table.dropna(subset=col)
            no_nulls[col] = no_nulls[col].astype("str")
            no_nulls[col] = no_nulls[col].apply(lambda x: self.convert_dates_to_epoch(x))
            table.update(no_nulls)
            table[col] = table[col].astype("float64")
        return table     

    def clean_funded_amount(self, table):
        table["funded_amount"] = table["funded_amount"].fillna(table["loan_amount"])
        return table
    
    def clean_term(self, table):
        table.loc[(table["loan_amount"] > 14855.5) & (table["term"].isnull()), ["term"]] = "60 months"
        table.loc[(table["loan_amount"] <= 14855.5) & (table["term"].isnull()), ["term"]] = "36 months"
        table["term"] = table["term"].astype(str)
        table["term"] = table["term"].str.replace(" months", "")
        table["term"] = table["term"].astype(int)
        return table
    
    def clean_int_rate(self, table):
        avg_int_rate_by_grade = table.groupby("grade", observed=True)["int_rate"].mean()
        for grade in avg_int_rate_by_grade.index:
            table.loc[(table["grade"] == grade) & (table["int_rate"].isnull()), ["int_rate"]] = avg_int_rate_by_grade[grade]
        return table
    
    def clean_employment_length(self, table):
        table["employment_length"].fillna("10+ years", inplace=True)
        table["employment_length"] = pd.Categorical(table["employment_length"], categories=["< 1 year", "1 year", "2 years", "3 years", "4 years", "5 years", "6 years", "7 years", "8 years", "9 years", "10+ years"], ordered=True)
        table["employment_length_cats"] = table["employment_length"].cat.codes
        table["employment_length_cats"] = table["employment_length_cats"].astype("int64")
        return table

    def label_encoding(self, table, cols):
        label_encoder = LabelEncoder()
        for col in cols:
            table[f"{col}_cats"] = label_encoder.fit_transform(table[col])
        return table
    
    def prep_for_corr(self, table):
        table = self.label_encoding(table, to_cat)
        table = self.convert_to_float(table, cat_cols)
        return table
    
    def sqrt_transform(self, table):
        sqrt_df = table.transform(np.sqrt)
        return sqrt_df

    def log_transform(self, table):
        for col in table.columns:
            table[col] = table[col].apply(lambda x: np.log(x) if x > 0 else 0)
        return table
    
    def box_cox(self, table):
        table += 0.01
        table = table.astype("float64")
        for col in table.columns:
            transformed, _ = stats.boxcox(table[col])
            table[col] = transformed
        return table
            


   


# transformer = DataTransformer()
# converted_loans_df = transformer.convert_dtypes(original_loans_df, col_conversion_dict)
# converted_loans_df = transformer.drop_columns(converted_loans_df, to_drop)
# converted_loans_df = transformer.clean_funded_amount(converted_loans_df)
# converted_loans_df = transformer.clean_term(converted_loans_df)
# converted_loans_df = transformer.clean_int_rate(converted_loans_df)
# converted_loans_df = transformer.clean_employment_length(converted_loans_df)
# converted_loans_df = transformer.drop_nulls(converted_loans_df, nulls_to_drop)
# converted_loans_df = transformer.clean_dates(converted_loans_df, dates_to_clean)
# converted_loans_df = transformer.prep_for_corr(converted_loans_df)
# sqrt_transformation = transformer.sqrt_transform(skewed_columns)
# print(sqrt_transformation.head(20))



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

# def impute_values(self, table, col1, col2):
#         '''col1 is the target variable (the one with missing values) 
#         and col2 is the independent variable (the one being used as reference)'''
#         training_set = table.dropna(subset=col1)
#         nulls = table[table[col1].isnull()]
#         nulls.reset_index(drop=True, inplace=True)
#         X = np.array(training_set[col2]).reshape(-1, 1)
#         y = np.array(training_set[col1])
#         X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=1, random_state=42)
#         model = LinearRegression()
#         model.fit(X_train, y_train)
#         x_null = nulls[col2].values.reshape(-1, 1)
#         for row in nulls.index:
#             predictor = x_null[row].reshape(-1, 1)
#             y_pred = model.predict(predictor)
#             print(y_pred)
#         # y_null = y_null.reshape(-1, 1)
#         # print(y_null.dtype)
#         # for row in nulls.index:
#         #     y_pred = model.predict(y_null)
#         #     print(y_pred)
#         # plt.scatter(X_test, y_test, color ='b')
#         # plt.plot(X_test, y_pred, color ='k')
#         # plt.show()