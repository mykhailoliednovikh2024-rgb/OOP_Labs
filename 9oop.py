
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv('Job opportunities.csv')

def clean_salary(salary_str):
    if pd.isna(salary_str): return 0
    clean_str = str(salary_str).replace('£', '').replace('$', '').replace(',', '').replace(' ', '').lower().replace('k', '000')
    parts = clean_str.split('-')
    try:
        return (int(parts[0]) + int(parts[1])) / 2 if len(parts) == 2 else int(parts[0])
    except: return 0

df['Average Salary'] = df['Salary Range'].apply(clean_salary)
df['Year'] = pd.to_datetime(df['Date Posted']).dt.year

plt.figure(figsize=(10, 6))
sns.barplot(x='Experience Level', y='Average Salary', data=df, palette='viridis')
plt.title('Average Salary by Experience Level')
plt.xlabel('Experience Level')
plt.ylabel('Average Salary')
plt.show()


plt.figure(figsize=(12, 6))
sns.boxplot(x='Industry', y='Average Salary', data=df, palette='Set2')
plt.xticks(rotation=45, ha='right')
plt.title('Salary Distribution by Industry')
plt.xlabel('Industry')
plt.ylabel('Average Salary')
plt.tight_layout()
plt.show()
plt.figure(figsize=(10, 8))
pivot_table = pd.crosstab(df['Experience Level'], df['Industry'])
sns.heatmap(pivot_table, annot=True, cmap='viridis', linewidths=0.5)
plt.title('Number of Jobs: Experience vs Industry')
plt.show()
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Year', y='Average Salary', hue='Experience Level', data=df, palette='deep', alpha=0.7)
plt.title('Salary vs Year and Experience')
plt.xlabel('Year')
plt.ylabel('Average Salary')
plt.legend(title='Experience', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


sns.pairplot(df[['Average Salary', 'Year', 'Experience Level']], hue='Experience Level', diag_kind='kde', palette='bright')
plt.suptitle('Pairplot: Salary, Year and Experience', y=1.02)
plt.show()