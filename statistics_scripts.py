import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

ALPHAH = 0.05
# Replace this with your actual data
data = pd.read_excel('kruskal_test.xlsx')
data = data.pivot(columns='luxury group', values='pricet in thousands')

# Group the data
groups = [data[col].dropna() for col in data.columns]

n = len(data)
k = len(groups)

# Levene's test for equal variances
levene_stat, levene_p = stats.levene(*groups)
equal_var = levene_p > ALPHAH
print(f"\n📏 Levene's Test: W={levene_stat:.4f}, p={levene_p:.4f}")

# Decide which test to run
if equal_var > ALPHAH:
    print("\n✅ Assumptions met: Performing ANOVA")
    model = ols('value ~ C(group)', data=data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print(anova_table)

    # Omega squared calculation
    ss_between = anova_table.loc['C(group)', 'sum_sq']
    ss_total = anova_table['sum_sq'].sum()
    df_between = anova_table.loc['C(group)', 'df']
    ms_error = anova_table.loc['Residual', 'sum_sq'] / anova_table.loc['Residual', 'df']
    omega_sq = (ss_between - (df_between * ms_error)) / (ss_total + ms_error)
    print(f"\n🧠 Omega Squared: {omega_sq:.4f}")
else:
    print("\n❌ Assumptions violated: Performing Kruskal-Wallis Test")
    kruskal_result = stats.kruskal(*groups)
    H = kruskal_result.statistic
    print(f"H-statistic: {kruskal_result.statistic:.4f}, p-value: {kruskal_result.pvalue:.4f}")
    epsilon_sq = (H - k + 1) / (n - k)
    print(f"Kruskal-Wallis H: {H:.4f}, p-value: {kruskal_result.pvalue:.4f}")
    print(f"Estimated Omega Squared (ε²): {epsilon_sq:.4f}")

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats

# Function to create a bar chart
def create_bar_chart(categories, values, title="Bar Chart"):
    plt.figure(figsize=(8, 5))
    sns.barplot(x=categories, y=values, palette="viridis")
    plt.title(title)
    plt.xlabel("Categories")
    plt.ylabel("Values")
    plt.tight_layout()
    plt.show()

# Function to create a scatter plot
def create_scatter_plot(x, y, title="Scatter Plot"):
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x=x, y=y, color="dodgerblue", edgecolor="black")
    plt.title(title)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.tight_layout()
    plt.show()

# Function to create a Q-Q plot
def create_qq_plot(data, title="Q-Q Plot"):
    plt.figure(figsize=(6, 6))
    stats.probplot(data, dist="norm", plot=plt)
    plt.title(title)
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Bar chart
    categories = ['A', 'B', 'C', 'D']
    values = [23, 45, 12, 36]
    create_bar_chart(categories, values)

    # Scatter plot
    x = np.random.rand(50)
    y = x * 2 + np.random.normal(0, 0.1, 50)
    create_scatter_plot(x, y)

    # Q-Q plot
    data = np.random.normal(loc=0, scale=1, size=100)
    create_qq_plot(data)
