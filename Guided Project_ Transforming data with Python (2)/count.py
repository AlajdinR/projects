import read
import collections
df = read.load_data()
s = ""
l = df["headline"].tolist()
for string in l:
    s += str(string) + " "
res = s.lower().split(' ')
c = collections.Counter(res)
print(c.most_common(100))
