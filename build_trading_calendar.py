import calendar
import pandas as pd

# Create the empty calendar
START = "2009-01-01"
END = "2024-12-31"

if __name__ == "__main__":
    df = pd.DataFrame({"Date": pd.date_range(START, END)})
    df["Day"] = df.Date.dt.day_name()

    # Reading Trading Holidays
    df_holidays = pd.read_csv("data\master\IndiaTradingHolidays.csv").drop(
        "Holiday", axis=1
    )
    df_holidays.Date = pd.to_datetime(df_holidays.Date)
    df_holidays["Trading Day"] = 0

    # merging Trading Holidays with calendar
    df = df.merge(df_holidays, how="left", on=["Date", "Day"])
    df.loc[df["Day"].apply(lambda x: x in ["Saturday", "Sunday"]), "Trading Day"] = (
        0  # Marking Sat and Sun as Holidays
    )

    # Denoting rest of days as Trading Days
    df.loc[df["Trading Day"].isna(), "Trading Day"] = 1

    df.to_csv("data\master\IndiaTradingCalendar.csv", index=False)
