import read
df = read.load_data()
s = ""
for string in df["headline"].values:
    s += string
res = s.lower().split(' ')
