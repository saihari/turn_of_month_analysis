import requests
import calendar
import os
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile, BadZipFile
from datetime import datetime


URL = "https://www.niftyindices.com/Market_Capitalisation_Weightage_Beta_for_NIFTY_50_And_NIFTY_Next_50/mcwb_{month_year}.zip"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
}

MONTHS = calendar.month_abbr


def download(year: str) -> None:

    # Create path
    zipfile_path = f"./data/zipfiles/{year}"
    os.makedirs(zipfile_path, exist_ok=True)

    # Create path
    extracted_file_path = f"./data/reports/mcwb/{year}"
    os.makedirs(extracted_file_path, exist_ok=True)

    for month in MONTHS:

        if (int(year) == datetime.now().year) & (
            month == datetime.now().strftime("%b")
        ):
            break

        url = URL.format(month_year=month + year[-2:])

        # Downloading the file
        response = requests.get(url, stream=True, headers=HEADERS)

        print(f"File Downloaded Started: {month}, {year}")

        if "text/html; charset=utf-8" in response.headers.get("content-type"):
            continue

        with open(zipfile_path + "/" + url.split("/")[-1], mode="wb") as file:
            for chunk in response.iter_content(chunk_size=10 * 1024):
                file.write(chunk)

        response.close()

        print(f"{month}, {year} MCWB Report Downloaded Successfully")
        try:
            with ZipFile(zipfile_path + "/" + url.split("/")[-1], "r") as object:
                object.extractall(extracted_file_path + f"/{month}/")
                print(f"{month}, {year} MCWB Report Extracted Successfully")
        except BadZipFile:
            url.split("/")[-1]
            print(f"{month}, {year} MCWB Report Could not be Extracted")


if __name__ == "__main__":

    # Loop runs through 2009 to current year
    for year in range(2009, datetime.now().year + 1):
        download(str(year))
