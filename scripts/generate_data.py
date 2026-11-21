"""Generate a SYNTHETIC gaming industry dataset for learning purposes.
No real company or official figures are used. Run: python scripts/generate_data.py"""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
n = 300
year = rng.choice(range(2018, 2026), n)
platform = rng.choice(['PC','Console','Mobile'], n, p=[.28,.27,.45])
genre = rng.choice(['Action','Adventure','RPG','Sports','Strategy','Puzzle','Shooter'], n)
region = rng.choice(['Asia-Pacific','North America','Europe','Rest of World'], n, p=[.38,.27,.23,.12])
monet = np.where(platform=='Mobile', rng.choice(['Free-to-Play','Premium','Subscription'], n, p=[.8,.12,.08]),
                 rng.choice(['Free-to-Play','Premium','Subscription'], n, p=[.25,.6,.15]))
price = np.where(monet=='Premium', rng.choice([9.99,19.99,29.99,49.99,59.99], n), 0.0)
marketing = np.clip(rng.gamma(2.0, 4.0, n), 0.5, 60).round(1)
rating = np.clip(rng.normal(3.8, 0.5, n), 1.5, 5).round(1)
plat_w = pd.Series(platform).map({'PC':1.0,'Console':1.3,'Mobile':1.6}).values
gen_w = pd.Series(genre).map({'Action':1.1,'Adventure':0.9,'RPG':1.2,'Sports':1.0,'Strategy':0.8,'Puzzle':0.7,'Shooter':1.4}).values
reg_w = pd.Series(region).map({'Asia-Pacific':1.4,'North America':1.2,'Europe':1.0,'Rest of World':0.6}).values
mon_w = pd.Series(monet).map({'Free-to-Play':1.5,'Premium':1.0,'Subscription':0.9}).values
growth = 1 + 0.08*(year-2018)
players = np.clip(2*plat_w*gen_w*reg_w*growth*(0.5+marketing/10)*np.exp(rng.normal(0,.35,n)), 0.1, 300).round(2)
revenue = np.clip(players*(6+8*(rating-3))*mon_w*0.8*np.exp(rng.normal(0,.3,n)) + price*players*0.3, 1, 5000).round(1)
df = pd.DataFrame({'Game_ID':[f'G{2001+i}' for i in range(n)],'Release_Year':year,'Platform':platform,'Genre':genre,
  'Region':region,'Monetization':monet,'Price_USD':price,'Marketing_Budget_MUSD':marketing,
  'Avg_Rating':rating,'Players_Millions':players,'Revenue_MUSD':revenue})
# Data-quality problems for the cleaning exercise
for col,k in [('Marketing_Budget_MUSD',6),('Avg_Rating',5),('Players_Millions',4),('Revenue_MUSD',4)]:
    df.loc[rng.choice(n,k,replace=False),col] = np.nan
df.loc[11,'Avg_Rating'] = 7.5                      # impossible rating (max is 5)
df.loc[[40,120],'Platform'] = ['mobile','CONSOLE'] # inconsistent text
df = pd.concat([df, df.sample(5, random_state=1)], ignore_index=True)  # duplicates
df.to_csv('data/raw/gaming_industry.csv', index=False)
print(df.shape)
