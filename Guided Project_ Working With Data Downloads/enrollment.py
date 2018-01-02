import pandas as pd

if __name__ == "__main__":
    data = pd.read_csv("data/CRDC2013_14.csv", encoding="Latin-1")
    total_enrollment = data["TOT_ENR_M"] + data["TOT_ENR_F"]
    all_enrollment = total_enrollment.sum()
    #print(total_enrollment)
    print(all_enrollment)
    