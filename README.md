# Exploratory Data Analysis Project - Finance

This project simulates performing exploratory data analysis on a database of customer loan data for a finance company. 

Technologies used: Python, pandas, PostreSQL, sqlalchemy

## Usage Instructions

## Project Components / File Structure

### Deciding whether to drop columns with many null values

There are a few columns with a high number of null values: around 60% for mths_since_last_delinq and next_payment_date, and between 85 and 90% for mths_since_last_record and mths_since_last_major_derog. The high number of null values in the columns counting months since last delinquency, public record, and major derogatory is presumably due to the fact that most customers have repaid their loans in accordance with the terms. The presence of one of these indicators of credit risk in a customer's account is crucial information for the loan company. As a result, these columns should not be dropped despite the high number of nulls. Neither should the values be imputed using the mean or median, as this would falsely create the impression that all customers had recently failed to repay, which could significantly affect their treatment by the company. One solution is to replace all the null values with the value 0, perhaps with a note indicating that a value of 0 represents never. 

For next_payment_date, it is not immediately clear why there are so many nulls, so further analysis was performed to help decide whether to drop this column or impute the values. The following SQL query revealed that all of the accounts with a null next payment date were either "fully paid" or "charged off":

SELECT DISTINCT loan_status
FROM loans
WHERE next_payment_date IS NULL

The values should therefore not be imputed as they are not missing at random and imputing them would create a false impression that there were outstanding payments due on these loans.

For columns with a small number of nulls, the choice was made whether to impute by the mean or median. For columns with normally distributed data, the mean was used. For columns with skewed data the median was used.

The first in the list is funded_amount, which has 3007 null values, or 5.5%. Using the Plotter class to view the distribution shows the data is skewed to the right, although with a cluster at 35000 (the highest amount available). The median of funded_amount is 12,000. However on closer inspection it was decided not to impute the null values using the median because of the extremely close correlation between funded_amount and loan_amount as seen using sns.pairplot. A SQL query revealed they are only different in 941 cases (0.17%). Also, the funded amount is always less than or equal to the loan amount, so using 12,000 would be incorrect in rows where loan_amount is less than 12,000. As the median of loan_amount is also 12,000, this would clearly lead to errors. As a result the null values in funded_amount were filled by using the value from loan_amount.

The next column is term, which has 4772 null values, or 8.8%. Term is a categorical variable with two values: 60 months and 36 months. The mode is 36 months, with 66% of rows. More information is needed before deciding whether to impute using the mode: are the different term values correlated with any other variables? It would make sense for term length to be influenced by e.g. loan amount. Using SQL to check the average loan amount for each term length (SELECT term, AVG(loan_amount) FROM loans GROUP BY term) shows that the average loan amount for 60-month terms is 18233.5, while for 36-month terms it is 11477.5. As a result it was decided to replace null values in term with 60 months if loan_amount > 14855.5 and 36 months otherwise.

The next column with nulls is int_rate, with 9.5% nulls (5169 rows). Again, it would make sense for the interest rate to be correlated with other factors such as loan amount, loan status, or grade. Running the SQL query (SELECT AVG(int_rate) AS avg_int_rate, grade FROM loans GROUP BY grade ORDER BY avg_int_rate ASC) shows clearly that the interest rate increases as the grade gets worse: an average of 7.5% for A grade loans, 11.4% for B grade loans, 14.6% for C grade loans, 17.4% for D grade loans, 19.9% for E grade loans, 22.4% for F grade loans, and 23% for G grade loans. These averages were used to fill the null values in the int_rate column based on the corresponding grade (there are no nulls in the grade column).

The next column with nulls is employment_length. 