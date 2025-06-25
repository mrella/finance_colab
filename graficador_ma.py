import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
sns.set_theme(style="darkgrid", palette="muted", font_scale=1.1)
import matplotlib
matplotlib.use('Agg')


def generar_graficos(tickers, path):
    
    # Parámetros configurables (¡flexibilidad total!)
    fast_ma_period = 20  # Media móvil rápida
    slow_ma_period = 50  # Media móvil lenta
    period = '6mo'       # Período de datos históricos

    for i, ticker in enumerate(tickers):

        fig, ax = plt.subplots(1, 1, figsize=(12, 5))   
        #axes = [axes]  # Ajuste para un solo gráfico
        data = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        data['Fast_MA'] = data['Close'].rolling(window=fast_ma_period).mean()
        data['Slow_MA'] = data['Close'].rolling(window=slow_ma_period).mean()

        #ax = axes[i]
        ax.plot(data['Close'], label='Precio', color='cyan')
        ax.plot(data['Fast_MA'], label=f'MA {fast_ma_period}', color='orange')
        ax.plot(data['Slow_MA'], label=f'MA {slow_ma_period}', color='magenta')
        ax.set_title(f'{ticker} ', fontsize=14)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.3)

        plt.tight_layout()
        plt.savefig(f"{path}{ticker}_ma.png")
        plt.close()



def generar_grafico(tickers, path):
    
    # Parámetros configurables (¡flexibilidad total!)
    fast_ma_period = 20  # Media móvil rápida
    slow_ma_period = 50  # Media móvil lenta
    period = '6mo'       # Período de datos históricos
    
    num_tickers = len(tickers)
    fig, axes = plt.subplots(num_tickers, 1, figsize=(12, 5 * num_tickers))
    if num_tickers == 1:
        axes = [axes]  # Ajuste para un solo gráfico

    for i, ticker in enumerate(tickers):

        data = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        data['Fast_MA'] = data['Close'].rolling(window=fast_ma_period).mean()
        data['Slow_MA'] = data['Close'].rolling(window=slow_ma_period).mean()

        ax = axes[i]
        ax.plot(data['Close'], label='Precio', color='cyan')
        ax.plot(data['Fast_MA'], label=f'MA {fast_ma_period}', color='orange')
        ax.plot(data['Slow_MA'], label=f'MA {slow_ma_period}', color='magenta')
        ax.set_title(f'{ticker} ', fontsize=14)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.savefig(path)
    plt.close()



def generar_graficos_vol(tickers, path):
    
    # Parámetros configurables
    fast_ma_period = 20
    slow_ma_period = 50
    period = '6mo'

    for i, ticker in enumerate(tickers):

        fig, ax1 = plt.subplots(figsize=(12, 6))
        data = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        data['Fast_MA'] = data['Close'].rolling(window=fast_ma_period).mean()
        data['Slow_MA'] = data['Close'].rolling(window=slow_ma_period).mean()

        # Eje principal: precios y medias móviles
        ax1.plot(data['Close'], label='Precio', color='cyan')
        ax1.plot(data['Fast_MA'], label=f'MA {fast_ma_period}', color='orange')
        ax1.plot(data['Slow_MA'], label=f'MA {slow_ma_period}', color='magenta')
        ax1.set_title(f'{ticker}', fontsize=14)
        ax1.set_ylabel("Precio")
        ax1.grid(True, linestyle='--', alpha=0.3)

        # Eje secundario: volumen
        ax2 = ax1.twinx()
        ax2.bar(data.index, data['Volume'], width=1.0, color='lightgray', alpha=0.3, label='Volumen')
        ax2.set_ylabel("Volumen")

        # Combinar leyendas
        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper left')

        plt.tight_layout()
        plt.savefig(f"{path}{ticker}_ma.png")
        plt.close()
    


def generar_grafico_col(tickers, path,columnas=2):
    
    num_tickers = len(tickers)
    num_columnas = 2
    num_filas = (num_tickers + num_columnas - 1) // num_columnas  # Calcula el número de filas necesarias


    # Parámetros configurables (¡flexibilidad total!)
    fast_ma_period = 20  # Media móvil rápida
    slow_ma_period = 50  # Media móvil lenta
    period = '6mo'       # Período de datos históricos
    
    num_tickers = len(tickers)
    fig, axes = plt.subplots(num_filas, num_columnas, figsize=(16, 4 * num_filas))
    axes = axes.flatten()  # Aplanamos los ejes para facilitar el acceso


    for i, ticker in enumerate(tickers):

        data = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        data['Fast_MA'] = data['Close'].rolling(window=fast_ma_period).mean()
        data['Slow_MA'] = data['Close'].rolling(window=slow_ma_period).mean()

        ax = axes[i]
        ax.plot(data['Close'], label='Precio', color='cyan')
        ax.plot(data['Fast_MA'], label=f'MA {fast_ma_period}', color='orange')
        ax.plot(data['Slow_MA'], label=f'MA {slow_ma_period}', color='magenta')
        ax.set_title(f'{ticker} ', fontsize=14)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.3)

    # Ocultamos los ejes vacíos si los hay
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.savefig(path)
    plt.close()

#generar_graficos(['SPY', 'AAPL', 'GOOGL','SPY', 'AAPL', 'GOOGL','SPY', 'AAPL', 'GOOGL','SPY', 'AAPL', 'GOOGL','SPY', 'AAPL', 'GOOGL','SPY', 'AAPL', 'GOOGL','SPY', 'AAPL', 'GOOGL','SPY', 'AAPL', 'GOOGL','SPY', 'AAPL', 'GOOGL'], "C:/users/mrella/OneDrive - Consorci Administració Oberta de Catalunya/Inversion/FinanceMR/gappers/gappers.png") 