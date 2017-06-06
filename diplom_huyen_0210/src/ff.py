import pandas as pd
df = pd.DataFrame({'foo':list('ABCdkahdgjkfdagjg')})
print(df)
print(df.ix[df.index.min(), 'foo'])
print(df.ix[df.index.max(), 'foo'])
# print(df.index.min())
# print(df.index.max())