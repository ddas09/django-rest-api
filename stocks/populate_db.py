from dotenv import load_dotenv
import requests, os, sqlite3, random

# loads enviroment variables from .env
load_dotenv() 


def sendApiRequest(endpoint_url):
    base_url = os.getenv("API_BASE_URL")
    api_token = "token=" + os.getenv("API_TOKEN")

    # Calling API
    try:
        request_url = base_url + endpoint_url + api_token
        response = requests.get(request_url)
        response.raise_for_status()
        results = response.json()
    except requests.exceptions.HTTPError as error:
        print (error)
        results = None

    return results


def insertStockData(cursor):
    # Get stock list registered on IEX
    stocks = sendApiRequest("ref-data/symbols?filter=symbol,name,type,isEnabled&")
    allowed_stock_types = ['ad', 'cs', 'ps']

    # Insert new stock informations
    query = "INSERT INTO stocks(symbol, name, price) VALUES(?, ?, ?)"
    for stock in stocks:
        if stock['type'] in allowed_stock_types and stock['isEnabled']:
            price = round((random.random() * 1000), 2)
            values = [stock['symbol'], stock['name'], price]
            try:
                cursor.execute(query, values)
                print(f"Inserted a new stock: {values}")

            except Exception as e:
                continue


if __name__ == "__main__":
    # Accquire connection to the database
    connection = sqlite3.connect("stocks.sqlite3")
    cursor = connection.cursor()
    insertStockData(cursor)
    # Close connection
    connection.commit()
    connection.close()
