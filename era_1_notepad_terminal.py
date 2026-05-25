# marketing_analysis.py — written in Notepad, run from terminal
# No IDE, no autocomplete, no linting — just you and the Python docs

import csv
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

filename = "data/marketing_campaign.csv"
if not os.path.exists(filename):
    print("ERROR: Cannot find " + filename)
    exit(1)

data = []
f = open(filename, 'r')
reader = csv.DictReader(f)
for row in reader:
    data.append(row)
f.close()

print("Loaded " + str(len(data)) + " rows")

channel_spend = {}
channel_revenue = {}

for row in data:
    ch = row['channel']
    spend = float(row['spend'])
    revenue = float(row['revenue'])

    if ch not in channel_spend:
        channel_spend[ch] = 0.0
        channel_revenue[ch] = 0.0

    channel_spend[ch] = channel_spend[ch] + spend
    channel_revenue[ch] = channel_revenue[ch] + revenue

print("")
print("=" * 50)
print("MARKETING CAMPAIGN ANALYSIS")
print("=" * 50)
print("{:<12} {:>12} {:>12} {:>8}".format("Channel", "Spend ($)", "Revenue ($)", "ROI (%)"))
print("-" * 50)

for ch in sorted(channel_spend.keys()):
    s = channel_spend[ch]
    r = channel_revenue[ch]
    roi = ((r - s) / s) * 100 if s > 0 else 0
    print("{:<12} {:>12,.2f} {:>12,.2f} {:>7.1f}%".format(ch, s, r, roi))

monthly_revenue = {}
for row in data:
    parts = row['date'].split('-')
    ym = parts[0] + '-' + parts[1]
    if ym not in monthly_revenue:
        monthly_revenue[ym] = 0.0
    monthly_revenue[ym] += float(row['revenue'])

sorted_months = sorted(monthly_revenue.keys())
month_values = [monthly_revenue[m] for m in sorted_months]

if not os.path.exists('plots'):
    os.makedirs('plots')

channels_list = sorted(channel_spend.keys())
spend_vals = [channel_spend[ch] for ch in channels_list]
rev_vals = [channel_revenue[ch] for ch in channels_list]

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
