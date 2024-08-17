import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('preprocessed_sales.csv')

df_copy = df[df['Country'] != 'United Kingdom']

# Calculate sales amount per country
df_copy['SalesAmount'] = df_copy['Quantity'] * df_copy['UnitPrice']
country_data = df_copy.groupby('Country').agg({'SalesAmount': 'sum', 'CustomerId': 'nunique'}).reset_index()
country_data.columns = ['Country', 'SalesAmount', 'CustomerCount']

qSA = country_data['SalesAmount'].quantile(0.75)
qCC = country_data['CustomerCount'].quantile(0.75)

# Classify countries based on sales and customer count
def classify_country(row):
    if row['SalesAmount'] > qSA and row['CustomerCount'] > qCC:
        return 'Highest customer & revenue'
    elif row['SalesAmount'] < qSA and row['CustomerCount'] > qCC:
        return 'High customer & low revenue'
    elif row['SalesAmount'] > qSA and row['CustomerCount'] < qCC:
        return 'High revenue & low customer'
    else:
        return 'Low customer & revenue'

country_data['Group'] = country_data.apply(classify_country, axis=1)

plt.figure(figsize=(10, 10))
colors = {
    'Highest customer & revenue': 'red',
    'High customer & low revenue': 'blue',
    'High revenue & low customer': 'green',
    'Low customer & revenue': 'cyan'
}

for group, color in colors.items():
    subset = country_data[country_data['Group'] == group]
    plt.scatter(subset['SalesAmount'], subset['CustomerCount'], s=20, color=color, label=group)

plt.title('Market Study', fontsize=18)
plt.xlabel('Sales Amount', fontsize=16)
plt.ylabel('Number of Customers', fontsize=16)

# Annotate specific countries
for country in ['France', 'Spain', 'Netherlands']:
    subset = country_data[country_data['Country'] == country]
    for _, row in subset.iterrows():
        plt.text(row['SalesAmount'], row['CustomerCount'] + 0.5, row['Country'], fontsize=15, ha='center')

plt.legend(title='Group', title_fontsize=16, fontsize=14, frameon=True, facecolor='silver')
plt.show()
