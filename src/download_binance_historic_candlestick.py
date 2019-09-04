"""
Below is an example of downloading all 30 minute wide candlestick data in the trx/eth market from start date to end date

Usage:
    download_binance_historic_candlestick.py --start="1 Dec, 2016" --end="3 Jan, 2019" -w 30m -m TRXETH

"""
# Downloads historic candlestick data from binance and exports it to a csv file
#
# Each row of the saved csv file contains the following data:
#
#   [
#     1499040000000,      // Open time
#     "0.01634790",       // Open
#     "0.80000000",       // High
#     "0.01575800",       // Low
#     "0.01577100",       // Close
#     "148976.11427815",  // Volume
#     1499644799999,      // Close time
#     "2434.19055334",    // Quote asset volume
#     308,                // Number of trades
#     "1756.87402397",    // Taker buy base asset volume
#     "28.46694368",      // Taker buy quote asset volume
#     "17928899.62484339" // Ignore.
#   ]
#
# See https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#klinecandlestick-data
#
#
from optparse import OptionParser
from binance.client import Client
import datetime
import csv
import os

with open("._keys.csv", 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    keys = list(csv_reader)
    api_key = keys[0][0]
    api_secret = keys[0][1]

client = Client(api_key, api_secret)

parser = OptionParser()
parser.add_option("-s", "--start", dest="start",
                  help="start date", metavar="START")
parser.add_option("-e", "--end", dest="end",
                  help="end date", metavar="END")
parser.add_option("-w", "--width", dest="width",
                  help="time interval if candlestick (1m, 5m, 30m, 1h, 2h, etc)", metavar="WIDTH")
parser.add_option("-m", "--marketsym", dest="marketsymbol",
                  help="Market Symbol (TRXETH, etc)", metavar="MARKETSYM")
(options, args) = parser.parse_args()

if not os.path.exists("../output"):
    os.makedirs("../output")


start_date = "1 Dec, 2016"
end_date = "3 Jan, 2019"
candle_width = Client.KLINE_INTERVAL_30MINUTE
market_symbol = "TRXETH"

if options.start is not None:
    start_date = options.start
if options.end is not None:
    end_date = options.end
if options.marketsymbol is not None:
    market_symbol = options.marketsymbol

if options.width is not None:
    if options.width == Client.KLINE_INTERVAL_1MINUTE:
        candle_width = Client.KLINE_INTERVAL_1MINUTE
    elif options.width == Client.KLINE_INTERVAL_3MINUTE:
        candle_width = Client.KLINE_INTERVAL_3MINUTE
    elif options.width == Client.KLINE_INTERVAL_5MINUTE:
        candle_width = Client.KLINE_INTERVAL_5MINUTE
    elif options.width == Client.KLINE_INTERVAL_15MINUTE:
        candle_width = Client.KLINE_INTERVAL_15MINUTE
    elif options.width == Client.KLINE_INTERVAL_30MINUTE:
        candle_width = Client.KLINE_INTERVAL_30MINUTE
    elif options.width == Client.KLINE_INTERVAL_1HOUR:
        candle_width = Client.KLINE_INTERVAL_1HOUR
    elif options.width == Client.KLINE_INTERVAL_2HOUR:
        candle_width = Client.KLINE_INTERVAL_2HOUR
    elif options.width == Client.KLINE_INTERVAL_4HOUR:
        candle_width = Client.KLINE_INTERVAL_4HOUR
    elif options.width == Client.KLINE_INTERVAL_6HOUR:
        candle_width = Client.KLINE_INTERVAL_6HOUR
    elif options.width == Client.KLINE_INTERVAL_8HOUR:
        candle_width = Client.KLINE_INTERVAL_8HOUR
    elif options.width == Client.KLINE_INTERVAL_12HOUR:
        candle_width = Client.KLINE_INTERVAL_12HOUR
    elif options.width == Client.KLINE_INTERVAL_1DAY:
        candle_width = Client.KLINE_INTERVAL_1DAY
    elif options.width == Client.KLINE_INTERVAL_3DAY:
        candle_width = Client.KLINE_INTERVAL_3DAY
    elif options.width == Client.KLINE_INTERVAL_1WEEK:
        candle_width = Client.KLINE_INTERVAL_1WEEK
    elif options.width == Client.KLINE_INTERVAL_1MONTH:
        candle_width = Client.KLINE_INTERVAL_1MONTH

now_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
output_filename = "binance_historic_klines_{}_{}_{}_{}_created_{}.csv".format(
    market_symbol,
    start_date,
    end_date,
    candle_width,
    now_datetime)

output_directory_name = "../output"
output_path = os.path.join(output_directory_name, output_filename)

klines = client.get_historical_klines(market_symbol, candle_width, start_date, end_date)

with open(output_path, 'w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Write the header
    header = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"]
    csv_writer.writerow(header)

    for k_line in klines:
        print("Writing: {}".format(k_line))
        csv_writer.writerow(k_line)
