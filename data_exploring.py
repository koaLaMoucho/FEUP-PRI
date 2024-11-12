from matplotlib import pyplot as plt
import pandas as pd
from wordcloud import WordCloud

# Load your CSV file
df = pd.read_csv('onepiece_allepisodes_with_ratings.csv')
"""
missing_data = df.isnull().sum()

## see which lines are missing

text_data = ' '.join(df['Long Summary'].dropna().tolist()) + ' ' + \
            ' '.join(df['Short Summary'].dropna().tolist())

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)

# Display the word cloud using matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Hide the axes
plt.show()
"""
"""
from collections import Counter


all_characters = ' '.join(df['Characters'].dropna().tolist()).split(',')

all_characters = [char.strip() for char in all_characters]  
character_counts = Counter(all_characters) 

# Convert to DataFrame for better visualization
character_df = pd.DataFrame(character_counts.items(), columns=['Character', 'Count'])
character_df = character_df.sort_values(by='Count', ascending=False)  # Sort by frequency

colors = ['#FF5733', '#33FF57', '#3357FF', '#F3FF33', '#FF33A1', 
          '#FF9133', '#33FFF1', '#3357F3', '#F333FF', '#F3FF33']

plt.figure(figsize=(12, 6))
plt.bar(character_df['Character'][:10], character_df['Count'][:10], color=colors)
plt.xlabel('Characters')
plt.ylabel('Frequency')
plt.title('Top 10 Most Frequent Characters in One Piece Episodes')
plt.xticks(rotation=45)  # Rotate character names for better readability
#decrease font size
plt.xticks(fontsize=6)
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add horizontal grid lines
plt.show()
"""

"""
# Function to calculate word count
def word_count(text):
    if pd.isna(text):  # Handle NaN values
        return 0
    return len(text.split())  # Count words by splitting the text

# Calculate word count for Long Summary
df['Short_Summary_Word_Count'] = df['Short Summary'].apply(word_count)

# Initialize variables for counting
averages = []
total_words = 0
total_episodes = 0

# Loop through the DataFrame to calculate averages in batches of 100 episodes
for index, row in df.iterrows():
    total_words += row['Short_Summary_Word_Count']
    total_episodes += 1
    
    # If 100 episodes have been counted, calculate the average
    if total_episodes == 100:
        averages.append(total_words / total_episodes)  # Calculate the average word count
        total_words = 0  # Reset total words for the next batch
        total_episodes = 0  # Reset total episodes for the next batch

# Handle remaining episodes (if any)
if total_episodes > 0:
    averages.append(total_words / total_episodes)

# Create a list for episode ranges

episode_ranges = [f"{i*100+1}-{(i+1)*100}" for i in range(len(averages))]



#Instead of the last range being 1101-1200, make it 1101-1120
episode_ranges[-1] = f"{1101}-{1120}"

# Plotting the average word counts over episode ranges
plt.figure(figsize=(10, 6))
plt.bar(episode_ranges, averages, color='orange')

# Adding titles and labels
plt.title('Average Word Count in Short Summaries by Episode Ranges')
plt.xlabel('Episode Range')
plt.ylabel('Average Word Count')
plt.xticks(rotation=45)
# Rotate x-axis labels for better readability
#change font size
plt.xticks(fontsize=8)
plt.grid(axis='y')
plt.show()"""


df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

# Variables to store totals and averages
total_ratings = 0
total_episodes = 0
averages = []

# Loop through the DataFrame to calculate averages in batches of 100 episodes
for index, row in df.iterrows():
    rating = row['Rating']
    
    # Only consider valid ratings (skip NaN values)
    if not pd.isna(rating):
        total_ratings += rating
        total_episodes += 1

    # Every 100 episodes, calculate the average
    if total_episodes == 100:
        averages.append(total_ratings / total_episodes)  # Calculate the average rating
        total_ratings = 0  # Reset for the next batch
        total_episodes = 0  # Reset episode count

# Handle any remaining episodes (e.g., from 1101 to 1120)
if total_episodes > 0:
    averages.append(total_ratings / total_episodes)

# Create a list for episode ranges (e.g., "1-100", "101-200")
episode_ranges = [f"{i*100+1}-{(i+1)*100}" for i in range(len(averages))]

# Adjust the last range if it's not a full 100 episodes (e.g., 1101-1120)
episode_ranges[-1] = f"{1101}-1120"

# Plotting the average ratings over episode ranges
plt.figure(figsize=(10, 6))
plt.bar(episode_ranges, averages, color='orange')

# Adding titles and labels
plt.title('Average Ratings by Episode Ranges')
plt.xlabel('Episode Range')
plt.ylabel('Average Rating')
plt.xticks(rotation=45)

# Adjust font size and grid
plt.xticks(fontsize=8)
plt.grid(axis='y')
plt.ylim(4, 5)
# Show the plot
plt.show()