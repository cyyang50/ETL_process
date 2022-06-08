
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def extract():
    for q in QUOTES:
        u = eval(f"{URL}")
        print(f"reading from url {u} ...")
        # grab web page content
        raw_html = requests.get(u,headers=HEADERS)
        # convert to a beautiful soup object
        soup = bs(raw_html.content, "lxml")
        #column_names
        table = soup.find("table")
        columns = table.find("thead").find_all("th")
        column_names = [c.string for c in columns if c.string is not None]
        #output:['Year', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        #row data
        all_tables = []
        all_column_names = []
        tables = []
        table_rows = table.find("tbody").find_all("tr")
        for r in table_rows:
            td = r.find_all("td")
            row = [tr.string for tr in td]
            tables.append(row)
        #data => data frame
        df = pd.DataFrame(tables)
        df.columns = column_names
        #stack the data frame
        df_col = df.set_index(['Year']).stack().reset_index().rename({'level_1': 'Month', 0:q }, axis=1)
        # write to csv
        df_col.to_csv("{}_carsales_src.csv".format(q),index=False)
        print(f"{q}_carsales_src.csv is downloaded from url {u} ...")

if __name__ == "__main__":
    #set user agent
    USER_AGENT = (
        'Mozilla/5.0 (X11; Linux x86_64)'
        'AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/90.0.4430.212 Safari/537.36'    )
    HEADERS = {'User-Agent': USER_AGENT}
    #print robots.txt
    website = "https://www.goodcarbadcar.net"
    print(requests.get(f"{website}/robots.txt", headers=HEADERS).content.decode())
    print("*"*15)
    #set URL
    URL = 'f"{website}/{q}-us-sales-figures/"'
    QUOTES = ["tesla-inc", "ford-motor-company", "general-motors"]
    extract()
