import requests

# Saves the bonds html page

url = "https://www.bvb.ro/FinancialInstruments/Markets/Bonds"
x = requests.get(url)
print(x.status_code)

saveFile = "bonds.html"

with open(saveFile, "wb") as f:
    f.write(x.content)