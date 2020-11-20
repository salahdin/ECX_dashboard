import pandas as pd

df = pd.read_csv('rptCoffee.csv')
df1 = df[df['Symbol'].str.contains('LUBM3')]
print(df1.index)
