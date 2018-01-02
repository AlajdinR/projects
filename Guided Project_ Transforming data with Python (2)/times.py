import read
import dateutil

df = read.load_data()

def get_hr(n):
    temp = dateutil.parser.parse(n)
    n = temp.hour
    return n

df["sub_hrs"] = df["submission_time"].apply(get_hr)
print(df["sub_hrs"].value_counts())

