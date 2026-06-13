import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the dataset safely
df = pd.read_csv('population_csv.csv', skiprows=4)

# 2. Clean up regional groupings to avoid skewed chart metrics
regions_to_drop = ['World', 'High income', 'OECD members', 'Post-demographic dividend', 
                   'IDA & IBRD total', 'Low & middle income', 'Middle income', 'IBRD only',
                   'East Asia & Pacific', 'Europe & Central Asia', 'Latin America & Caribbean',
                   'South Asia', 'Sub-Saharan Africa']
df_countries = df[~df['Country Name'].isin(regions_to_drop)].dropna(subset=['2022'])

# =================================================================
# SET UP A 2x2 CANVAS GRID (4 Graphs in One Window)
# =================================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Comprehensive Population Data Analysis Dashboard (Task 1)', fontsize=18, fontweight='bold')

# -----------------------------------------------------------------
# GRAPH 1: Top 15 Most Populous Countries (Bar Chart)
# Shows the exact scale of the largest individual nations
# -----------------------------------------------------------------
top_15 = df_countries.sort_values(by='2022', ascending=False).head(15)
sns.barplot(ax=axes[0, 0], x='2022', y='Country Name', data=top_15, palette='viridis')
axes[0, 0].set_title('Top 15 Countries by Total Population (2022)', fontweight='bold')
axes[0, 0].set_xlabel('Population Count')
axes[0, 0].set_ylabel('Country')

# -----------------------------------------------------------------
# GRAPH 2: Distribution of All Country Sizes (Histogram)
# Visually captures all 200+ remaining data points at once
# -----------------------------------------------------------------
sns.histplot(ax=axes[0, 1], x=df_countries['2022'], bins=30, kde=True, color='crimson')
axes[0, 1].set_title('Global Distribution of Country Sizes', fontweight='bold')
axes[0, 1].set_xlabel('Population Scale Bracket')
axes[0, 1].set_ylabel('Number of Countries')

# -----------------------------------------------------------------
# GRAPH 3: Historical Timeline Comparison (Line Plot)
# Visualizes historical shifts across multiple years (1960 vs 2022)
# -----------------------------------------------------------------
# We reshape a tiny subset to show a timeline trajectory
sample_countries = ['India', 'United States', 'Brazil', 'Nigeria', 'Japan']
timeline_df = df_countries[df_countries['Country Name'].isin(sample_countries)]

# Melt the columns so years become rows for plotting
melted_df = timeline_df.melt(id_vars=['Country Name'], value_vars=['1960', '1980', '2000', '2022'],
                             var_name='Year', value_name='Population')

sns.lineplot(ax=axes[1, 0], x='Year', y='Population', hue='Country Name', data=melted_df, marker='o', linewidth=2.5)
axes[1, 0].set_title('Historical Population Growth Trends (1960 - 2022)', fontweight='bold')
axes[1, 1].set_xlabel('Timeline Year')
axes[1, 0].set_ylabel('Population')

# -----------------------------------------------------------------
# GRAPH 4: Regional Scale Check (Pie Chart)
# Visualizes macro regional chunks of the global population
# -----------------------------------------------------------------
regional_groups = ['East Asia & Pacific', 'Europe & Central Asia', 'Latin America & Caribbean', 
                   'Middle East & North Africa', 'North America', 'South Asia', 'Sub-Saharan Africa']
df_regions = df[df['Country Name'].isin(regional_groups)].dropna(subset=['2022'])

axes[1, 1].pie(df_regions['2022'], labels=df_regions['Country Name'], autopct='%1.1f%%', 
               startangle=140, colors=sns.color_palette('pastel'))
axes[1, 1].set_title('Continental Distribution of Global Population (2022)', fontweight='bold')

# =================================================================
# DISPLAY THE COMPLETED WINDOW LAYOUT
# =================================================================
plt.tight_layout()
plt.show()
