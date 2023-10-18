# Exploratory Data Analysis Project - Finance

This project simulates performing exploratory data analysis on a database of customer loan data for a finance company. 

Technologies used: Python, pandas, PostreSQL, sqlalchemy

## Usage Instructions

## Project Components / File Structure

### Dealing with null values

There are a few columns with a high number of null values: around 60% for mths_since_last_delinq and next_payment_date, and between 85 and 90% for mths_since_last_record and mths_since_last_major_derog. For these columns the number of missing values is so high that it would be too risky to impute the values so they are dropped.

Columns with a small number of nulls were investigated on an individual basis to determine the most appropriate action.

The funded_amount column has 3007 null values, or 5.5%. Using the Plotter class to view the distribution shows the data is skewed to the right, suggesting the median might be most appropriate. The median of funded_amount is 12,000. However on closer inspection it was decided not to impute using the median because of the extremely close correlation between funded_amount and loan_amount as seen using sns.pairplot. A SQL query revealed they are only different in 941 cases (0.17%). Also, the funded amount is always less than or equal to the loan amount, so using 12,000 would be incorrect where loan_amount < 12,000. The null values in funded_amount were therefore filled using the corresponding value from loan_amount.

The term column has 4772 null values, or 8.8%. Term is a categorical variable with two values: 60 months and 36 months. It would make sense for term length to be influenced by e.g. loan amount. Using SQL to check the average loan amount for each term length (SELECT term, AVG(loan_amount) FROM loans GROUP BY term) shows that the average loan amount for 60-month terms is 18233.5, while for 36-month terms it is 11477.5. The null values in term were therefore replacved with 60 months if loan_amount > 14855.5 and 36 months otherwise.

The int_rate column has 5169 null values, or 9.5%. Again, it would make sense for the interest rate to be correlated with other factors such as loan status or grade. Running the SQL query (SELECT AVG(int_rate) AS avg_int_rate, grade FROM loans GROUP BY grade ORDER BY avg_int_rate ASC) shows clearly that the interest rate increases as the grade gets worse: an average of 7.5% for A grade loans, 11.4% for B grade loans, 14.6% for C grade loans, 17.4% for D grade loans, 19.9% for E grade loans, 22.4% for F grade loans, and 23% for G grade loans. This can also be seen clearly on a scatterplot. These averages were used to fill the null values in the int_rate column based on the corresponding grade.

The employment_length column has 2188 null values, or 3.9%. The seaborn heatmap shows it is not strongly correlated with any other columns and the distribution plot shows that it is not normally distributed: there are many more customers with 10+ years employment length than any other length. As a result the mode (10+ years) was used to impute the missing values.

The last_payment_date column has just 73 null values, or 0.13%. The seaborn heatmap shows that it is highly correlated with issue_date (0.83). However, viewing a scatterplot of the two columns shows that although last_payment_date is never before issue_date, there is no other obvious pattern. A SQL query (SELECT issue_date, last_payment_date, term FROM loans WHERE term = '60 months' AND issue_date = 'Apr-2017' ORDER BY last_payment_date) was performed to see if issue_date can be predicted by adding the number of months in term to the last payment date, but was negative (e.g. loans issued in April 2017 have last payment dates ranging from Jan 2018 to Jan 2022). As there are so few rows with null values, and there is no reliable way of imputing the values, the null rows in last_payment_date were dropped.

There are 7 null values in last_credit_pull date, or 0.01%. This column is correlated fairly strongly (0.69) with last_payment_date as seen in the seaborn heatmap. However a scatterplot does not show a reliable pattern so the null rows were dropped.  

There are 51 null values in collections_12_mths_ex_med, or 0.09%. The seaborn heatmap shows this column is not strongly correlated with any other, so the null rows were dropped. 

### Dealing with skewness

pd.skew() was used to identify the skewness of each column in the dataframe. The skewed columns (defined as skew > 0.5) were transformed using a square root, log, and box-cox transformation to see which was the most effective. The effect of each transformation was also visualized using seaborn histplots. The most effective transformation for every column was Box Cox, which was therefore used to transform the entire dataframe, except the collections_12_mths_ex_med column, because the Box Cox transformation produced very large numbers that were unprocessable when trying to update the main dataframe. As a result a log transformation was used on this column. The id and member_id columns were also excluded from the transformation as they are specific numbers assigned to customers and should not be changed. 

### Removing outliers

A seaborn boxplot was used to visualize which columns might have outliers. Potential outliers were then investigated to see if they are part of natural variation, in which case they were retained, or if they are the result of error, in which case they were removed. Potential outliers were identified in recoveries and collection_recovery_fee, both of which had a few values well outside the whiskers in the boxplot. Using PGAdmin to view the original data for these columns was inconclusive - there are a few data points higher than the others, but not massively so. The two columns are strongly correlated with each other so a scatterplot was used to see if either of them contained any outliers in relation to each other. This suggested there were three outliers with very high values for recoveries compared to collection_recovery_fee. These values were therefore removed. 

### Removing highly correlated columns
A heatmap was used to identify highly correlated columns that could lead to overfitting. The threshold used was a correlation coefficient of 0.9. As a result, funded_amount, funded_amount_inv, and instalment were dropped as they are very highly correlated with loan_amount. Also removed were total_payment_inv and total_rec_prncp, which are very highly correlated with total_payment, and grade and sub_grade, which are very highly correlated with each other and with int_rate.