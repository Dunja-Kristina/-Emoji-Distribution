import pandas as pd
import scipy.stats

df = pd.read_csv("/home/dunyxx/Documents/fakultet/3. godina/STAT/projCHAT/podaci.csv")
df2 = pd.DataFrame(df, columns=["Zipf coef.", "Openness to Experience"])
#print(df2.values.tolist())

correlation = df2.corr(method="pearson")
print("KOeficijent korelacije je: ")
print(correlation)

result = scipy.stats.linregress(df2["Zipf coef."], df2["Openness to Experience"])

print(result.rvalue)