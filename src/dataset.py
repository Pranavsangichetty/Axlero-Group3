import pandas as pd

DATA_PATH = "data/raw/online_retail_II.csv"


def inspect_dataset():
    print("Loading complete dataset...")

    df = pd.read_csv(DATA_PATH)

    print("\n========== DATASET OVERVIEW ==========")
    print("Total Rows:", df.shape[0])
    print("Total Columns:", df.shape[1])

    print("\n========== COLUMN NAMES ==========")
    print(df.columns.tolist())

    print("\n========== FIRST 5 RECORDS ==========")
    print(df.head())

    print("\n========== DATA TYPES ==========")
    print(df.dtypes)

    print("\n========== MISSING VALUES ==========")
    print(df.isnull().sum())

    print("\n========== DUPLICATE RECORDS ==========")
    print(df.duplicated().sum())


if __name__ == "__main__":
    inspect_dataset()
