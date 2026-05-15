import csv
import random
import math
from datetime import datetime, timedelta

random.seed(42)

channels = {
    "Email": {"base_impressions": 15000, "ctr": 0.035, "conv_rate": 0.08, "cpc": 0.50},
    "Social": {"base_impressions": 50000, "ctr": 0.012, "conv_rate": 0.03, "cpc": 1.20},
    "Search": {"base_impressions": 8000, "ctr": 0.065, "conv_rate": 0.12, "cpc": 2.50},
    "Display": {"base_impressions": 80000, "ctr": 0.004, "conv_rate": 0.015, "cpc": 0.30},
}

campaign_names = {
    "Email": ["Newsletter_Weekly", "Promo_Flash_Sale", "Onboarding_Drip", "Re-engagement_Win-back"],
    "Social": ["Brand_Awareness_FB", "Product_Launch_IG", "Retargeting_TikTok", "Influencer_Collab"],
    "Search": ["Brand_Keywords", "Competitor_Terms", "Product_Category", "Long_Tail_Queries"],
    "Display": ["Banner_Homepage", "Remarketing_Cart", "Lookalike_Audience", "Contextual_Targeting"],
}

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
rows = []

current = start_date
while current <= end_date:
    for channel, params in channels.items():
        day_of_year = current.timetuple().tm_yday
        seasonality = 1 + 0.3 * math.sin(2 * math.pi * (day_of_year - 30) / 365)

        if current.month in [11, 12]:
            seasonality *= 1.4
        if current.weekday() >= 5:
            seasonality *= 0.7

        impressions = int(params["base_impressions"] * seasonality * random.uniform(0.7, 1.3) / 7)
        clicks = int(impressions * params["ctr"] * random.uniform(0.6, 1.4))
        conversions = int(clicks * params["conv_rate"] * random.uniform(0.5, 1.5))
        spend = round(clicks * params["cpc"] * random.uniform(0.8, 1.2), 2)
        revenue = round(conversions * random.uniform(25, 150), 2)

        if random.random() < 0.02:
            impressions = int(impressions * random.uniform(2.5, 4.0))
            clicks = int(clicks * random.uniform(2.0, 3.0))

        campaign = random.choice(campaign_names[channel])

        rows.append({
            "date": current.strftime("%Y-%m-%d"),
            "channel": channel,
            "campaign_name": campaign,
            "impressions": max(impressions, 0),
            "clicks": max(clicks, 0),
            "conversions": max(conversions, 0),
            "spend": max(spend, 0),
            "revenue": max(revenue, 0),
        })

    current += timedelta(days=random.choice([3, 4, 3, 4]))

random.shuffle(rows)
rows.sort(key=lambda r: r["date"])

with open("data/marketing_campaign.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["date", "channel", "campaign_name", "impressions", "clicks", "conversions", "spend", "revenue"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows")
