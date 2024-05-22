import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import calendar
import glob
import os

files = [
    name.replace("\\", "/")
    for name in glob.glob(r"data\reports\mcwb\**\*.csv", recursive=True)
    if name.split("\\")[-1] in ["jrniftymcwb.csv", "niftynext50_mcwb.csv"]
]

master_df = pd.DataFrame()

for each_file in tqdm(files):
    year = int(each_file.split("/")[3])
    month = each_file.split("/")[4]

    df = pd.read_csv(each_file)
    if df.shape[1] == 1:
        df = pd.read_csv(each_file, header=1)
    elif "Sr. No" in df.columns:
        pass
    else:
        df_full_page = pd.read_csv(each_file).replace("Sr.no.", "Sr. No")

        header = np.where(df_full_page == "Sr. No")[0][0] + 1
        df = pd.read_csv(each_file, header=header)

    df.rename({"Sr.no.": "Sr. No"}, inplace=True, axis=1)

    if pd.isna(df.loc[0, "Sr. No"]):
        df.drop(0, inplace=True)

    # Removing rows with all Null values
    df = df.drop(index=df[df.isna().all(axis=1)].index, axis=0)

    df.reset_index(drop=True, inplace=True)
    df = df.loc[:49]

    # Drop all columns containing all null values
    df = df.drop(labels=df.columns[df.isna().all()], axis=1)

    columns = [
        "Sr. No",
        "Security Symbol",
        "Security Name",
        "Industry",
        "Equity",
        "Market Capitalisation",
        "Weightage",
        "Beta",
        "R2",
        "Volatility",
        "Monthly Return",
        "Avg. Impact Cost",
    ]

    if "Industry" not in df.columns:
        columns.remove("Industry")

    if "Security Name" not in df.columns:
        columns.remove("Security Name")

    if "Unnamed: 10" in df.columns:
        columns = columns + ["Unnamed: 10"]

    df.columns = columns

    if (calendar.month_abbr[:].index(month) <= 5) and (int(year) <= 2009):
        df.loc[:, "Market Capitalisation Type"] = "Total"
    else:
        df.loc[:, "Market Capitalisation Type"] = "Free"

    df.loc[:, "Year"] = year
    df.loc[:, "Month"] = month

    master_df = pd.concat([master_df, df], ignore_index=True)
    del df


os.makedirs("./data/master/", exist_ok=True)
master_df.to_csv("./data/master/NiftyNext50.csv")


for year in range(2009, datetime.now().year):

    for month in range(1, 13):
        if (
            master_df.loc[
                (master_df["Year"] == year)
                & (master_df["Month"] == calendar.month_abbr[month])
            ].shape[0]
            == 0
        ):
            print("Missing Year Month:", year, calendar.month_abbr[month])
