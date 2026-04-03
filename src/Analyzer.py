# Phase 1: Data Wrangling & Cleaning
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

## Load and basic cleaning
df = pd.read_csv('netflix_titles.csv')

### 1. Handle Missing Values
df['country'] = df['country'].fillna('Unknown')
df['cast'] = df['cast'].fillna('No Data')
df.dropna(subset=['date_added', 'rating'], inplace=True)

### 2. Fix Date Formatting
df['date_added'] = pd.to_datetime(df['date_added'].str.strip())
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month_name()

#Phase 2: Core EDA & Visualizations
## 1. The Content Split (Movies vs. TV Shows)
plt.figure(figsize=(7, 5))
sns.countplot(x='type', data=df, palette=['#e50914', '#221f1f'])
plt.title('Distribution of Movies vs TV Shows')
plt.show()

## 2. Content Growth Over Time
content_by_year = df.groupby(['year_added', 'type']).size().unstack().fillna(0)
content_by_year.plot(kind='line', figsize=(12, 6), color=['#e50914', '#b20710'])
plt.title('Content Added Over the Years')
plt.ylabel('Number of Titles')

## 3. Top 10 Countries producing Content

# Explode the country column for accurate counts
countries = df['country'].str.split(', ').explode().value_counts().head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=countries.values, y=countries.index, palette='Reds_r')
plt.title('Top 10 Content Producing Countries')

# Filter top 10 countries and cross-tabulate with ratings
top_countries_list = df['country'].value_counts().head(10).index
subset = df[df['country'].isin(top_countries_list)]

rating_map = pd.crosstab(subset['country'], subset['rating'])
sns.heatmap(rating_map, annot=True, cmap='Reds', fmt='d')
plt.title('Content Rating Distribution by Country')

# 3. Top 10 Countries producing Content
