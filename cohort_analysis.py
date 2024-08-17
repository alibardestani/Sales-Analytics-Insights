import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('preprocessed_sales.csv')

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

df['MonthYear'] = df['InvoiceDate'].dt.to_period('M').dt.start_time
df_first_purchase = df.groupby('CustomerId')['MonthYear'].min().reset_index()
df_first_purchase.columns = ['CustomerId', 'FirstPurchaseMonth']

df = pd.merge(df, df_first_purchase, on='CustomerId')

# Calculate CohortIndex
df['CohortIndex'] = ((df['MonthYear'].dt.year - df['FirstPurchaseMonth'].dt.year) * 12 + 
                     (df['MonthYear'].dt.month - df['FirstPurchaseMonth'].dt.month)) + 1

# Create a retention matrix
retention = df.groupby(['FirstPurchaseMonth', 'CohortIndex'])['CustomerId'].nunique().unstack().divide(df.groupby('FirstPurchaseMonth')['CustomerId'].nunique(), axis=0) * 100

# Plot the retention matrix as a heatmap
plt.figure(figsize=(15, 8))
sns.heatmap(retention, annot=True, fmt='.0f', cmap='BuGn', vmin=0, vmax=50)
plt.title('Customer Retention Rates')
plt.ylabel('First Purchase Month')
plt.yticks(ticks=np.arange(len(retention.index)) + 0.5, labels=retention.index.strftime('%Y-%m'))
plt.xticks(ticks=np.arange(1, retention.columns.size + 1), labels=range(1, retention.columns.size + 1))
plt.show()
