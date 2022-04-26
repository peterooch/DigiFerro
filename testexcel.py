import pandas as pd

df = pd.read_excel('History.xlsx')
x = list((df.itertuples()))[0]
print(x[2])