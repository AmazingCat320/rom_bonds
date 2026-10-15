
# grab bonds list from bvb
# filter down to just Mfin bonds
# additional filters readily visible
# output to csv

import requests
import pandas as pd
import numpy as np


# Saves the bonds html page

def get_html():
    url = "https://www.bvb.ro/FinancialInstruments/Markets/Bonds"
    x = requests.get(url)
    print(x.status_code)

    bonds_html = "bonds.html"    # file name

    with open(bonds_html, "wb") as f:    # write to file 
        f.write(x.content)


# gathers dataframe from html

def get_dataframe():
    bonds_html = "bonds.html"    # file name

    df = pd.read_html(bonds_html)
    df = pd.DataFrame(df[0])    # takes list into data frame
    df.rename(columns={"Simbol / ISIN" : "Simbol"}, inplace=True)

    # get each bond's symbol short for url use
    df["Simbol_scurt"] = df["Simbol"].astype(str).str[:7]    # adds a new column with sliced symbol to be searchable online

    # print(df)    # debug

    return df


# reduce dataframe to only gov bonds

def filter(df):
    # create a bool mask of true/false for each row
    isMfin = df["Societate"] == "MINISTERUL FINANTELOR"

    # count them instantly
    print("nr. of Mfin bonds: ", isMfin.sum())

    # dataframe with only Mfin entries
    gov_bonds = df[isMfin]
    gov_bonds = gov_bonds.reset_index(drop=True)    # recounts the index, drop leaves only the new index

    print(gov_bonds)    # debug

    return gov_bonds


# currency filter

def filter_currency(gov_bonds):
    # create a bool mask to look for the Eur currency
    isEur = gov_bonds["Moneda de emisiune"] == "EUR"

    # count them
    print("nr. of Eur bonds: ", isEur.sum())

    #update dataframe
    eur_bonds = gov_bonds[isEur]
    eur_bonds = eur_bonds.reset_index(drop=True)    # recounts the index

    print(eur_bonds)    # debug

    return eur_bonds


# save to file

def save_file(gov_bonds):
    file_name = "mfin_bonds.csv"
    gov_bonds.to_csv(file_name)




"""     
        program
# grab bonds list from bvb
# filter down to just Mfin bonds
# additional filters readily visible
# output to csv
"""


# scrape main bond page on bvb
# get_html()    # turn on / off

# make the main bond page from html to dataframe
# get_dataframe()    # turn on / off

df = get_dataframe()    # gets df from get_dataframe function

gov_bonds = filter(df)    # gets gov_bonds from filter function

gov_bonds = filter_currency(gov_bonds)    # turn on / off

save_file(gov_bonds)    # save to file

# final message

print("")
print("dataframe from bonds.html file")
print("filtered down by Mfin bonds, and currency")