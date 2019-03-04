import pandas as pd
import pandas_profiling

csv = 'data/data.csv'


def main():
    df = pd.read_csv(csv)
    profile = pandas_profiling.ProfileReport(df)
    profile.to_file("data/profile_" + csv[5:-4] + ".html")


if __name__ == "__main__": main()
