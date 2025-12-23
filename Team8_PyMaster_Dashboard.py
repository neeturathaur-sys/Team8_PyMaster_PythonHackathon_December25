import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator


#Reading the cleaned data 
survey1=pd.read_excel("cleaned_schema_1_data.xlsx")
survey2=pd.read_excel("cleaned_schema_2_data.xlsx")
survey3=pd.read_excel("cleaned_schema_3_data.xlsx")

#Creating a copy of the original data to protect unnecessary modification in original data.
df1=survey1.copy()
df2=survey2.copy()
df3=survey3.copy()

#chart1 data
total_resp1 = len(df1)
total_resp2 = len(df2)
total_resp3 = len(df3)

phases = ['Survey Phase 1', 'Survey Phase 2', 'Survey Phase 3']
responses = [total_resp1, total_resp2, total_resp3]

#----- Data to chart 2 --------#
to_exclude = ['none', 'na']

ethnicity_data = df2[
    ~df2['ethnicity'].str.lower().isin(to_exclude)
].copy()

# Count ethnicity
to_exclude = ['none', 'na']

ethnicity_data = df2[
    ~df2['ethnicity'].str.lower().isin(to_exclude)
].copy()

full_counts = ethnicity_data['ethnicity'].value_counts()

combined_ethnicity = pd.concat([
    full_counts.head(5),
    pd.Series({'Others': full_counts.iloc[5:].sum()})
])
total = combined_ethnicity.sum()
#Age data
def age_counts(df):
    # Automatically detect columns containing age groups
    age_columns = {
        '<26': [col for col in df.columns if 'age_1_<26' in col],
        '26-44': [col for col in df.columns if 'age_1_26-44' in col],
        '45-64': [col for col in df.columns if 'age_1_45-64' in col],
        '>65': [col for col in df.columns if 'age_1_>65' in col]
    }
    
    # Sum across columns in case there are multiple variants
    counts = {}
    for age_group, cols in age_columns.items():
        if cols:
            counts[age_group] = df[cols].sum().sum()  # sum across all columns and rows
        else:
            counts[age_group] = 0
    return counts
#Rename df1 age column to match with other dfs
df1_newCol = df1.rename(columns={'age_binary': 'age_1_>65'})


counts1 = age_counts(df1_newCol)
counts2 = age_counts(df2)
counts3 = age_counts(df3)
#print(age_counts_df3)

df_counts1 = pd.DataFrame(list(counts1.items()), columns=['Age Group', 'Survey1'])
df_counts2 = pd.DataFrame(list(counts2.items()), columns=['Age Group', 'Survey2'])
df_counts3 = pd.DataFrame(list(counts3.items()), columns=['Age Group', 'Survey3'])

# Merge by Age Group
combined_counts = pd.merge(df_counts1, df_counts2, on='Age Group')
combined_counts = pd.merge(combined_counts, df_counts3, on='Age Group')

# Add a Total column
combined_counts['Total'] = (
    combined_counts['Survey1'] +
    combined_counts['Survey2'] +
    combined_counts['Survey3']
)


# Calculate column totals
survey_totals = combined_counts[['Survey1','Survey2', 'Survey3']].sum()

# Calculate percentages
combined_counts['Survey1_%'] = (combined_counts['Survey1'] / survey_totals['Survey1']) * 100
combined_counts['Survey2_%'] = (combined_counts['Survey2'] / survey_totals['Survey2']) * 100
combined_counts['Survey3_%'] = (combined_counts['Survey3'] / survey_totals['Survey3']) * 100
grand_total = combined_counts['Total'].sum()

combined_counts['Overall_%'] = (combined_counts['Total'] / grand_total) * 100
#round percentage for readability
combined_counts[['Survey1_%','Survey2_%', 'Survey3_%', 'Overall_%']] = \
    combined_counts[['Survey1_%','Survey2_%', 'Survey3_%', 'Overall_%']].round(2)

#------------------------ --------#
#######Data for chart 4 ##########
#--------------------------------#
monthwise_summary = df3.groupby('covid_results_date')['covid_positive'].agg(
    Total_Testing='count',      # total responses in the month
    Positive_Cases='sum'           # total positive cases
).reset_index()

# Calculate positivity rate
monthwise_summary['Positivity_Rate (%)'] = (
    monthwise_summary['Positive_Cases'] / monthwise_summary['Total_Testing'] * 100
)

# Define correct month order
month_order = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'
]

# Correct any spelling issues in your data
monthwise_summary['covid_results_date'] = monthwise_summary['covid_results_date'].replace({
    'Feburary': 'February'  # fix spelling
})

# Convert to categorical with ordered months
monthwise_summary['covid_results_date'] = pd.Categorical(
    monthwise_summary['covid_results_date'],
    categories=month_order,
    ordered=True
)

# Sort by month
monthwise_summary = monthwise_summary.sort_values('covid_results_date').reset_index(drop=True)

#----------------------#
##### Chart 5 data#####
#----------------------#
tested_df = df3.dropna(subset=['covid_positive'])

# List of symptoms to analyze (as they appear in your column headers)
symptom_cols = {
    'symp_lossOfSmellTaste': 'Loss of Smell/Taste',
    'symp_fever': 'Fever',
    'symp_cough': 'Cough',
    'symp_shortnessOfBreath': 'Shortness of Breath',
    'symp_chills': 'Chills',
    'symp_soreThroat': 'Sore Throat',
    'symp_diarrhea': 'Diarrhea'
}

# 2. Perform Live Analysis
analysis_results = []

for col, clean_name in symptom_cols.items():
    # Filter for people who have this specific symptom
    has_symptom = tested_df[tested_df[col] == 1]
    total_with_symptom = len(has_symptom)
    
    if total_with_symptom > 0:
        # Calculate PPV: (Positive Tests / Total people with that symptom)
        positive_count = has_symptom['covid_positive'].sum()
        ppv = (positive_count / total_with_symptom) * 100
        
        analysis_results.append({
            'Symptom': clean_name,
            'Prob': round(ppv, 1),
            'Count': total_with_symptom
        })

# ---------------------------
# Sample data (replace with real values)
# ---------------------------
def prioritize_wellness_media(df):
    youth_df = df[df['age_1_<26'] == 1].copy()
    
    if youth_df.empty:
        print("No data found for users under 26.")
        return None

    # 2. Identify Negative Mental Health Impact
    youth_df['mh_neg_impact'] = (youth_df['mental_health_impact'] == 'negatively').astype(int)
    
    # 3. Process Media Channels
    media_list = ['twitter', 'reddit', 'instagram', 'facebook', 'tiktok', 'tv', 'radio']
    media_risk_data = []
    
    # Fill missing values to prevent string search errors
    youth_df['media_channels'] = youth_df['media_channels'].fillna('').astype(str).str.lower()
    
    for channel in media_list:
        # Check if user uses this channel
        has_channel = youth_df['media_channels'].str.contains(channel)
        
        if has_channel.sum() > 0:
            risk_rate = youth_df[has_channel]['mh_neg_impact'].mean() * 100
            user_count = has_channel.sum()
            
            media_risk_data.append({
                'Media Channel': channel.capitalize(),
                'Negative MH Impact (%)': round(risk_rate, 2),
                'Youth User Count': user_count
            })
    
    analysis_df = pd.DataFrame(media_risk_data).sort_values(by='Negative MH Impact (%)', ascending=False)
    return analysis_df
#days = np.arange(1, 8)
#daily_cases = [120, 150, 180, 160, 200, 220, 210]

# ---------------------------
# Streamlit setup
# ---------------------------
st.set_page_config(page_title="Survey Dashboard", layout="wide")
st.title("📊 Survey Analysis Dashboard")

# ===========================
# Row 1 (3 columns)
# ===========================
col1, col2, col3 = st.columns(3)

# Chart 1: Survey phase responses
with col1:
    st.subheader("Total Responses by Phase")
    fig1, ax1 = plt.subplots()
    bars = ax1.bar(phases, responses, color=['steelblue', 'orange', 'green'])
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, height, f'{height:,}',
                 ha='center', va='bottom')
    ax1.set_ylabel("Responses")
    st.pyplot(fig1)

# Chart 2: Ethnicity frequency
with col2:
    st.subheader("Total Responses by Ethinicity")
    fig2, ax2 = plt.subplots(figsize=(10, 7))

    explode = [0.05 if i > 1 else 0 for i in range(len(combined_ethnicity))]

    wedges, _ = ax2.pie(
   	 combined_ethnicity,
    	startangle=140,
    	colors=plt.cm.Paired.colors,
    	explode=explode
   	 )
    legend_labels = [
   	 f'{label}: {val} ({(val/total)*100:.1f}%)'
    	for label, val in combined_ethnicity.items()
    ]
    ax2.legend(wedges, legend_labels, title="Ethnicity", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    st.pyplot(fig2)

# Chart 3: Age distribution
with col3:
    st.subheader("Age Distribution")
    fig, ax = plt.subplots(figsize=(7,5))
    fig3, ax3 = plt.subplots()
    ax3.bar(
        combined_counts['Age Group'],
        combined_counts['Overall_%'],
            color='steelblue'
)

#ax.set_title("Overall Age Distribution Across All Surveys")
    ax3.set_xlabel("Age Group")
    ax3.set_ylabel("Percentage of Participants")
    ax3.yaxis.set_major_locator(MaxNLocator(integer=True))

# Add value labels
    for i, val in enumerate(combined_counts['Overall_%']):
        ax.text(i, val + 0.5, f"{val}%", ha='center')

    
    #fig3, ax3 = plt.subplots()
    #ax3.bar(age_groups, age_counts, color='purple')
    #ax3.set_ylabel("Respondents")
    st.pyplot(fig3)

# ===========================
# Row 2 (3 columns)
# ===========================
col4, col5, col6 = st.columns(3)

# Chart 4: COVID positivity monthly chart
with col4:
    st.subheader("Monthly testing & COVID rate")
    plt.figure()
    fig4, ax4 = plt.subplots()
    plt.bar(
        monthwise_summary['covid_results_date'].astype(str),
        monthwise_summary['Total_Testing'],
        color='skyblue',
        label='Total Testing'
    )
    plt.plot(
        monthwise_summary['covid_results_date'].astype(str),
        monthwise_summary['Positive_Cases'],
        color='red',
        marker='o',
        linewidth=2,
        label='Positive Cases'
    )
    plt.xlabel('Month')
    plt.ylabel('Count')
    plt.title('Month-wise COVID-19 Testing and Positive Cases')
    for label in ax.get_xticklabels():
        label.set_rotation(45)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot(fig4)


# Chart 5: Symptoms by probbelity chart
with col5:
    plot_df = pd.DataFrame(analysis_results).sort_values(by='Prob', ascending=True)
    st.subheader("Symptoms as COVID-19 Predictors")
    plt.figure()
    fig5, ax5 = plt.subplots()


    # Highlight the primary policy predictor (Loss of Smell/Taste) in red
    colors = ['#e74c3c' if x == 'Loss of Smell/Taste' else'#3498db' for x in plot_df['Symptom']]

    bars = ax5.barh(plot_df['Symptom'], plot_df['Prob'], color=colors)

    # Labels and Styling
    ax5.set_title('Strength of Symptoms as COVID-19 Predictors')
    ax5.set_xlabel('Probability of Positive Test (%)')
    ax5.set_xlim(0, 100)
    ax5.grid(axis='x', linestyle='--', alpha=0.7)

    # Add value labels to the end of each bar
    for bar in bars:
        width = bar.get_width()
        ax5.text(width + 2, bar.get_y() + bar.get_height()/2, f'{width}%', 
            va='center', fontweight='bold', color='#2c3e50')

    st.pyplot(fig5)

# Chart 6: Response trend
with col6:
    st.subheader("Negative Mental Health per Media Channel")
    fig6, ax6 = plt.subplots()
    
    analysis_df = prioritize_wellness_media(df3)
    colors = plt.cm.RdYlGn_r(np.linspace(0, 0.8, len(analysis_df)))
        
    bars = plt.bar(analysis_df['Media Channel'], analysis_df['Negative MH Impact (%)'], color=colors)
    plt.title('Digital Wellness Priority: Negative Mental Health per Media Channel', fontsize=14, fontweight='bold')
    plt.ylabel('Percentage Reporting Negative Impact (%)')
    plt.ylim(0, 105) # Extra room for labels
        
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval}%', ha='center', fontweight='bold')

        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()

    
    st.pyplot(fig6)
