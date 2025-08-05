# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 2025

@author: KeeganMurphy
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# Loading Files
# =============================================================================

# Load the orders data
orders_data = pd.read_excel('orders.xlsx')

# Load the customers data
customers_data = pd.read_excel('customers.xlsx')

# Load the order payments data
order_payments_data = pd.read_excel('order_payment.xlsx')

# =============================================================================
# Describing the Data
# =============================================================================

orders_data.info()
customers_data.info()
order_payments_data.info()
# noticed some missing data / null values

# =============================================================================
# Handling the Missing Data
# =============================================================================

# Check for missing data in the orders data
orders_data.isnull().sum()
order_payments_data.isnull().sum()
customers_data.isnull().sum()

# Filling in the missing values in orders with defult value
orders_data2 = orders_data.fillna('N/A')
# Check if there are null values in orders_data2
orders_data2.isnull().sum()

# Drop rows with missing values in order_payments_data
order_payments_data = order_payments_data.dropna()
# Check if there are null values in order_payments_data
order_payments_data.isnull().sum()

# =============================================================================
# Checking & Removing Duplicate Data
# =============================================================================

# Check for duplicates in orders data
orders_data.duplicated().sum()
# Reomve duplicats form orders data
orders_data = orders_data.drop_duplicates()

# Check for duplicates in order_payments_data
order_payments_data.duplicated().sum()
# Reomve duplicats form order_payments_data
order_payments_data = order_payments_data.drop_duplicates()

# Check for duplicates in customers_data
customers_data.duplicated().sum() # No duplicates

# =============================================================================
# Filtering the Data
# =============================================================================

# Select a subset of the orders based on the order status
invoiced_orders_data = orders_data[orders_data['order_status'] == 'invoiced']
# Reset the index
invoiced_orders_data = invoiced_orders_data.reset_index(drop=True)

# Select a subset of the payments data where payment type is = Credit Card and pmt value > 1000
credit_card_payments_data = order_payments_data[
    (order_payments_data['payment_type'] == 'credit_card') & 
    (order_payments_data['payment_value'] > 1000)
    ]
# Reset the index
credit_card_payments_data = credit_card_payments_data.reset_index(drop=True)

# Select a subset of customers based on customer state = SP
customer_state_SP = customers_data[customers_data['customer_state'] == 'SP']

# =============================================================================
# Merge and Join Dataframes
# =============================================================================

# Merge orders data with paymetns data on order_id column
merged_data = pd.merge(orders_data, order_payments_data, on='order_id') 

# Join the merged data with customer data on customer_id column
joined_data = pd.merge(merged_data, customers_data, on='customer_id')

# =============================================================================
# Data Visualization
# =============================================================================

# Create a field called month_year from order_purchase_timestamp
joined_data['month_year'] = joined_data['order_purchase_timestamp'].dt.to_period('M')
joined_data['week_year'] = joined_data['order_purchase_timestamp'].dt.to_period('W')
joined_data['year'] = joined_data['order_purchase_timestamp'].dt.to_period('Y')

# Plot prep
grouped_data = joined_data.groupby('month_year')['payment_value'].sum()
grouped_data = grouped_data.reset_index()
# Convert month_year from period into string
grouped_data['month_year'] = grouped_data['month_year'].astype(str)

# Creating a Plot
plt.plot(grouped_data['month_year'], grouped_data['payment_value'], color='green', marker='o')

# Editing Plot
plt.ticklabel_format(useOffset=False, style='plain', axis='y')
plt.xlabel('Month and Year')
plt.ylabel('Payment Value')
plt.title('Payment Value by Month and Year')
plt.xticks(rotation = 90, fontsize=8)
plt.yticks(fontsize=8)


# Scatter Plot

# Create the DataFrame
scatter_df = joined_data.groupby('customer_unique_id').agg({'payment_value' : 'sum', 'payment_installments' : 'sum'})

# Creating scatterplot
plt.scatter(scatter_df['payment_value'],scatter_df['payment_installments'], color='red')
plt.xlabel('Payment Value')
plt.ylabel('Payment Installments')
plt.title('Payment Value vs Installments by Customer')
plt.show()


# Same scatterplot but using Seaborn
sns.set_theme(style='darkgrid') #whitegrid, darkgrid, dark, white

sns.scatterplot(data=scatter_df, x='payment_value', y='payment_installments')
plt.xlabel('Payment Value')
plt.ylabel('Payment Installments')
plt.title('Payment Value vs Installments by Customer')
plt.show()


# Creating a Bar Chart
bar_chart_df = joined_data.groupby(['payment_type', 'month_year'])['payment_value'].sum()
bar_chart_df = bar_chart_df.reset_index()

pivot_data = bar_chart_df.pivot(index='month_year', columns='payment_type', values='payment_value')

pivot_data.plot(kind='bar', stacked='True')
plt.ticklabel_format(useOffset=False, style='plain', axis='y')
plt.ylabel('Month of Payment')
plt.xlabel('Payment Value')
plt.title('Payment per Payment Type by Month')


# Creating a Box Plot
payment_values = joined_data['payment_value']
payment_types = joined_data['payment_type']

# Creating a seperate box plot per payment type
plt.boxplot([payment_values[payment_types == 'credit_card'],
             payment_values[payment_types == 'boleto'],
             payment_values[payment_types == 'voucher'],
             payment_values[payment_types == 'debit_card']],
            labels = ['Credit Card','Boleto','Voucher','Debit Card']
            )

# Set lables and titles
plt.ylabel('Payment Value')
plt.xlabel('Payment Type')
plt.title('Box Plot showing Payment Value ranges by Payment Type')
plt.show()


# Creating a Subpolt (3 plots in 1)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10,10))

# ax1 Boxplot
ax1.boxplot([payment_values[payment_types == 'credit_card'],
             payment_values[payment_types == 'boleto'],
             payment_values[payment_types == 'voucher'],
             payment_values[payment_types == 'debit_card']],
            labels = ['Credit Card','Boleto','Voucher','Debit Card']
            )
ax1.set_ylabel('Payment Value')
ax1.set_xlabel('Payment Type')
ax1.set_title('Box Plot showing Payment Value ranges by Payment Type')

# ax2 Stacked Bar Chart
pivot_data.plot(kind='bar', stacked='True', ax=ax2)
ax2.ticklabel_format(useOffset=False, style='plain', axis='y')
ax2.set_ylabel('Month of Payment')
ax2.set_xlabel('Payment Value')
ax2.set_title('Payment per Payment Type by Month')

# ax3 Scatter Plot
ax3.scatter(scatter_df['payment_value'],scatter_df['payment_installments'], color='red')
ax3.set_xlabel('Payment Value')
ax3.set_ylabel('Payment Installments')
ax3.set_title('Payment Value vs Installments by Customer')

fig.tight_layout() # adjust the spacing

plt.savefig('my_plot.png')





















