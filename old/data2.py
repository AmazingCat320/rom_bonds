# get mfin bonds csv
# get list of each bond to search its info
# put everything together in a dataframe
# export to csv

import glob
import requests
import pandas as pd
import numpy as np
import time
import random as rn
from urllib.parse import urlparse, parse_qs


# search each bond's page
# for each symbol - build url string - request - save

# build url list to search individual bonds
def url_list():
    web_list = []

    for simbol in bonds["Simbol_scurt"]:
        web_list.append(f"https://www.bvb.ro/FinancialInstruments/Details/FinancialInstrumentsDetails.aspx?s=" + simbol)    # makes the url string

    print(web_list)    # debug

    return web_list


# regime switching waiting times

def wait():
    lo, hi = rn.choice([(2, 6), (7, 10)])
    return rn.uniform(lo, hi)


# download each bond's page    ## careful when you run this ##

def scrape(web_list):    # web_list is the list of all urls

    session = requests.Session()    # start a single session, one connection multiple requests

    session.headers.update({    # updates user agent header, tells the website it's a normal browser
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0"
    })

    # loops over each bond's url
    for url in web_list:    # do it for each symbol

        try:    # handle errors so the program doesn't end
            response = session.get(url, timeout=10)    # get the page of the url in web_list
            response.raise_for_status()    # catches silent errors that would give a blank page

        except requests.RequestException as e:    # if there's an error put it in "e"
            print(f"failed {url} -> {e}")   
            continue  

        print(response.status_code)    # debug

        symbol = parse_qs(urlparse(url).query)["s"][0]    # gets url characters from last, up to the "s="
        save_file = f"bonds_html/{symbol}.html"    # takes only the short symbol as file name
        print(save_file)    # debug

        with open(save_file, "wb") as f:    # saves to file
            f.write(response.content)

        time.sleep(wait())    # get wait time from wait function


# bond's html pages to csv

def bonds_to_csv():
    # get html page into datafram -> save as csv
    for simbol in bonds["Simbol_scurt"]:    # parse each bond shortened symbol which is their filename
        target = f"bonds_html/{simbol}.html"    # build filename.html for each bond   
        try:
            # read html file
            df = pd.read_html(target)    # gives a list with 4 elems
            df = pd.concat(df, ignore_index=True)    # get all 4 elems into a dataframe
            print(len(df), "\n", df)    # debug

            # save the combined dataframe
            file_name = "bonds_csv/" + simbol + ".csv"    # build filename.csv for each bond
            df.to_csv(file_name)
        except FileNotFoundError: 
            print(f"couldn't find: {simbol}.html")
        except ValueError:
            print(f"no html table found in: {simbol}.html")
        except Exception as e:    # general error
            print(f"error processing {simbol}: {e}")

            
# output each csv file in bonds_csv folder # debug

def read_csv():
    for simbol in bonds["Simbol_scurt"]:
        try:
            df = pd.read_csv(f"bonds_csv/{simbol}.csv", index_col=0)
            print(df)
            return 0
        except Exception as e:
            print(f"issue: {e}")


# get all the csv in bonds_csv folder into a single dataframe, save it as csv

def final_df():
    csv_files = glob.glob("bonds_csv/*.csv")    # get all csv files in the folder
    all_bonds_rows = []

    # parse through all files in the folder
    for file in csv_files:
        try:
            # load csv file as dataframe
            df = pd.read_csv(file, usecols=[1,2], names=["label", "value"], header=0)

            # Clean up: remove empty rows and strip extra spaces/colons from labels
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
    master_df.to_csv("all_bonds_full.csv", index=False)

    print("final dataframe created successfully!")



"""
    program
## get bond list of all mfin bonds from csv - from data.py (after currency filter)
## get list of all urls: made up by a url baseplate + the bond's short symbol at the end
## scrape(web_list) : scrape each bond's individual page - the urls from web_list = url_list()
## bonds_to_csv() : get each bond's data from html page to dataframe to csv file
"""

## set main data
file_name = "mfin_bonds.csv"
bonds = pd.read_csv(file_name, index_col=0)    # get Mfin bonds from csv


# print(bonds)    # debug


# web_list = url_list()    # gets web_list from url_list function; list of all the urls


# scrape(web_list)    ## be careful with this ##


## get each bond's data from html page into csv
# bonds_to_csv()


# read_csv()    # debug


final_df()

###