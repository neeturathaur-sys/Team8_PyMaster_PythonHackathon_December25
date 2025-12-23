# Team8_PyMaster_PythonHackathon_December25
The Flatten dataset consists of three versions of the survey referred to as Schema 1, Schema 2, and Schema 3. As compared to Schema 1, subsequent versions either include additional questions or refine existing question and answer options. 
Each survey response is stored as an individual record (row) in the dataset.

Problem Statement:
This study aims to determine whether early self‑reported symptoms, exposure histories, and demographic factors from the FLATTEN COVID‑19 survey can be used to predict probable SARS‑CoV‑2 infection and reveal geographic and communicative disparities in health information dissemination.

Methods and Analysis:
1 Data cleaning
	1 Data Integrity
		Load the dataset and verify data types.
	I	dentify missing values, inconsistent formats (e.g., 'Y' vs 'y' vs 'Yes'), and correct them.
		Standardize categorical variables (e.g., symptoms, exposure history, demographic labels).
	2 Data Transformation
		Convert binary(y/n) responses to numeric (0/1) ).
		Normalize/encode categorical variables (one-hot encoding for multi-category fields).
		Converted weeks into months to make consistency among all datasets.
2 Descriptive Statistics
	Summarize participant demographics (age, sex, region).
	Frequency of self-reported symptoms and exposures.
3 Symptom & Exposure Patterns
	Visualize symptom prevalence (e.g., bar charts) grouped by COVID results.
	Statistical cross-tabulations:
	Symptom presence vs positivity
	Exposure history vs positivity
4 Risk Stratification
	Create risk scores (e.g., your Triage_Score) and categorize into risk groups.
	Compare positivity rates across risk groups.
5 Geographical Insights
	Aggregate measures by geographic units (FSA/region):
	Positivity rate
	High-risk population density
	Average symptom burden
	Identify clusters/high-risk areas using geospatial charts.