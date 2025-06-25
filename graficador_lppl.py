import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy.optimize import curve_fit
from matplotlib.animation import FuncAnimation
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import seaborn as sns
sns.set_theme(style="darkgrid", palette="muted", font_scale=1.1)
import matplotlib
matplotlib.use('Agg')


fecha_inicio = f"{datetime.now().year}-01-01"
fecha_fin = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


# === Función LPPL ===
def lppl(t, A, B, C, tc, m, omega, phi):
    return A + B * (tc - t) ** m + C * (tc - t) ** m * np.cos(omega * np.log(tc - t) - phi)


def generar_grafico_lppl(path, ticker, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin):

    # === Descargar datos del SPY desde 2015 ===
    spy = yf.download(ticker, start=fecha_inicio, end=fecha_fin)
    spy['LogClose'] = np.log(spy['Close'])
    spy = spy.reset_index()
    spy['t'] = np.arange(len(spy))  # tiempo discreto

    # === Ajustar LPPL al periodo completo ===
    t = spy['t'].values
    log_price = spy['LogClose'].values

    # === Parámetros iniciales ===
    tc_init = t[-1] + 50  # fecha crítica 50 días después del último
    p0 = [10, -1, 0.1, tc_init, 0.5, 8, 0]

    # === Límites de parámetros razonables ===
    bounds = ([0, -np.inf, -np.inf, t[-1], 0.01, 6, -np.pi],
            [np.inf, 0, np.inf, t[-1] + 300, 1, 13, np.pi])

    # === Ajuste LPPL ===
    try:
        popt, _ = curve_fit(lppl, t, log_price, p0=p0, bounds=bounds, maxfev=10000)
        fitted_lppl = lppl(t, *popt)
    except RuntimeError:
        print("El ajuste LPPL no convergió.")
        popt = None
        fitted_lppl = None

    # === Gráfica ===
    plt.figure(figsize=(14, 6))
    plt.plot(spy['Date'], log_price, label='Log Precio '+ticker, color='cyan')
    if fitted_lppl is not None:
        plt.plot(spy['Date'], fitted_lppl, label='Modelo LPPL', color='orange')
    plt.title('Ajuste LPPL al ' + ticker)
    plt.xlabel('Fecha')
    plt.ylabel('Log Precio')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()




def generar_graficos(tickers, path):
        
    
    for ticker in tickers:
        try:
            # === Descargar datos ===    
            data = yf.download(ticker, start=fecha_inicio, period='6mo', auto_adjust=True, progress=False) #end=fecha_fin, progress=False)
            data = data[['Close']]
            data = data.reset_index()
            data['t'] = np.arange(len(data))
            data['LogClose'] = np.log(data['Close'])

            # === Ajustar LPPL ===
            t = data['t'].values
            log_price = data['LogClose'].values

            # Parámetros iniciales
            tc_init = t[-1] + 30
            p0 = [10, -1, 0.1, tc_init, 0.5, 8, 0]
            bounds = ([0, -np.inf, -np.inf, t[-1], 0.01, 6, -np.pi],
                    [np.inf, 0, np.inf, t[-1] + 200, 1, 13, np.pi])


            try:
                popt, _ = curve_fit(lppl, t, log_price, p0=p0, bounds=bounds, maxfev=10000)
                data['LPPL'] = lppl(t, *popt)
                data['Residual'] = data['LogClose'] - data['LPPL']
            except RuntimeError:
                print("El ajuste LPPL no convergió.")
                data['LPPL'] = np.nan
                data['Residual'] = np.nan

            # === Detectar extremos LPPL (percentiles) ===
            q_high = data['Residual'].quantile(0.975)
            q_low = data['Residual'].quantile(0.025)

            data['Overbought'] = np.where(data['Residual'] > q_high, data['Residual'] - q_high, 0)
            data['Oversold'] = np.where(data['Residual'] < q_low, q_low - data['Residual'], 0)

            # === Graficar ===
            fig, ax1 = plt.subplots(figsize=(14, 6))

            # Precio real
            ax1.plot(data['Date'], data['LogClose'], color='cyan', label='Precio')
            if data['LPPL'] is not None:
                ax1.plot(data['Date'], data['LPPL'], label='Modelo LPPL', color='orange')
            ax1.set_ylabel('Precio')
            ax1.set_title(f'{ticker}  Señales de Sobrecompra/Sobreventa basadas en LPPL')
            
            

            # Segundo eje para extremos
            ax2 = ax1.twinx()
            ax2.bar(data['Date'], data['Overbought'], width=1.5, color='red', alpha=0.5, label='Sobrecompra LPPL')
            ax2.bar(data['Date'], data['Oversold'], width=1.5, color='green', alpha=0.5, label='Sobreventa LPPL')
            ax2.set_ylabel('Nivel de Desviación Log-Precio vs LPPL')

            # Leyenda y estilo
            fig.legend(loc='upper left')
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f"{path}{ticker}_lppl.png")
            plt.close()
        except Exception:
            plt.close()
            continue


