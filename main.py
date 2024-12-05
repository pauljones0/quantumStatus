import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
import pandas as pd

# Define the quadratic function for fitting
def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

# Load the post counts data
with open('cleanedData/post_counts.json', 'r') as f:
    data = json.load(f)

# Prepare data for table
table_data = []

# Prepare the plot
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))
plt.title("Blog Post Counts: Historical Data and Predictions", fontsize=16)

# Colors for categories
colors = {
    "Quantum": "blue",
    "Ai": "green"
}

# Markers for subcategories
markers = {
    "QuantumComputing": "o",
    "CudaQ": "s",
    "CuQuantum": "D",
    "GenerativeAi": "v",
    "Ai": "^",
    "Cuda": "P"
}

# Iterate through each main category and subcategory
for category, subcategories in data.items():
    for subcat, counts in subcategories.items():
        years = np.array([int(year) for year in counts.keys()])
        posts = np.array(list(counts.values()))
        
        # Fit a quadratic curve
        popt, _ = curve_fit(quadratic, years, posts)
        
        # Predict until reaching 500 posts per year for Quantum
        if category == "Quantum":
            target = 500
            future_year = years.max()
            while True:
                future_year += 1
                prediction = quadratic(future_year, *popt)
                if prediction >= target:
                    break
            future_years = np.arange(years.min(), future_year + 1)
        else:
            # Predict for the next 10 years
            future_years = np.arange(years.min(), years.max() + 10 + 1)
        
        predictions = quadratic(future_years, *popt)
        
        # Plot historical data
        plt.scatter(years, posts, label=f"{subcat} (actual)", color=colors.get(category, 'black'), marker=markers.get(subcat, 'o'))
        
        # Add data labels
        for x, y in zip(years, posts):
            plt.text(x, y, str(y), fontsize=9, ha='right')
        
        # Plot predictions
        plt.plot(future_years, predictions, label=f"{subcat} (predicted)", linestyle='--', color=colors.get(category, 'black'))
        
        # Append to table data
        for year, post in zip(years, posts):
            table_data.append({
                "Category": category,
                "Subcategory": subcat,
                "Year": year,
                "Posts": post
            })

# Configure logarithmic Y-axis
plt.yscale('log')

plt.xlabel("Year")
plt.ylabel("Blog Posts")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Save the plot
os.makedirs('output', exist_ok=True)
plt.savefig('output/blog_post_counts.png')
plt.close()

# Create a DataFrame for the table
df = pd.DataFrame(table_data)
df_sorted = df.sort_values(by=["Category", "Subcategory", "Year"])

# Save the table as a CSV file
df_sorted.to_csv('output/blog_post_counts_table.csv', index=False)

# Pretty print the table to a Markdown file
df_pivot = df_sorted.pivot_table(index=["Category", "Subcategory"], columns="Year", values="Posts", fill_value=0)
df_pivot.to_markdown('output/blog_post_counts_table.md')

# Update README.md with references to the output files
readme_content = """
# quantumStatus
Identifying where in the Hype cycle we are, using Nvidia BlogPosts as guidance

## Analysis Results

### Blog Post Counts Overview
![Blog Post Counts](output/blog_post_counts.png)

### Detailed Post Counts Table
You can find the detailed table of blog post counts and forecasts in the following files:
- CSV: [blog_post_counts_table.csv](output/blog_post_counts_table.csv)
- Markdown: [blog_post_counts_table.md](output/blog_post_counts_table.md)

## Generalizations
- **AI vs Quantum**: AI blog posts significantly outpace Quantum Computing posts, indicating a higher level of investment and focus in AI-related research and development at Nvidia.
- **Growth Trends**: AI shows consistent growth, while Quantum Computing has sporadic increases, suggesting emerging interest but less established traction.
- **Forecasts**: Quantum Computing is projected to grow to meet AI's 2024 post count, aligning with potential increases in investment and market focus.

## Issues with Data Analysis
- **Data Source**: The analysis is based solely on the number of blog posts tagged with specific keywords on Nvidia's website. This may not accurately reflect the overall investment or growth in each field.
- **Market Monopoly**: Nvidia does not have a monopoly in Quantum Computing as it does in AI, potentially leading to fewer exclusive blog posts.
- **Historical Data**: Nvidia's website began in 2011, limiting the historical data available for analysis.
- **Marketing Influence**: The number of blog posts may be influenced by the size and focus of Nvidia's marketing department, rather than direct investment or technological advancement.

"""

with open('README.md', 'w') as f:
    f.write(readme_content)
