import json
import os
import requests
import csv
import datetime


def parse_response(response_text):
    if isinstance(response_text, str):
        response_text = json.loads(response_text)
    stock_values = []
    time_series_daily = response_text["Time Series (Daily)"]
    for result_date in time_series_daily:
        prices = time_series_daily[result_date]
        output = {
            "date": result_date,
            "open": prices["1. open"],
            "high": prices["2. high"],
            "low": prices["3. low"],
            "close": prices["4. close"],
            "volume": prices["5. volume"]
        }
        stock_values.append(output)
    return stock_values

def write_prices_to_file(prices=[], filename= "data/stock_symbol.csv"):
    csv_filepath = os.path.join(os.path.dirname(__file__), "..", filename)
    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["date", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        for p in prices:
            row = {
                "date": p["date"],
                "open": p["open"],
                "high": p["high"],
                "low": p["low"],
                "close": p["close"],
                "volume": p["volume"]
            }
            writer.writerow(row)

def mean(numbers):
    return float(sum(numbers))/max(len(numbers), 1)

if __name__ == '__main__':
    api_key = os.environ.get("alphavantage_api_key")
    stock_symbol = input("Please enter stock you would like to review: ")

    try:
        float(stock_symbol)
        quit("Oops! Expecting a non-numeric stock symbol (e.g. 'MSFT').")
    except ValueError as e:
        pass
    if len(stock_symbol)>5:
        quit("Oops! Expecting a properly formed stock symbol (e.g. 'MSFT').")
    else:
        pass

    # url_end = stock_symbol + "&outputsize=full&apikey=" + api_key
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={api_key}" #+ url_end #likely #want the TIME SERIES DAILY version

    response = requests.get(request_url)
    response_output = json.loads(response.text)
    # print(response)
    if "Error Message" in response.text:
        quit("I'm sorry. That stock symbol could not be found.")

    daily_prices = parse_response(response.text)

    write_prices_to_file(prices=daily_prices, filename="data/" + stock_symbol + ".csv")

    datestamp = datetime.date.today().strftime('%m/%d/%Y')
    timestamp = datetime.datetime.now().strftime('%I:%M %p')
    metadata = response_output["Meta Data"]
    stock_data = response_output["Time Series (Daily)"]
    dates = list(stock_data)
    latest_daily_data = stock_data[dates[0]]
    last_update = dates[0]
    # datetime.date(last_update).strptime('%m/%d/%Y')
    #TODO: format the last update date correctly

    high = []
    low = []
    volume = []

    for x in stock_data:
        high.append(float(stock_data[x]["2. high"]))
        low.append(float(stock_data[x]["3. low"]))
        volume.append(float(stock_data[x]["5. volume"]))

    latest_price = latest_daily_data["4. close"]
    latest_price = float(latest_price)
    latest_price_usd = "${0:,.2f}".format(latest_price)

    avg_high = max(high)
    avg_high_usd = "${0:,.2f}".format(avg_high)
    avg_low = min(low)
    avg_low_usd = "${0:,.2f}".format(avg_low)

    avg_vol = mean(volume[:30])

    print("Stock: " + stock_symbol)
    print("Run on: " + datestamp + " at " +  timestamp)
    print("Latest data from: " + last_update)
    print("Lastest closing price: " + latest_price_usd)
    print("Recent average high price:", avg_high_usd)
    print("Recent average low price:", avg_low_usd)

    if volume[0] > avg_vol: #IBD recommends buying stocks at above average volume
        if low[0]>low[1] and low[0]>low[2]:
            print("Buy! This stock is trending upward.") #I use these words loosely considering my extremely limited knowledge of stocks.
        else:
            print("Do not buy. This stock does not appear to be trending upward.")
    else:
        low_vol = input("Low volume. IBD recommends buying stocks at above average volume. Would you like to continue? ")
        if low_vol == "yes":
            if low[0]>low[1] and low[0]>low[2]:
                print("Buy! This stock is trending upward.")
            else:
                print("Do not buy. This stock does not appear to be trending upward.")
        else:
            print("Do not buy. Market volume is too low.")
