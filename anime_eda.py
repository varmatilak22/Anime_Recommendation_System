import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization settings
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['figure.dpi'] = 250
import warnings
warnings.filterwarnings('ignore')
sns.set_theme(style='darkgrid', palette='viridis')

# Load the dataset (assuming the file is local, replace the URL with the local file path)
df = pd.read_csv('https://raw.githubusercontent.com/Rushabh178/Data-Set/main/data/anime.csv')

# Check for missing values
print("Missing values in the dataset:")
print(df.isnull().sum())

# Drop rows with missing values in 'genre' and 'type'
df = df.dropna(subset=['genre', 'type'])

# Fill missing ratings with the average rating
average_rating = df['rating'].mean()
df['rating'].fillna(average_rating, inplace=True)

# Display basic statistics of the dataset
print("Basic statistics of the dataset:")
print(df.describe())

# Plotting distributions of 'rating' and 'members'
plt.figure()
sns.histplot(df['rating'], kde=True)
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.show()

plt.figure()
sns.histplot(df['members'], kde=True)
plt.title('Distribution of Members')
plt.xlabel('Members')
plt.ylabel('Frequency')
plt.show()

# Analyzing the relationship between rating and members
plt.figure()
sns.scatterplot(x='rating', y='members', data=df)
plt.title('Relationship between Rating and Members')
plt.xlabel('Rating')
plt.ylabel('Members')
plt.show()

# Check for the most frequent genres
df['genre'] = df['genre'].apply(lambda x: x.split(', '))
all_genres = [genre for sublist in df['genre'] for genre in sublist]
genre_count = pd.Series(all_genres).value_counts()

plt.figure()
sns.barplot(x=genre_count.index[:10], y=genre_count.values[:10])
plt.xticks(rotation=90)
plt.title('Top 10 Most Frequent Genres')
plt.xlabel('Genre')
plt.ylabel('Count')
plt.show()
