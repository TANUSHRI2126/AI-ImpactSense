import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns # Optional: Used for nicer styling and heatmaps

# ---------------------------------------------------------
# 1. LOAD / CREATE DATA
# ---------------------------------------------------------

df = pd.read_csv('your_earthquake_data.csv')

# ---------------------------------------------------------
# 2. DATA PROCESSING
# ---------------------------------------------------------

# Basic check of the data
print("First 5 rows of the dataset:")
print(df.head())
print("\nDataset Info:")
print(df.info())

# Set a plotting style
plt.style.use('ggplot') 

# Create a figure with 2 rows and 2 columns
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Earthquake Dataset Analysis', fontsize=16, weight='bold')

# ---------------------------------------------------------
# 3. VISUALIZATIONS
# ---------------------------------------------------------

# PLOT 1: Histogram of Magnitude
# Shows how frequent certain earthquake strengths are
axes[0, 0].hist(df['magnitude'], bins=5, color='skyblue', edgecolor='black')
axes[0, 0].set_title('Distribution of Magnitude')
axes[0, 0].set_xlabel('Magnitude')
axes[0, 0].set_ylabel('Frequency')

# PLOT 2: Scatter Plot - Magnitude vs Depth
# Shows if there is a relationship between how deep and how strong the quake is
axes[0, 1].scatter(df['magnitude'], df['depth'], color='purple', alpha=0.7, s=100)
axes[0, 1].set_title('Magnitude vs. Depth')
axes[0, 1].set_xlabel('Magnitude')
axes[0, 1].set_ylabel('Depth (km)')
axes[0, 1].invert_yaxis() # Deep quakes are usually plotted going down

# PLOT 3: Bar Chart - Alert Counts
# Counts how many green, yellow, orange, red alerts exist
alert_counts = df['alert'].value_counts()
# map the index (alert name) to actual colors for the bars
bar_colors = [x if x in ['green', 'yellow', 'orange', 'red'] else 'gray' for x in alert_counts.index]

alert_counts.plot(kind='bar', ax=axes[1, 0], color=bar_colors, edgecolor='black')
axes[1, 0].set_title('Count of Alert Levels')
axes[1, 0].set_xlabel('Alert Level')
axes[1, 0].set_ylabel('Count')

# PLOT 4: Correlation Heatmap
# Shows statistical relationship between numeric columns
# We drop 'alert' because it is text, not number
numeric_df = df.drop(columns=['alert'])
corr = numeric_df.corr()

sns.heatmap(corr, annot=True, cmap='coolwarm', ax=axes[1, 1], fmt=".2f")
axes[1, 1].set_title('Correlation Matrix')

# ---------------------------------------------------------
# 4. SHOW PLOTS
# ---------------------------------------------------------
plt.tight_layout() # Adjusts spacing so labels don't overlap
plt.subplots_adjust(top=0.90) # Make room for the main title
plt.show()