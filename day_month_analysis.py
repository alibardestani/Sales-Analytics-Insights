import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('preprocessed_sales.csv')

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

df['DayName'] = df['InvoiceDate'].dt.day_name()

days_df = df.groupby('DayName')['InvoiceNumber'].nunique().reset_index(name='counts')

# Define the day order for plotting
day_order = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
day_name_map = {
    'Monday': 'Mon',
    'Tuesday': 'Tue',
    'Wednesday': 'Wed',
    'Thursday': 'Thur',
    'Friday': 'Fri',
    'Saturday': 'Sat',
    'Sunday': 'Sun'
}

# Map and sort the days
days_df['DayName'] = pd.Categorical(days_df['DayName'].map(day_name_map), categories=day_order, ordered=True)
days_df = days_df.sort_values('DayName').reset_index(drop=True)

plt.figure(figsize=(15, 6))
plt.bar(days_df['DayName'], days_df['counts'], color='lime')
plt.title("Number of Orders by Day", color="green", fontsize=15)
plt.xlabel('Day', color='lightseagreen', fontsize=15)
plt.ylabel("Number of Orders", color='lightseagreen', fontsize=15)
plt.xticks(rotation=0, fontsize=15)
plt.show()

# Monthly sales analysis
df['MonthYear'] = df['InvoiceDate'].dt.to_period('M').dt.start_time
df['Sales'] = df['UnitPrice'] * df['Quantity']
Months_df = df.groupby(df['MonthYear'].dt.strftime('%b_%Y'))['Sales'].sum().reset_index()

month_order = ['Dec_2009','Jan_2010',"Feb_2010","Mar_2010","Apr_2010","May_2010","Jun_2010",
               "Jul_2010","Aug_2010","Sep_2010","Oct_2010","Nov_2010","Dec_2010"]
Months_df['MonthsName'] = pd.Categorical(Months_df['MonthYear'], categories=month_order, ordered=True)
Months_df = Months_df.sort_values('MonthsName').reset_index(drop=True)

plt.figure(figsize=(15, 6))
plt.bar(Months_df['MonthsName'], Months_df['Sales'], color='darkkhaki')
plt.title("Sales by Month", color="cadetblue", fontsize=15)
plt.xlabel('Month', color='orange', fontsize=15)
plt.ylabel('Sales Amount', color='orange', fontsize=15)
plt.xticks(rotation=45, fontsize=13)
plt.show()
