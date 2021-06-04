from dotenv import load_dotenv
import sqlite3, os, requests


# Loads environment variables from .env file
load_dotenv()

# https://iexcloud.io/docs/api/
IEX_BASE_URL = "https://cloud.iexapis.com/stable/"
API_TOKEN = os.getenv("IEX_TOKEN")


def getAllStocks():
    # Get list of all stocks
    endpoint_url = "ref-data/symbols?filter=symbol,name&token="
    stocks = sendApiRequest(endpoint_url)
    return stocks
                    

def sendApiRequest(endpoint_url):
    # Calling API
    try:
        request_url = IEX_BASE_URL + endpoint_url + API_TOKEN
        response = requests.get(request_url)
        response.raise_for_status()
        results = response.json()
    except requests.exceptions.HTTPError as error:
        print (error)
        results = None

    return results


if __name__ == '__main__':
    connection = sqlite3.connect("stocks.sqlite3")
    cursor = connection.cursor()
    
    stocks = getAllStocks()
    query = "INSERT INTO stocks(symbol, name) VALUES(?, ?)"

    # Insert only allowed stocks
    for stock in stocks:
        try:
            cursor.execute(query, [stock['symbol'], stock['name']])
            print(f"Inserted a new stock: {stock['symbol']}, {stock['name']}.")
        except Exception:
            continue

    connection.commit()
    connection.close()

