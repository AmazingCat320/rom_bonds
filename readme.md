## Context
For personal reasons I wanted to invest in low risk assets, in this case bonds, since I noticed Fidelis bonds, of my preffered maturities, were trading at nice interest rates, I wanted to have my own means to gather information about them and organize it. To know which ones to buy for my own strategy. 

**To be more specific:** I wanted to have a program that I can run whenever I want to update myself on the state of my interested issues, and return a table of organized data upon which I can make financial decisions: on porfolio, strategy and allocation.

This project has been financially valuable for me.

## Project Timeline
- Studying scraping methods and the BVB website: fortunately all the data needed is statically rendered on the HTML without requiring to interact with the webpage.

- Designing the pipeline: Scrape -> Organize the data -> screen -> display

- Designing circuit breaks: caching stages for both HTML and DF manipulation (to and from CSV)


## Clever shortcuts
I mentioned above how all the important data is already statically rendered in HTML, just not plainly visible. The scraping starts by looking at the url of the BVB bonds page. Which is downloaded and from where we can gather the list of the tickers of all bonds traded on the BVB. Then there are the following steps:

- Filter down to issuer (Ministry of finance) and currency (for me it's EUR, otherwise you can choose RON).

- Gather the tickers and form the URL of the page of each issue given a format that can be extrapolated by looking at the page of each bond issue on the BVB

- Download each issue's page, scrape its data, which is already conveniently arranged in a table, much like all the other ones in the BVB main all bonds page, cut down to the data that I need, and finally apply the filters.

#

### It works because:
- The data is statically available even if not visibly displayed in full for a visitor on the site
- Each bond issue has its own page, they all follow the same url structure that can be reconstructed and modified with each new ones ticker symbol. 
- And each issue has all its important information on its own page


### What can be improved:
The code could be rendered more neat and organized. The caching can be organized better as well. To be honest, personally, while I do get the satisfaction of bringing projects to completion, I also can't avoid down the line the urge of rewriting them. Which I have in plan for the future for this project. The project remains financially valuable for me.

#

##### **<u>Disclaimer</u>**: web scrapers can break over time as they depend on a given structure of the target site to be able to function properly. This project may not work if: BVB changes their site and I don't keep up with it to update the app. 