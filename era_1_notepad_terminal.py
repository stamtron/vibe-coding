# marketing_analysis.py — written in Notepad, run from terminal
# No IDE, no autocomplete, no linting — just you and the Python docs

import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

filename = "data/marketing_campaign.csv"
if not os.path.exists(filename):
    print("ERROR: Cannot find " + filename)
    exit(1)

df = pd.read_csv(filename)

print("Loaded " + str(len(df)) + " rows")

channel_summary = df.groupby('channel').agg(
    spend=('spend', 'sum'),
    revenue=('revenue', 'sum')
).sort_index()

channel_summary['roi'] = ((channel_summary['revenue'] - channel_summary['spend']) / channel_summary['spend']) * 100

print("")
print("=" * 50)
print("MARKETING CAMPAIGN ANALYSIS")
print("=" * 50)
print("{:<12} {:>12} {:>12} {:>8}".format("Channel", "Spend ($)", "Revenue ($)", "ROI (%)"))
print("-" * 50)

for ch, row in channel_summary.iterrows():
    print("{:<12} {:>12,.2f} {:>12,.2f} {:>7.1f}%".format(ch, row['spend'], row['revenue'], row['roi']))

df['year_month'] = pd.to_datetime(df['date']).dt.to_period('M')
monthly_revenue = df.groupby('year_month')['revenue'].sum()

sorted_months = [str(m) for m in monthly_revenue.index]
month_values = monthly_revenue.values.tolist()

if not os.path.exists('plots'):
    os.makedirs('plots')

channels_list = channel_summary.index.tolist()
spend_vals = channel_summary['spend'].tolist()
rev_vals = channel_summary['revenue'].tolist()

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)
bar_width = 0.35
x = list(range(len(channels_list)))
ax.bar(x, spend_vals, bar_width, color='#cc4444', label='Spend')
ax.bar([i + bar_width for i in x], rev_vals, bar_width, color='#44aa44', label='Revenue')
ax.set_ylabel('Amount ($)')
ax.set_title('Spend vs Revenue by Channel')
ax.set_xticks([i + bar_width/2 for i in x])
ax.set_xticklabels(channels_list)
ax.legend()
plt.tight_layout()
plt.savefig('plots/era1_spend_vs_revenue.png', dpi=100)
plt.close()

print("\nDone! Plot saved to plots/")
