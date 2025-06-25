import yfinance as yf
import pandas as pd
#import yahoo_fin.stock_info as si
from datetime import datetime, timedelta


def get_gappers(tickers):
  
  fecha_fin = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
  data = yf.download(tickers, start=fecha_fin).dropna(axis=1)
  data.index = pd.to_datetime(data.index)

  
  s = ""
  sum=0
  last_tickers = []

  gap = data['Open'] / data['Close'].shift(1)
  roc = data['Close'].pct_change()
  volume_diff = data['Volume']/data['Volume'].rolling(10).mean()

  mask = ((gap > 1.5) & (roc > 0.10) & (volume_diff >  2)).astype(int)

  mask = ((gap > 1.04) | (roc > 0.04)).astype(int)

  selected_stocks_by_date = {}

  for date in mask.index:
      selected_tickers = mask.loc[date][mask.loc[date] == 1].index.tolist()
      selected_stocks_by_date[date.strftime('%Y-%m-%d')] = selected_tickers

  for date, tickers in selected_stocks_by_date.items():
      s = s + (f"{date}:\n {tickers}\n\n")
      if tickers is not None:
          last_tickers = tickers
          sum += len(tickers)


  return s, sum, last_tickers 