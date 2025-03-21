# %%
import pandas as pd

from matplotlib import pyplot as plt

df = pd.read_csv('./material_costs.csv', delimiter=',', decimal=",", thousands=".", encoding='utf-8')
df.head(40)

# %%
df = df.iloc[1:]
# Artikelnummer: extract numeric part and symbol
df['article_id'] = df['Artikelnummer'].astype(str).str.extract(r'([\d\.]+)')[0]
df['article_id'] = df['article_id'].str.replace('.', '', regex=False)
df['item_type'] = df['Artikelnummer'].astype(str).str.extract(r'([PEK])')[0]

# Remove Bezeichnung column
df.drop(columns=['Bezeichnung'], inplace=True, errors='ignore')

# Verwendung: split into used_for_child, used_for_men, used_for_women
df['used_for_child'] = df['Verwendung'].apply(lambda x: 1 if 'K' in str(x) else 0)
df['used_for_men'] = df['Verwendung'].apply(lambda x: 1 if 'H' in str(x) else 0)
df['used_for_women'] = df['Verwendung'].apply(lambda x: 1 if 'D' in str(x) else 0)

# Rename and reformat columns
# Startmenge -> start_quantity, remove dots (thousands separator)
df['start_quantity'] = df['Startmenge']

# Startpreis [ € ] -> price_per_part, remove thousand markers and convert comma to dot
df['price_per_part'] = df['Startpreis[€]']

# Lieferkosten [ € ] -> order_price
df['order_price'] = df['Lieferkosten[€]']

# Lieferzeit [Perioden] -> order_duration
df['order_duration'] = df['Lieferzeit[Perioden]']

# rename Lieferzeitabweichung to order_86_deviation and convert to english number format
df['order_86_deviation'] = df['Lieferzeitabweichung']

# calculate order_standard_deviation and drop the original order_86_deviation column
df['order_standard_deviation'] = df['order_86_deviation'] / 1.48
df.drop(columns=['order_86_deviation'], inplace=True)
# Lieferzeitabweichung -> order_86_deviation

# Add discount_quantity and discount_amount for item_type K
df['discount_quantity'] = df.apply(lambda row: row['start_quantity'] if row['item_type'] == 'K' else 0, axis=1)
df['discount_amount'] = df.apply(lambda row: 0.1 if row['item_type'] == 'K' else 0, axis=1)
cols = ['article_id', 'item_type', 'used_for_child', 'used_for_men', 'used_for_women',
        'start_quantity', 'price_per_part', 'order_price', 'order_duration', 'order_standard_deviation',
        'discount_quantity', 'discount_amount']
df = df[cols]
df.to_csv('material_costs_cleaned.csv', index=False, encoding='utf-8')

# %%
df.describe()
# %%
df.head()
# %%
import seaborn as sns

df = pd.read_csv('material_costs_cleaned_edited.csv', encoding='utf-8')
sns.boxplot(y=df['order_duration'])
plt.title('Boxplot of Values')
plt.show()
# %%
import matplotlib.pyplot as plt

df_k = df[df['item_type'] == 'K']
kids_cost = (df_k['price_per_part'] * df_k['quantity_used_for_child']).sum()
men_cost = (df_k['price_per_part'] * df_k['quantity_used_for_men']).sum()
women_cost = (df_k['price_per_part'] * df_k['quantity_used_for_women']).sum()

categories = ['Kids Bikes', 'Men Bikes', 'Women Bikes']
costs = [kids_cost, men_cost, women_cost]

plt.figure()
plt.bar(categories, costs)
plt.ylabel('Material Cost')
plt.title('Material Cost by Product Category')
plt.show()

# %%
start_quantities = df['start_quantity']
summed_usage = (df['quantity_used_for_child'] + df['quantity_used_for_men'] + df['quantity_used_for_women']) / 3

plt.scatter(start_quantities, summed_usage)

# %%
storage_time = start_quantities / summed_usage
plt.boxplot(storage_time)
plt.ylim(0, 2000)
# %%
df.head()
# %%
import matplotlib.pyplot as plt
import numpy as np

# Filter only K counter
df_k = df[df['item_type'] == 'K'].copy()
AVERAGE_PRODUCT_DEMAND = 300
AVERAGE_PRODUCT_PRICE = 200
# Calculate actual demand from the two columns that give the actual usage
df_k['average_demand'] = (df['quantity_used_for_child'] + df['quantity_used_for_men'] + df[
    'quantity_used_for_women']) / 3

# Safety stock is based on variability in order and the actual demand.
# We use a safety factor (z = 1.65) to determine the safety stock.
z = 1.65
df_k['safety_stock_factor'] = z * df_k['order_standard_deviation'] * df_k['average_demand']
df_k['start_safety_stock_factor'] = df_k['start_quantity'] / df_k['average_demand'] / AVERAGE_PRODUCT_DEMAND
# Storage cost depends on the safety stock level and the product value (price_per_part)
df_k['storage_value_factor'] = df_k['safety_stock_factor'] * df_k['price_per_part']
df_k['start_storage_value_factor'] = df_k['start_safety_stock_factor'] * df_k['price_per_part']
# Visualize Safety Stock for each K item
plt.figure(figsize=(12, 5))
width = 0.35
indices = np.arange(len(df_k))
plt.bar(indices - width / 2, df_k['safety_stock_factor'], width, label='Safety Stock Factor')
plt.bar(indices + width / 2, df_k['start_safety_stock_factor'], width, label='Start Safety Stock Factor', color='red')
plt.xlabel('Article ID')
plt.ylabel('Safety Stock per one product')
plt.title('Start Quantities Safety Factor vs new calculated Safety Factor')
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.show()

df_k['safety_store_per_revenue'] = df_k['storage_value_factor'] / AVERAGE_PRODUCT_PRICE

plt.figure(figsize=(12, 5))
width = 0.35
indices = np.arange(len(df_k))
plt.bar(indices - width / 2, df_k['safety_store_per_revenue'], width, label='Safety Stock Factor')
plt.bar(indices + width / 2, df_k['start_storage_value_factor'] / AVERAGE_PRODUCT_PRICE, width,
        label='Start Safety Stock Factor', color='red')
plt.xlabel('Article ID')
plt.ylabel('Storage Value per one product produced / revenue per product')
plt.title('Safety Storage value as revenue factor (200) for K Items in regards to the summed demand')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
safety_stock_per_revenue = df_k['safety_store_per_revenue'].sum()
# %%
AVERAGE_REVENUE = AVERAGE_PRODUCT_DEMAND * AVERAGE_PRODUCT_PRICE

stock_value = safety_stock_per_revenue * AVERAGE_REVENUE

stock_value
# %%
import math


def order_duration_safety_factor(order_duration):
    return max(1.0, math.sqrt(order_duration))


# %%
df_k['adjusted_safety_stock_linear'] = df_k['safety_stock_factor'] * df_k['order_duration']
df_k['adjusted_safety_stock_sqrt'] = df_k['safety_stock_factor'] * df_k['order_duration'].apply(
    order_duration_safety_factor)

indices = np.arange(len(df_k))
width = 0.35

plt.figure(figsize=(12, 5))

# 2. Scatter plot: Order Cost vs Order Duration
plt.scatter(df_k['order_duration'], df_k['order_price'], color='green')
for i, txt in enumerate(df_k['article_id']):
    plt.annotate(txt, (df_k['order_duration'].iloc[i], df_k['order_price'].iloc[i]))
plt.xlabel('Order Duration')
plt.ylabel('Order Price')
plt.title('Order Cost vs Order Duration')
plt.show()

plt.figure(figsize=(12, 5))

# 4. Adjusted Safety Stock (including order duration)
plt.bar(indices, df_k['adjusted_safety_stock_sqrt'], color='purple')
plt.xlabel('Article ID')
plt.ylabel('Adjusted Safety Stock')
plt.title('Adjusted Safety Stock (Safety Factor * Order Duration)')
plt.xticks(indices)
plt.tight_layout()
plt.show()

# %% md
# Durchnittlische Belastung pro Arbeitsplatz also wie eng dort die Kapazitäten prinzipiell sind.
# kritischer Pfad, längster Pfad. Bei den Eigenerzeugnissen weniger auf Lager halten von Teilen die schneller produziert werden können.
# 
# 
# 
# %%
