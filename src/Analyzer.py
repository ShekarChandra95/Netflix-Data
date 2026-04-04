# Phase 1: Data Wrangling & Cleaning
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load and basic cleaning
df = pd.read_csv(r'C:\Users\chand\Downloads\Netflix_Movies_and_TV_Shows.csv')

# 1. Handle Missing Values
df['Country'] = df['Country'].fillna('Unknown')
df['Genre'] = df['Genre'].fillna('No Data')
print(df.columns.tolist())
df.dropna(subset=['Rating'], inplace=True)
target_cols = ['date_added', 'Rating']
# This line keeps only the columns that are actually in df.columns
existing_cols = [c for c in target_cols if c in df.columns]

df.dropna(subset=existing_cols, inplace=True)

# 2. Fix Date Formatting
df['Release Year'] = pd.to_datetime(df['Release Year'].astype(str).str.strip(), format='%Y')
df['year_added'] = df['Release Year'].dt.year
df['month_added'] = df['Release Year'].dt.month_name()

#Phase 2: Core EDA & Visualizations
# 1. The Content Split (Movies vs. TV Shows)
plt.figure(figsize=(3, 2))
sns.countplot(x='Type', data=df, hue='Type', palette=["#1fe509", "#2626bd"], legend=False)
plt.title('Distribution of Movies vs TV Shows')
plt.show()

## 2. Content Growth Over Time
content_by_year = df.groupby(['year_added', 'Type']).size().unstack().fillna(0)
content_by_year.plot(kind='line', figsize=(12, 6), color=["#2c0c95", '#b20710'])
plt.title('Content Added Over the Years')
plt.ylabel('Number of Titles')
plt.show()

## 3. Top 10 Countries producing Content

# Explode the country column for accurate counts
countries = df['Country'].str.split(', ').explode().value_counts().head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=countries.values, y=countries.index, hue=countries.index, palette='Reds_r', legend=False)
plt.title('Top 10 Content Producing Countries')
plt.show()

# Filter top 10 countries and cross-tabulate with ratings
top_countries_list = df['Country'].value_counts().head(10).index
subset = df[df['Country'].isin(top_countries_list)]

rating_map = pd.crosstab(subset['Country'], subset['Rating'])
sns.heatmap(rating_map, annot=True, cmap='Reds', fmt='d')
plt.title('Content Rating Distribution by Country')
plt.show()
