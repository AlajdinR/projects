import read

df = read.load_data()

#print(df["url"].value_counts())
def replace(n):
    temp = str(n).split(".")
    if len(temp)>2 and temp[0] != "":
        del temp[0]
    n = ".".join(temp)
    return n
df["rob_url"]=df["url"].apply(replace)
domains = df["rob_url"].value_counts()

for name, row in domains.items():
    print("{0}: {1}".format(name, row))
