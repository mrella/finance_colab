import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')
sns.set_theme(style="darkgrid", palette="muted", font_scale=1.1)




def drawdown_medio_tickers_img(tickers, fecha_inicio, fecha_fin, titulo, indice, path):
  data = yf.download(tickers, start=fecha_inicio, end=fecha_fin)['Close']
  data_index = yf.download(indice, start=fecha_inicio, end=fecha_fin)['Close']

  # Crear un DataFrame para almacenar los resultados
  drawdowns = []

  # Calcular drawdown para cada ticker
  print("Calculando drawdowns...")
  for ticker in tickers:
      if ticker in data.columns:
          stock_data = data[ticker].dropna()

          if not stock_data.empty:
              max_price = stock_data.max()
              # Precio más reciente
              latest_price = stock_data.iloc[-1]
              # Calcular drawdown
              drawdown = (latest_price - max_price) / max_price
              drawdowns.append({'Ticker': ticker, 'Drawdown': drawdown})

  # Crear DataFrame con los drawdowns
  drawdown_df = pd.DataFrame(drawdowns).sort_values(by='Drawdown')

  # Calcular la mediana y el índice
  median_drawdown = drawdown_df['Drawdown'].median()
  index_drawdown = (data.mean(axis=1).iloc[-1] - data.mean(axis=1).max()) / data.mean(axis=1).max()

  # Graficar
  plt.figure(figsize=(12, 8))
  plt.bar(range(len(drawdown_df)), drawdown_df['Drawdown'], color='orange', alpha=0.7)
  plt.axhline(y=median_drawdown, color='green', linestyle='--', label=f'Median Stock: {median_drawdown:.1%}')
  plt.axhline(y=index_drawdown, color='red', linestyle='-', label=f'Index: {index_drawdown:.1%}')

  # Añadir etiquetas y título
  plt.title(f'{titulo} components drawdown {fecha_fin} ')
  plt.ylabel('Drawdown (%)')
  plt.xlabel('Stocks (sorted by drawdown)')
  plt.xticks([], [])  # Ocultar los nombres de los tickers en el eje x
  plt.legend()
  plt.savefig(path)
  plt.close()  # Cerrar la figura para liberar memoria


def generar_graficos(path):

    ##### parametros iniciales
    tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()

    fecha_inicio = f"{datetime.now().year}-01-01"
    fecha_fin = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    titulo = "SPY"
    indice = "SPY"
    #####
    drawdown_medio_tickers_img(tickers, fecha_inicio, fecha_fin, titulo, indice,path + "/spy_drawdown.png")

    ##### parametros iniciales
    tickers = [
        "AAPL","ABNB","ADBE","ADI","ADP","ADSK","AEP","AMAT","AMD","AMGN",
        "AMZN","ANSS","APP","ARM","ASML","AVGO","AXON","AZN","BIIB","BKNG",
        "BKR","CCEP","CDNS","CDW","CEG","CHTR","CMCSA","COST","CPRT","CRWD",
        "CSCO","CSGP","CSX","CTAS","CTSH","DASH","DDOG","DXCM","EA","EXC",
        "FANG","FAST","FTNT","GEHC","GFS","GILD","GOOG","GOOGL","HON","IDXX",
        "INTC","INTU","ISRG","KDP","KHC","KLAC","LIN","LRCX","LULU","MAR",
        "MCHP","MDLZ","MELI","META","MNST","MRVL","MSFT","MSTR","MU","NFLX",
        "NVDA","NXPI","ODFL","ON","ORLY","PANW","PAYX","PCAR","PDD","PEP",
        "PLTR","PYPL","QCOM","REGN","ROP","ROST","SBUX","SHOP","SNPS","TEAM",
        "TMUS","TSLA","TTD","TTWO","TXN","VRSK","VRTX","WBD","WDAY","XEL","ZS"
    ]
    fecha_inicio = f"{datetime.now().year}-01-01"
    fecha_fin = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    titulo = "QQQ"
    indice = "QQQ"
    #####
    drawdown_medio_tickers_img(tickers, fecha_inicio, fecha_fin, titulo, indice, path + "/qqq_drawdown.png")


def drawdown_medio_tickers_video(tickers, fecha_inicio, fecha_fin, titulo, indice, path):

  print(f"Descargando datos de los tickers {tickers}...")
  data = yf.download(tickers, start=fecha_inicio, end=fecha_fin)['Close']
  data_index = yf.download(indice, start=fecha_inicio, end=fecha_fin)['Close']

  # Configurar variables para la animación

  dates = data.index  # Fechas disponibles
  drawdowns_history = []

  # Precalcular drawdowns para cada fecha
  print("Calculando drawdowns...")
  for i in range(len(dates)):
      current_date = dates[i]
      window_data = data.iloc[0:i]
      drawdowns = []

      for ticker in data.columns:
          if ticker in window_data:
              stock_data = window_data[ticker].dropna()

              if not stock_data.empty:
                  max_price = stock_data.max()
                  latest_price = stock_data.iloc[-1]
                  drawdown = (latest_price - max_price) / max_price if max_price > 0 else 0
                  drawdowns.append(drawdown)

      # Almacenar drawdowns del día actual
      median_drawdown = pd.Series(drawdowns).median()
      up_to_date = data_index.loc[:current_date]
      #print(median_drawdown)
      #index_drawdown = (data.mean(axis=1).iloc[-1] - data_index.mean(axis=1).max()) / data_index.mean(axis=1).max()
      index_drawdown = float(( data_index.iloc[i]-data_index.iloc[1]) /  data_index.iloc[1])

      #print(index_drawdown)

      drawdowns_history.append((current_date, sorted(drawdowns), median_drawdown, up_to_date , index_drawdown ))

  #print (drawdowns_history)

  # Función para actualizar cada frame en la animación
  def update(frame):
      # Limpiar la figura completa antes de actualizar
      fig.clear()

      # Obtener los datos para el frame actual
      current_date, drawdowns, median_drawdown, up_to_date, index_drawdown = drawdowns_history[frame]

      # Crear subgráfico 1: Drawdowns
      ax1 = fig.add_subplot(2, 1, 1)
      ax1.bar(range(len(drawdowns)), drawdowns, color='orange', alpha=0.7)
      ax1.axhline(y=median_drawdown, color='green', linestyle='--', label=f'Median Stock: {median_drawdown:.1%}')
      ax1.axhline(y=index_drawdown, color='red', linestyle='-', label=f'{titulo} Index: {index_drawdown:.1%}')
      ax1.set_title(f'{titulo} Drawdowns as of {current_date.strftime("%Y-%m-%d")}')
      ax1.set_ylabel('Drawdown (%)')
      ax1.set_xticks([])  # Ocultar nombres de acciones
      ax1.legend()

      # Crear subgráfico 2: Precio del SPY
      ax2 = fig.add_subplot(2, 1, 2)
      ax2.plot(up_to_date.index, up_to_date.values, color='cyan', label='Price')
      ax2.set_title('Price Evolution')
      ax2.set_ylabel('Price ($)')
      ax2.set_xlabel('Date')
      ax2.legend()


  # Crear la figura para la animación
  fig = plt.figure(figsize=(12, 10))
  
  # Crear la animación
  ani = FuncAnimation(fig, update, frames=len(drawdowns_history), repeat=False)

  # Guardar como video
  print(f"Generando animación {titulo} ...")
  ani.save(path, writer='ffmpeg', fps=3)
  plt.close(fig)  # Cerrar la figura para liberar memoria
  print(f"Animación {titulo} completada...")


def generar_graficos_video(path):

    ##### parametros iniciales
    tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()
    fecha_inicio = f"{datetime.now().year}-01-01"
    fecha_fin = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    titulo = "SPY"
    indice = "SPY"
    #####
    drawdown_medio_tickers_video(tickers, fecha_inicio, fecha_fin, titulo, indice,path+"spy_drawdown.mp4")

    ##### parametros iniciales
    tickers = [
        "AAPL","ABNB","ADBE","ADI","ADP","ADSK","AEP","AMAT","AMD","AMGN",
        "AMZN","ANSS","APP","ARM","ASML","AVGO","AXON","AZN","BIIB","BKNG",
        "BKR","CCEP","CDNS","CDW","CEG","CHTR","CMCSA","COST","CPRT","CRWD",
        "CSCO","CSGP","CSX","CTAS","CTSH","DASH","DDOG","DXCM","EA","EXC",
        "FANG","FAST","FTNT","GEHC","GFS","GILD","GOOG","GOOGL","HON","IDXX",
        "INTC","INTU","ISRG","KDP","KHC","KLAC","LIN","LRCX","LULU","MAR",
        "MCHP","MDLZ","MELI","META","MNST","MRVL","MSFT","MSTR","MU","NFLX",
        "NVDA","NXPI","ODFL","ON","ORLY","PANW","PAYX","PCAR","PDD","PEP",
        "PLTR","PYPL","QCOM","REGN","ROP","ROST","SBUX","SHOP","SNPS","TEAM",
        "TMUS","TSLA","TTD","TTWO","TXN","VRSK","VRTX","WBD","WDAY","XEL","ZS"
    ]
    fecha_inicio = f"{datetime.now().year}-01-01"
    fecha_fin = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    titulo = "QQQ"
    indice = "QQQ"
    #####
    drawdown_medio_tickers_video(tickers, fecha_inicio, fecha_fin, titulo, indice,path+"qqq_drawdown.mp4")