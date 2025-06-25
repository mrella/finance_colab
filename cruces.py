import yfinance as yf
import pandas as pd
#import yahoo_fin.stock_info as si
from datetime import datetime, timedelta


# Función para detectar cruces como un trader pro
def detect_crossover(data, fast_ma, slow_ma):
    if len(data) < 2:
        return None
    if data[fast_ma].iloc[-2] < data[slow_ma].iloc[-2] and data[fast_ma].iloc[-1] > data[slow_ma].iloc[-1]:
        return 'alcista'
    elif data[fast_ma].iloc[-2] > data[slow_ma].iloc[-2] and data[fast_ma].iloc[-1] < data[slow_ma].iloc[-1]:
        return 'bajista'
    return None


def get_cruces(tickers):
  
  fecha_fin = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
  #data = yf.download(tickers, start=fecha_fin).dropna(axis=1)
  #data.index = pd.to_datetime(data.index)

  # Parámetros configurables (¡flexibilidad total!)
  fast_ma_period = 20  # Media móvil rápida
  slow_ma_period = 50  # Media móvil lenta
  period = '6mo'       # Período de datos históricos

  # Lista para los tickers con cruce
  last_cruces = []
  #warnings.filterwarnings("ignore", category=FutureWarning)

  for ticker in tickers:
    try:
        crossover = False
        try:
            data = yf.download(ticker, period=period, progress=False)           
            data['Fast_MA'] = data['Close'].rolling(window=fast_ma_period).mean() 
            data['Slow_MA'] = data['Close'].rolling(window=slow_ma_period).mean()
            crossover = detect_crossover(data, 'Fast_MA', 'Slow_MA') 
        
        except Exception as e2:
            print(f"Error al calcular medias móviles para {ticker}")
            crossover = False
        if crossover:
            last_cruces.append(ticker)
    except Exception as e:
        print(f"Error con {ticker}: {e}")
     
  return last_cruces 