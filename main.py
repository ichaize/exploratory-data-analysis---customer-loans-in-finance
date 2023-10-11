from db_utils import loans_df
from data_transforms import DataTransformer
from dataframe_info import DataFrameInfo
from plotter import Plotter
import pandas as pd
transformer = DataTransformer()
plotter = Plotter()
info_getter = DataFrameInfo()

loans_df.drop("Unnamed: 0", axis=1, inplace=True)

to_float = ["loan_amount"]
to_cat = ["grade", "home_ownership", "verification_status", "loan_status", "purpose", "sub_grade"]
to_bool = ["payment_plan"]
to_int = ["collections_12_mths_ex_med"]
to_drop = ["mths_since_last_major_derog", "next_payment_date", "mths_since_last_record", "mths_since_last_delinq", "application_type", "policy_code"] # application type and policy code both only have one value so are a bit poiintless
dates_to_clean = ["last_payment_date", "issue_date", "earliest_credit_line", "last_credit_pull_date"]
cat_cols = ["grade_cats", "home_ownership_cats", "verification_status_cats", "loan_status_cats", "purpose_cats", "sub_grade_cats"]
nulls_to_drop = ["last_payment_date", "last_credit_pull_date", "collections_12_mths_ex_med"]

col_conversion_dict = {
        "bool": to_bool,
        "cat": to_cat,
        "float": to_float,
        "int": to_int
}

cleaned_loans_df = transformer.prepare_data(loans_df, col_conversion_dict, to_drop, nulls_to_drop, dates_to_clean)
skewed_columns = info_getter.identify_skewness(cleaned_loans_df)
# sqrt_df = transformer.sqrt_transform(skewed_columns)
# log_df = transformer.log_transform(skewed_columns)
box_coxed = transformer.box_cox(skewed_columns)
cleaned_loans_df.update(box_coxed)
print(cleaned_loans_df.head(20))
# info_getter.identify_skewness(sqrt_df)

# plotter.multiple_histograms(sqrt_df)

# zeroes = (skewed_columns > 0).sum().sum()



