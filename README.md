`pip install -r requirements.txt`

Create a file `src/._keys.csv` and put your api and secret key in it
````
api_key,secret_key
````

Warning: Never checkin your keys

Below is an example of downloading all 30 minute wide candlestick data in the trx eth market from start date to end date

Usage: 
`download_binance_historic_candlestick.py --start="1 Dec, 2016" --end="3 Jan, 2019" -w 30m -m TRXETH`