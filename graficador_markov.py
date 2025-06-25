import yfinance as yf
import numpy as np
import pandas as pd
from hmmlearn import hmm
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import seaborn as sns
sns.set_theme(style="darkgrid", palette="muted", font_scale=1.1)
import warnings
import matplotlib
matplotlib.use('Agg') 

warnings.filterwarnings('ignore')



# 1. Descargar datos históricos del S&P 500 usando yfinance
def descargar_datos(ticker='^GSPC', periodo='5y', interval="1d"):
    data = yf.download(ticker, period=periodo, progress=False, interval=interval)
    print(data)
    return data

# 2. Calcular volatilidad: True Range y Average True Range (ATR)
def calcular_atr(data, window=30):
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=window).mean()
    return atr


def preprocesar_datos_return(data):
    # Calcular retornos logarítmicos
    data['Return'] = np.log(data['Close'] / data['Close'].shift(1))
    # Eliminar filas con NaN (pueden haber valores NaN en las primeras filas por cálculos de ATR)
    data.dropna(inplace=True)
    # Normalizar características: Retornos, Volumen y Volatilidad
    scaler = StandardScaler()
    features = data[['Return']].values
    data.dropna(inplace=True)
    scaled_features = scaler.fit_transform(features)
    return scaled_features, data


def preprocesar_datos_atr(data):
    # Calcular ATR para la volatilidad
    data['Volatility_ATR'] = calcular_atr(data)
    # Eliminar filas con NaN (pueden haber valores NaN en las primeras filas por cálculos de ATR)
    data.dropna(inplace=True)
    scaler = StandardScaler()
    features = data[['Volatility_ATR']].values
    data.dropna(inplace=True)
    scaled_features = scaler.fit_transform(features)
    return scaled_features, data


def preprocesar_datos_atrvol(data):
    data['Return'] = np.log(data['Close'] / data['Close'].shift(1))
    data.dropna(inplace=True)
    data['Volatility_ATR'] = calcular_atr(data)
    data.dropna(inplace=True)
    scaler = StandardScaler()
    features = data[['Return', 'Volatility_ATR']].values
    data.dropna(inplace=True)
    scaled_features = scaler.fit_transform(features)
    return scaled_features, data


def preprocesar_datos_all(data):
    # Calcular retornos logarítmicos
    data['Return'] = np.log(data['Close'] / data['Close'].shift(1))
    # Calcular ATR para la volatilidad
    data['Volatility_ATR'] = calcular_atr(data)
    # Eliminar filas con NaN (pueden haber valores NaN en las primeras filas por cálculos de ATR)
    data.dropna(inplace=True)
    # Normalizar características: Retornos, Volumen y Volatilidad
    scaler = StandardScaler()
    features = data[['Return', 'Volume', 'Volatility_ATR']].values
    #data['Volumen_Monetario'] = data['Volume'] * data['Adj Close']
    data.dropna(inplace=True)
    scaler = StandardScaler()
    #features = scaler.fit_transform(data['Return'].values.reshape(-1, 1))
    scaled_features = scaler.fit_transform(features)
    return scaled_features, data



# 4. Entrenar un modelo HMM
def entrenar_hmm(datos, n_states):
    modelo_hmm = hmm.GaussianHMM(n_components=n_states, covariance_type="full", n_iter=3000)
    modelo_hmm.fit(datos)
    estados_ocultos = modelo_hmm.predict(datos)
    return modelo_hmm, estados_ocultos

# 5. Graficar los estados ocultos sobre los datos originales
def graficar_estados(data, estados_ocultos, type,  modelo_hmm, chart_path, ticker):
    fig, ax = plt.subplots(figsize=(12, 6))
    for i in range(modelo_hmm.n_components):
        idx = (estados_ocultos == i)
        colors = ['cyan', 'orange']
        ax.plot(data.index[idx], data['Close'][idx], '.', color=colors[i], label=f"Estado {i}")
    #ax.plot(data.index, data['Close'], label='S&P 500', color='black')
    plt.title(f'{ticker} con estados ocultos (HMM) {type}')
    plt.legend()
    plt.savefig(chart_path)
    plt.close()

# 6. Ejecutar el análisis completo
def generar_graficos(tickers, path, periodo):

    for ticker in tickers:
        try:
            datos = descargar_datos(ticker, periodo=periodo, interval="1d")

            features_scaled, datos_procesados = preprocesar_datos_return(datos)
            modelo_hmm, estados_ocultos = entrenar_hmm(features_scaled, n_states=2)
            graficar_estados(datos_procesados, estados_ocultos, 'Return', modelo_hmm, f"{path}{ticker}_markov_return.png", ticker)

            features_scaled, datos_procesados = preprocesar_datos_atr(datos)
            modelo_hmm, estados_ocultos = entrenar_hmm(features_scaled, n_states=2)
            graficar_estados(datos_procesados, estados_ocultos, 'ATR',  modelo_hmm, f"{path}{ticker}_markov_atr.png", ticker)
        except Exception as e:
            print(f"Error procesando {ticker}: {e}")
            plt.close()  # Cerrar cualquier figura abierta para evitar fugas de memoria
            continue

        #datos = descargar_datos(ticker="QQQ")

        #features_scaled, datos_procesados = preprocesar_datos_return(datos)
        #modelo_hmm, estados_ocultos = entrenar_hmm(features_scaled, n_states=2)
        #graficar_estados(datos_procesados, estados_ocultos, 'Return', modelo_hmm, path_markov+"markov_qqq_return.png")

        #features_scaled, datos_procesados = preprocesar_datos_atr(datos)
        #modelo_hmm, estados_ocultos = entrenar_hmm(features_scaled, n_states=2)
        #graficar_estados(datos_procesados, estados_ocultos, 'ATR',  modelo_hmm, path_markov+"markov_qqq_atr.png")


    #features_scaled, datos_procesados = preprocesar_datos_atrvol(datos)
    #modelo_hmm, estados_ocultos = entrenar_hmm(features_scaled, n_states=2)
    #graficar_estados(datos_procesados, estados_ocultos, 'atrreturn')

    #features_scaled, datos_procesados = preprocesar_datos_all(datos)
    #modelo_hmm, estados_ocultos = entrenar_hmm(features_scaled, n_states=2)
    #graficar_estados(datos_procesados, estados_ocultos, 'all')