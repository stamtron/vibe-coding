##############################################################################
# marketing_analysis.py
# Written in Notepad, run from terminal: python marketing_analysis.py
# No IDE, no autocomplete, no linting — just you and the docs
##############################################################################

import csv
import sys
import os

# We need matplotlib — hope we remembered to pip install it
# $ pip install matplotlib
# (no virtual environments, no requirements.txt, just global pip)
import matplotlib
matplotlib.use('Agg')  # because we're running from terminal, no GUI
import matplotlib.pyplot as plt

##############################################################################
# STEP 1: Read the CSV file manually with the csv module
# No pandas — most of us didn't even know pandas existed yet
##############################################################################

filename = "data/marketing_campaign.csv"

# Check if file exists (learned this the hard way after a FileNotFoundError)
if not os.path.exists(filename):
    print("ERROR: Cannot find " + filename)
    print("Make sure you're running this from the right directory!")
    sys.exit(1)

# Read all rows into a list of dictionaries
data = []
f = open(filename, 'r')
reader = csv.DictReader(f)
for row in reader:
    data.append(row)
f.close()

print("Loaded " + str(len(data)) + " rows from " + filename)

##############################################################################
# STEP 2: Calculate total spend and revenue per channel
# No groupby, no aggregation functions — just loops and dictionaries
##############################################################################

channel_spend = {}
channel_revenue = {}
channel_clicks = {}
channel_impressions = {}

for row in data:
    channel = row['channel']

    # Everything from CSV comes as strings — must convert manually
    spend = float(row['spend'])
    revenue = float(row['revenue'])
    clicks = int(row['clicks'])
    impressions = int(row['impressions'])

    # Initialize if we haven't seen this channel before
    if channel not in channel_spend:
        channel_spend[channel] = 0.0
        channel_revenue[channel] = 0.0
        channel_clicks[channel] = 0
        channel_impressions[channel] = 0

    channel_spend[channel] = channel_spend[channel] + spend
    channel_revenue[channel] = channel_revenue[channel] + revenue
    channel_clicks[channel] = channel_clicks[channel] + clicks
    channel_impressions[channel] = channel_impressions[channel] + impressions

# Print results to terminal
print("")
print("=" * 60)
print("MARKETING CAMPAIGN ANALYSIS")
print("=" * 60)
print("")
print("{:<12} {:>12} {:>12} {:>8}".format("Channel", "Spend ($)", "Revenue ($)", "ROI (%)"))
print("-" * 50)

for channel in sorted(channel_spend.keys()):
    spend = channel_spend[channel]
    revenue = channel_revenue[channel]
    if spend > 0:
        roi = ((revenue - spend) / spend) * 100
    else:
        roi = 0
    print("{:<12} {:>12,.2f} {:>12,.2f} {:>7.1f}%".format(
        channel, spend, revenue, roi
    ))

##############################################################################
# STEP 3: Calculate monthly revenue for time series
# Date parsing without datetime — just string splitting
##############################################################################

monthly_revenue = {}

for row in data:
    # Parse date manually: "2023-01-15" -> extract year-month
    date_str = row['date']
    parts = date_str.split('-')
    year = parts[0]
    month = parts[1]
    year_month = year + '-' + month

    revenue = float(row['revenue'])

    if year_month not in monthly_revenue:
        monthly_revenue[year_month] = 0.0
    monthly_revenue[year_month] = monthly_revenue[year_month] + revenue

# Sort the months (string sorting works for YYYY-MM format, thankfully)
sorted_months = sorted(monthly_revenue.keys())
month_values = []
for m in sorted_months:
    month_values.append(monthly_revenue[m])

##############################################################################
# STEP 4: Create plots with matplotlib
# Every single property set manually — no style sheets, no themes
##############################################################################

# Make sure output directory exists
if not os.path.exists('plots'):
    os.makedirs('plots')

# --- Plot 1: Bar chart of spend vs revenue by channel ---

channels_list = sorted(channel_spend.keys())
spend_values = []
revenue_values = []
for ch in channels_list:
    spend_values.append(channel_spend[ch])
    revenue_values.append(channel_revenue[ch])

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)

# Calculate bar positions manually
bar_width = 0.35
x_positions = []
for i in range(len(channels_list)):
    x_positions.append(i)

x_positions_revenue = []
for i in range(len(channels_list)):
    x_positions_revenue.append(i + bar_width)

ax.bar(x_positions, spend_values, bar_width, color='#cc4444', label='Spend')
ax.bar(x_positions_revenue, revenue_values, bar_width, color='#44aa44', label='Revenue')

# Set labels manually
ax.set_xlabel('Channel', fontsize=12)
ax.set_ylabel('Amount ($)', fontsize=12)
ax.set_title('Marketing Spend vs Revenue by Channel', fontsize=14)
ax.set_xticks([i + bar_width/2 for i in range(len(channels_list))])
ax.set_xticklabels(channels_list)
ax.legend()

# Add grid manually
ax.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('plots/era1_spend_vs_revenue.png', dpi=100)
plt.close()
print("")
print("Saved: plots/era1_spend_vs_revenue.png")

# --- Plot 2: Line chart of monthly revenue ---

fig2 = plt.figure(figsize=(12, 5))
ax2 = fig2.add_subplot(111)

x_positions_months = []
for i in range(len(sorted_months)):
    x_positions_months.append(i)

ax2.plot(x_positions_months, month_values, color='#2266cc', linewidth=2, marker='o', markersize=4)
ax2.set_xlabel('Month', fontsize=12)
ax2.set_ylabel('Revenue ($)', fontsize=12)
ax2.set_title('Monthly Revenue Trend', fontsize=14)

# Rotate x labels — figured this out after 20 minutes of googling
ax2.set_xticks(x_positions_months)
ax2.set_xticklabels(sorted_months, rotation=45, ha='right')

ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('plots/era1_monthly_revenue.png', dpi=100)
plt.close()
print("Saved: plots/era1_monthly_revenue.png")

# --- Plot 3: Click-through rate by channel ---

fig3 = plt.figure(figsize=(8, 6))
ax3 = fig3.add_subplot(111)

ctr_values = []
for ch in channels_list:
    if channel_impressions[ch] > 0:
        ctr = (float(channel_clicks[ch]) / float(channel_impressions[ch])) * 100
    else:
        ctr = 0
    ctr_values.append(ctr)

colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
ax3.bar(channels_list, ctr_values, color=colors)
ax3.set_xlabel('Channel', fontsize=12)
ax3.set_ylabel('CTR (%)', fontsize=12)
ax3.set_title('Click-Through Rate by Channel', fontsize=14)
ax3.grid(True, axis='y', alpha=0.3)

# Add value labels on bars — took forever to figure out the positioning
for i in range(len(channels_list)):
    ax3.text(i, ctr_values[i] + 0.1, "{:.2f}%".format(ctr_values[i]),
             ha='center', va='bottom', fontsize=11)

plt.tight_layout()
plt.savefig('plots/era1_ctr_by_channel.png', dpi=100)
plt.close()
print("Saved: plots/era1_ctr_by_channel.png")

print("")
print("Done! Check the plots/ directory for output.")
print("Total lines of code: ~160 (and counting...)")
