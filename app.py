import pysnooper
import sqlite3

# from datetime import datetime #timedelta

from icecream import ic
import pandas
from nsedata import Nse


# for debugging
# ic = icecream.IceCreamDebugger()
ic.enable()


def fetchCodes(nse: Nse):
    """#Fetch the scrips (code & company name) for live NSE server
    Args:
        nse (Nse): nsedata.Nse object
    Returns:
        [pandas.Dataframe]:
            List of Scrips with columns 'scripCode' and 'companyName'"""
    allCodes = nse.all_codes(give_json=True)
    # listOfScrips = pandas.DataFrame(allCodes)
    listOfScrips = pandas.DataFrame.from_records(
        allCodes, columns=["scripCode", "companyName"], index="scripCode"
    )
    return listOfScrips


def main():
    """Initialize the Nse class and fetch the scrips for NSE server"""
    nse = Nse()
    listOfScrips = fetchCodes(nse)
    # print(listOfScrips)

    """Create a table in sqlite3 db and insert the scrip data to it"""
    with sqlite3.connect("nseData.db") as con:
        ic(f"Database opened: {con}")
        cur = con.cursor()

        """Determine if scrips table exists in sql_master database;
        If not, create it """
        cur.execute(
            """SELECT name FROM sqlite_master
            WHERE type='table' AND name='scrips'"""
        )
        if cur.fetchone() is None:
            ensure_schema = """CREATE TABLE "scrips" (
                "scrip_id"	text NOT NULL,
                "company_name"	text,
                PRIMARY KEY("scrip_id")
                ) WITHOUT ROWID"""
            cur.execute(ensure_schema)
            ic(f"Table created: {ensure_schema}")

        """Insert the scrip data to the table"""
        insert_row = """INSERT OR IGNORE INTO scrips VALUES (?, ?)"""
        cur.executemany(
            insert_row,
            zip(listOfScrips.code, listOfScrips.company_name),
        )

        """Commit the transaction"""
        con.commit()

        """Close the connection"""
        ic(f"Database closed: {con}")
        exit(con)

    """historical data of 'bel' as in 'scrips' table
    from nsedata for last 5 days"""
    scripHistoriacalData = nse.historical_data(
        code="bel", date_from=(1, 7, 2021), date_to=(8, 7, 2021), give_json=True
    )
    ic(scripHistoriacalData)

    # scrip_data = pd.DataFrame()
    # for scrip in all_codes:
    #     scrip_data = scrip_data.add()


if __name__ == "__main__":
    main()
