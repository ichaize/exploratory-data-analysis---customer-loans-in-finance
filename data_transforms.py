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
        table[col] = table[col].astype("int64")
        return table
    

to_float = ["loan_amount"]
to_category = ["grade", "home_ownership", "verification_status", "loan_status", "purpose"]
to_bool = ["payment_plan"]
to_int = ["mths_since_last_delinq", "mths_since_last_record", "collections_12_mths_ex_med", "mths_since_last_major_derog"]
# also consider converting term to int after removing "months" and converting col name to "term_in_months"