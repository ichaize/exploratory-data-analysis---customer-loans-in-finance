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
correlated_to_drop = ["funded_amount", "funded_amount_inv", "instalment", "grade_cats", "sub_grade_cats", "total_payment_inv", "total_rec_prncp"]

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
transformed = transformer.log_transform(box_coxed, "collections_12_mths_ex_med")
cleaned_loans_df.update(transformed)
cleaned_loans_df = transformer.drop_columns(cleaned_loans_df, correlated_to_drop)

plotter.heatmap(cleaned_loans_df)
# smallest = cleaned_loans_df.nsmallest(10, "total_rec_late_fee")
# print(smallest["total_rec_late_fee"])
# cleaned_loans_df = transformer.remove_min_value(cleaned_loans_df, min_value_outliers)
# plotter.view_boxplot(cleaned_loans_df, "loan_amount")

# small_loans = cleaned_loans_df[cleaned_loans_df["loan_amount"] < 24]


# zeroes = (skewed_columns > 0).sum().sum()



