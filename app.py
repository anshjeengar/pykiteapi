import pysnooper
import sqlite3
from datetime import datetime, #timedelta

import icecream
import pandas
from nsedata import Nse

@pysnooper.snoop()
def fetchCodes(nse: Nse):
    """#Fetch the scrips (code & company name) for live NSE server
    Args:
        nse (Nse): nsedata.Nse object
    Returns:
        [pandas.Dataframe]: List of Scrips
    """
    allCodes = sorted(nse.all_codes.items())
    list_of_scrips = pandas.DataFrame.from_records(
        allCodes, columns=["code", "company_name"]
        )
    return list_of_scrips


def main():
    # for debugging
    ic = icecream.ic
    ic.enable()

    # Initialize the Nse class and fetch the scrips for NSE server
    nse = Nse()
    listOfScrips = fetchCodes(nse)

    # Create a table in sqlite3 db and insert the scrip data to it

    with sqlite3.connect("nseData.db") as con:
        ic(f"Database opened: {con}")
        cur = con.cursor()
        
        ensure_schema = """CREATE TABLE IF NOT EXISTS scrips (
            scrip_id VARCHAR PRIMARY KEY,
            company_name VARCHAR UNIQUE NOT NULL)"""
        cur.execute(ensure_schema)

        cur.executemany(
            "INSERT INTO scrips values (?, ?)",
            zip(listOfScrips.code, listOfScrips.company_name),
        )

        con.commit()
    
    scripHistoriacalData = nse.historical_data(
        code="bel",
        date_from=(1, 7, 2021), date_to=(9, 7, 2021),
        give_json=True
    )
    ic(scripHistoriacalData)

    # scrip_data = pd.DataFrame()
    # for scrip in all_codes:
    #     scrip_data = scrip_data.add()


if __name__ == "__main__":
    main()