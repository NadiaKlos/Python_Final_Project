# Python_Final_Project

The dataset represents ten years (1999-2008) of clinical care at 130 US hospitals and integrated delivery networks. Each row concerns hospital records of patients diagnosed with diabetes, who underwent laboratory, medications, and stayed up to 14 days. The goal is to determine the early readmission of the patient within 30 days of discharge.

# Dataset Characteristics
Multivariate

# Subject Area
Health and Medicine

# Associated Tasks
Classification, Clustering

# Feature Type
Categorical, Integer

# Instances
101766

# Features
47

The data contains such attributes as patient number, race, gender, age, admission type, time in hospital, medical specialty of admitting physician, number of lab tests performed, HbA1c test result, diagnosis, number of medications, diabetic medications, number of outpatient, inpatient, and emergency visits in the year before the hospitalization, etc.

We first pre-processed the dataset, reducing it to 25% of its original size (but still with 26,000 rows remaining).
We then proceeded to visualize certain columns to better understand the ins and outs.
Finally, we used classification models on the target column to predict whether patients would be readmitted or not.

However, as the 'NO' class is dominant in the target column, the models may learn to simply predict this majority class to maximize its accuracy, even if it doesn't capture well the cases of the minority classes. This can result in biased models. 
