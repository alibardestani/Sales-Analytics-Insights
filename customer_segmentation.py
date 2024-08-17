import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv('preprocessed_sales.csv')

last_day = pd.to_datetime(df['InvoiceDate']).max() + timedelta(days=1)

# Recency, Frequency, and Monetary (RFM) calculations
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df_customer_segments = df.groupby('CustomerId').agg({
    'InvoiceDate': 'max',
    'InvoiceNumber': 'nunique',
    'UnitPrice': lambda x: (x * df.loc[x.index, 'Quantity']).sum()
}).reset_index()

df_customer_segments['Recency'] = (last_day - df_customer_segments['InvoiceDate']).dt.days
df_customer_segments.columns = ['CustomerId', 'LastInvoiceDate', 'Frequency', 'MonetaryValue']

# Define quartiles for R, F, M
qR = df_customer_segments['Recency'].quantile([0.25, 0.50, 0.75])
qF = df_customer_segments['Frequency'].quantile([0.25, 0.50, 0.75])
qM = df_customer_segments['MonetaryValue'].quantile([0.25, 0.50, 0.75])

# Assign RFM scores
df_customer_segments['R'] = pd.cut(df_customer_segments['Recency'], bins=[-np.inf, qR[0.25], qR[0.50], qR[0.75], np.inf], labels=[1, 2, 3, 4])
df_customer_segments['F'] = pd.cut(df_customer_segments['Frequency'], bins=[-np.inf, qF[0.25], qF[0.50], qF[0.75], np.inf], labels=[1, 2, 3, 4])
df_customer_segments['M'] = pd.cut(df_customer_segments['MonetaryValue'], bins=[-np.inf, qM[0.25], qM[0.50], qM[0.75], np.inf], labels=[1, 2, 3, 4])

df_customer_segments['RFM'] = df_customer_segments['R'].astype(str) + df_customer_segments['F'].astype(str) + df_customer_segments['M'].astype(str)

# Define customer segments
def classify_customer(rfm):
    if rfm == '144':
        return 'Best'
    elif rfm == '344':
        return 'AlmostLost'
    elif rfm == '444':
        return 'LostBigSpenders'
    elif rfm == '441':
        return 'LostCheap'
    elif rfm[1] == '4':  # X4X pattern
        return 'Loyal'
    elif rfm[2] == '4':  # XX4 pattern
        return 'BigSpenders'
    else:
        return 'Normal'

df_customer_segments['Segment'] = df_customer_segments['RFM'].apply(classify_customer)
