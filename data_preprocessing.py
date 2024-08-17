import pandas as pd
import numpy as np

df = pd.read_excel('sales.xlsx')

df_no_missing_CustomerId = df.dropna(subset=['CustomerId'])

df_no_duplicate = df_no_missing_CustomerId.drop_duplicates()

df_no_missing_price = df_no_duplicate[df_no_duplicate['UnitPrice'] > 0]

# Calculate the percentage of cancelled orders
percentage_cancelled = df_no_missing_price.drop_duplicates(subset=['InvoiceNumber'], keep='last')
cancelled_orders = percentage_cancelled[percentage_cancelled['InvoiceNumber'].str.startswith('C')]
percentage_cancelled_orders = round(len(cancelled_orders) / len(percentage_cancelled) * 100, 2)

# Identify top 5 customers by cancellation count
top_cancelling_customers = df_no_missing_price[df_no_missing_price['InvoiceNumber'].str.startswith('C', na=False)]
top_cancelling_customers = top_cancelling_customers.drop_duplicates(subset=['CustomerId', 'InvoiceNumber'])
top_cancelling_customers = top_cancelling_customers.groupby('CustomerId').size().nlargest(5).index.astype(str).tolist()

# Remove cancelled invoices
df_no_canceled_invoice = df_no_missing_price[~df_no_missing_price['InvoiceNumber'].str.startswith('C')]

df_no_canceled_invoice.to_csv("preprocessed_sales.csv", index=False)

# Store unique remaining invoices
remaining_invoices = pd.Series(df_no_canceled_invoice['InvoiceNumber'].unique())
