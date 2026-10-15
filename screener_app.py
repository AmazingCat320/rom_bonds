import pandas as pd
import numpy as np

# load the all_bonds.csv file into a dataframe

def load_all_bonds():
    file_name = "all_bonds.csv"
    df = pd.read_csv(file_name)
    print(df)
    print(df.columns.to_list())
    return df


def filter_by_currency(df):
    # create a bool mask to look for the EUR currency - otherwise RON
    isEur = df["Moneda"] == "EUR"

    # count them
    print("nr. of Eur bonds: ", isEur.sum())

    # update dataframe
    df = df[isEur]
    df = df.reset_index(drop=True)    # recounts the index

    # print(df)    # debug

    return df


# load all bonds
df = load_all_bonds()


# convert maturity date data to pandas datetime (so it can be used)
df["Data maturitatii"] = pd.to_datetime(df["Data maturitatii"], format="%d.%m.%Y")

# calculate remaining time to maturity in days
today = pd.Timestamp.now().normalize()
df["Days left"] = (df["Data maturitatii"] - today).dt.days

# filter for bonds expiring withing a year ( <= 360 days )
mask_under_1yr = (df["Days left"] <= 900) & (df["Days left"] > 0)
filtered_df = df[mask_under_1yr].copy()    # make a new dataframe with the filtered data

# print(filtered_df)    # debug

# make new dataframe
# take over only some columns from the old one
new_df = filtered_df[["Simbol", "Data/ora last trade", "Cupon curent", "Days left", "Moneda de emisiune", "Data maturitatii"]]
new_df = new_df.rename(columns={"Cupon curent" : "Cupon%", "Moneda de emisiune" : "Moneda", "Data/ora last trade" : "Last trade"})

# filter by currency - optional
new_df = filter_by_currency(new_df)


# clean up columns
new_df[["Bid", "Ask"]] = df["Bid / Ask"].str.split(" / ", expand=True)
new_df["Bid"] = pd.to_numeric(new_df["Bid"].str.replace(",", "."), errors="coerce")
new_df["Ask"] = pd.to_numeric(new_df["Ask"].str.replace(",", "."), errors="coerce")
new_df["Cupon%"] = round( new_df["Cupon%"].str.replace(",", ".").str.replace("%", "").astype(float), 3)
new_df[["Bid vol", "Ask vol"]] = df["Bid / Ask Vol."].str.split(" / ", expand=True)

# add spread% column
new_df["Spread%"] = round((new_df["Ask"] - new_df["Bid"]) / new_df["Ask"] * 100, 3)

# add yield column
new_df["yield"] = new_df["Cupon%"] / new_df["Ask"] * 100

# add yield left column
# 1. Total net cash return over the remaining lifespan
is_short_term = new_df["Days left"] <= 365
# 2. Run the calculation only where True
new_df["Return_Left"] = np.where(
    is_short_term,
    (
        ((100 - new_df["Ask"]) + ((new_df["Days left"] / 365) * new_df["Cupon%"]))
        / (new_df["Ask"] + (((365 - new_df["Days left"]) / 365) * new_df["Cupon%"]))
    ) * 100,
    np.nan  # What to show if Days left > 365 (e.g., NaN or 0)
)

# new_df["Annualized%"] = new_df["Cupon%"] * ()

# show results
pd.set_option('display.max_rows', None)
print(new_df)