import requests
import glob
import pandas as pd
import time
import random as rn
from urllib.parse import urlparse, parse_qs
from pathlib import Path

"""
- get all bonds page - cache to html - cache to csv
- filter by issuer and currency - cache to csv
- get each bond's individual page from bvb - cache to html - cache to csv
- make single dataframe of all bonds information - cache to csv
"""


# get all bonds page from bvb - one request - cache

def get_all_bonds_bvb():
    url = "https://www.bvb.ro/FinancialInstruments/Markets/Bonds"
    x = requests.get(url)
    print(x.status_code)

    bonds_html = "bonds.html"    # file name

    #write to file
    with open(bonds_html, "wb") as f:
        f.write(x.content)


# make all bonds from html page to csv - cache

def all_bonds_to_csv():
    bonds_html = "bonds.html"    # file name

    df = pd.read_html(bonds_html)    # gives list
    df = pd.DataFrame(df[0])    # takes only pos 0 into dataframe
    df.rename(columns={"Simbol / ISIN" : "ISIN"}, inplace=True)

    # get each bond's shortened symbol for url use
    df["Simbol"] = df["ISIN"].astype(str).str.split("RO").str[0]    

    # print(df)    # debug

    # save to csv - cache
    file_name = "all_bvb_bonds.csv"
    df.to_csv(file_name)

    return df


# filter by issuer - Minstry of Finance (gov bonds)

def filter_by_issuer(df):
    # create a bool mask of true/false for each row    
    isMfin = df["Societate"] == "MINISTERUL FINANTELOR"

    # count them
    print("nr. of Mfin bonds: ", isMfin.sum())

    # dataframe with only Mfin bonds
    df = df[isMfin]
    df = df.reset_index(drop=True)

    print(df)    # debug

    return df


# filter by currency

def filter_by_currency(df):
    # create a bool mask to look for the EUR currency - otherwise RON
    isEur = df["Moneda de emisiune"] == "EUR"

    # count them
    print("nr. of Eur bonds: ", isEur.sum())

    # update dataframe
    df = df[isEur]
    df = df.reset_index(drop=True)    # recounts the index

    print(df)    # debug

    return df


# build url lit to search individual bonds
# pass to it the filtered bond list or the all_bonds_to_csv()

def build_bond_url_list(df):
    base_url = "https://www.bvb.ro/FinancialInstruments/Details/FinancialInstrumentsDetails.aspx?s="

    # adds url column with each bond's url for web search
    df["url"] = base_url + df["Simbol"].astype(str)

    return df


# save filtered bonds to csv file

def save_filtered_bonds(df):
    file_name = "mfin_bonds.csv"
    df.to_csv(file_name)


# download each bond's page    ## careful when you run this

def download_all_bonds_pages(df):

    # regime switching waiting times for more human behavior
    
    def wait():
        lo, hi = rn.choice([(2, 6), (7, 10)])
        return rn.uniform(lo, hi)

    session = requests.Session()    # start a single session, one connection multiple requests

    session.headers.update({    # updates user agent header, tells the website it's a normal browser
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0"
    })

    for url, symbol in zip(df["url"], df["Simbol"]):    # zip pairs their elems index by index

        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()    # catches silent errors that would give a blank page

        except requests.RequestException as e:    # catches any error from requests in e
            print(f"failed {url} -> {e}")
            continue

        print(response.status_code)    # debug

        file_name = f"bonds_html/{symbol}.html"
        print(file_name)    # debug

        with open(file_name, "wb") as f:    # make sure the folder bonds_html/ exists
            f.write(response.content)

        time.sleep(wait())


# bonds html pages to csv

def bonds_html_to_csv():
    html_files = glob.glob("bonds_html/*.html")

    for file_path in html_files:

        try:

            # read html file
            
            df = pd.read_html(file_path)
            df = pd.concat(df, ignore_index=True)
            print(len(df), "\n", df)    # debug

            # save the combined dataframe

            file_name = Path(file_path).stem
            csv_path = f"bonds_csv/{file_name}.csv"
            df.to_csv(csv_path)

        except FileNotFoundError:
            print(f"couldn't find: {file_path}")
        except ValueError:
            print(f"no html table found in: {file_name}")
        except Exception as e:    # general error
            print(f"error processing {file_path}: {e}")


# output each csv file in bonds_csv folder    # debug 

def read_bonds_csv():
    csv_files = glob.glob("bonds_csv/*.csv")
    for file in csv_files:
        try:
            df = pd.read_csv(file, index_col=0)
            print(df)
            # return 0    # debug
        except Exception as e:
            print(f"issue: {e}")


# build final complete dataframe with all bond data

def make_final_df():
    csv_files = glob.glob("bonds_csv/*.csv")
    all_bonds_rows = []

    # parse through all files in the folder
    for file in csv_files:
        try:
            # load csv file as dataframe
            df = pd.read_csv(file, usecols=[1, 2], names=["label", "value"], header=0)

            # clean up: remove empty rows and strip extra spaces/colons from labels
            df = df.dropna(subset=["label"])    # drops empty rows
            df["label"] = df["label"].str.replace(":", "").str.strip()    # replaces ":" with nothing, "simbol" instead of "simbol:"

            # correct duplicate rows - for the two "Data/ora" rows
            df.loc[ df.duplicated("label", keep="first") & (df["label"] == "Data/ora"), "label" ] = "Data/ora last trade"

            # transpose the dataframe
            df_flipped = df.set_index("label").T

            # append this single row to the list of all rows
            all_bonds_rows.append(df_flipped)

        except Exception as e:
            print(f"issue with {file}: {e}")

    # combine all rows into the final dataframe
    master_df = pd.concat(all_bonds_rows, ignore_index=True)

    print(master_df)    # debug

    # save to csv
    master_df.to_csv("all_bonds.csv", index=False)

    print("final dataframe created successfully!")



""" Program """    

## get all bonds page from bvb - one request - cache to one html file
get_all_bonds_bvb()

## make all bonds from html page to csv - cache to one csv file
df = all_bonds_to_csv()    # returns dataframe from html

""" ## """

""" filtering """
## filter by issuer
df = filter_by_issuer(df)

## filter by currency
df = filter_by_currency(df)
""" -------- """

## build bond url list
df = build_bond_url_list(df)

## save filtered bonds - caches to csv single file
save_filtered_bonds(df)

""" ## """

""" careful """
## get each bond's page from bvb - multiple requests - caches to html multiple files
download_all_bonds_pages(df)
""" ------- """

## previously downloaded html files to csv - caches to csv multiple files
bonds_html_to_csv()

""" ## """

read_bonds_csv()    # debug

## build final complete dataframe with all bond data - caches to csv single file
make_final_df()